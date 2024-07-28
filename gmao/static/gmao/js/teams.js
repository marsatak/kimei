let interventionEnCours = false;

$(document).ready(function () {
    /* EFA MANDE FA NOLOKOINA NY LIGNE`/
    /*function initPortfolioTable(data, interventionEnCoursGlobal) {
        console.log("Initialisation de la table avec les données:", data);
        if ($('#portfolioTable').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            try {
                $('#portfolioTable').DataTable({
                    data: data,
                    columns: [
                        {data: 'ndi', title: 'NDI'},
                        {data: 'station', title: 'Station'},
                        {data: 'element', title: 'Élément'},
                        {
                            data: 'panne_declarer',
                            title: 'Panne',
                            render: function (data, type, row) {
                                if (type === 'display' && data.length > 50) {
                                    return '<span title="' + data + '">' + data.substr(0, 50) + '...</span>';
                                }
                                return data;
                            }
                        },
                        {data: 'statut', title: 'Statut'},
                        {
                            data: null,
                            title: 'Actions',
                            render: function (data, type, row) {
                                return getActionButton(row, interventionEnCoursGlobal);
                            }
                        }
                    ],
                    responsive: true,
                    language: {
                        url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                    },
                    searching: false,
                    info: false,
                    paginate: false,
                    ordering: false,
                    pageLength: -1,  // Affiche toutes les entrées
                    lengthChange: false,  // Supprime le sélecteur de nombre d'entrées
                    order: [[0, 'asc']],
                    drawCallback: function (settings) {
                        console.log("DrawCallback - Intervention en cours (global):", interventionEnCoursGlobal);
                        $('.prendre-en-charge').prop('disable', interventionEnCoursGlobal);
                    },
                    columnDefs: [
                        {
                            orderable: false,
                            targets: 3, // Index de la colonne 'Panne'
                            className: 'text-wrap'
                        }
                    ]
                });
            } catch (error) {
                console.error("Erreur lors de l'initialisation de la table:", error);
            }
        } else {
            console.error("L'élément #portfolioTable n'existe pas dans le DOM");
        }
    }*/


    function initPortfolioTable(data, interventionEnCoursGlobal) {
        console.log("Initialisation de la table avec les données:", data);
        if ($('#portfolioTable').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            try {
                const table = $('#portfolioTable').DataTable({
                    data: data,
                    columns: [
                        {data: 'ndi', title: 'NDI', width: "10%"},
                        {data: 'station', title: 'Station', width: "15%"},
                        {data: 'statut', title: 'Statut', width: "10%"},
                        {data: 'element', title: 'Élément', width: "15%"},
                        {
                            data: 'panne_declarer',
                            title: 'Panne',
                            width: "30%",
                            render: function (data, type, row) {
                                if (type === 'display') {
                                    return '<div class="text-wrap width-200">' + data + '</div>';
                                }
                                return data;
                            }
                        },
                        {
                            data: null,
                            title: 'Actions',
                            width: "20%",
                            render: function (data, type, row) {
                                return getActionButton(row, interventionEnCoursGlobal);
                            }
                        }
                    ],
                    responsive: true,
                    language: {
                        url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                    },
                    searching: false,
                    info: false,
                    paginate: false,
                    ordering: false,
                    pageLength: -1,
                    lengthChange: false,
                    order: [[0, 'asc']],
                    drawCallback: function (settings) {
                        console.log("DrawCallback - Intervention en cours (global):", interventionEnCoursGlobal);
                        $('.prendre-en-charge').prop('disabled', interventionEnCoursGlobal);
                    },
                    createdRow: function (row, data, dataIndex) {
                        $(row).addClass('status-' + data.statut);
                        $('td', row).each(function (index, td) {
                            $(td).attr('data-label', $(td).closest('table').find('th').eq(index).text());
                        });
                    },
                    columnDefs: [
                        {
                            targets: '_all',
                            className: 'text-wrap'
                        }
                    ]
                });

                // Open all rows by default
                table.rows().every(function () {
                    this.child.show();
                    $(this.node()).addClass('parent');
                });

            } catch (error) {
                console.error("Erreur lors de l'initialisation de la table:", error);
            }
        } else {
            console.error("L'élément #portfolioTable n'existe pas dans le DOM");
        }
    }


    function loadTechnicienPortfolio() {
        console.log("Chargement du portfolio du technicien...");
        $.ajax({
            url: '/get-technicien-portfolio/',
            type: 'GET',
            success: function (response) {
                console.log("Réponse reçue du serveur:", response);
                if (response.success) {
                    console.log("Intervention en cours (global):", response.intervention_en_cours);
                    interventionEnCours = response.intervention_en_cours;
                    initPortfolioTable(response.doleances, interventionEnCours);
                } else {
                    console.error("Erreur dans la réponse du serveur:", response.message);
                    $('#portfolioContainer').html('<p>' + response.message + '</p>');
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", status, error);
                $('#portfolioContainer').html('<p>Erreur lors du chargement des données.</p>');
            }
        });
    }

    function prendreEnCharge(doleanceId) {
        console.log('prendreEnCharge appelé pour', doleanceId);
        $.ajax({
            url: `/home/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                console.log('Réponse reçue:', response);
                if (response.success) {
                    alert(response.message);
                    interventionEnCours = true;
                    loadTechnicienPortfolio();
                    window.location.reload();
                } else {
                    console.error("Erreur lors de la prise en charge:", response.message);
                    alert('Erreur : ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX lors de la prise en charge:", status, error);
                alert('Erreur de communication avec le serveur');
            }
        });
    }

    function getActionButton(doleance, interventionEnCours) {
        if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm btn-block">Détails intervention</a>`;
        } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !interventionEnCours) {
            return `<button class="btn btn-success btn-sm btn-block prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
        } else {
            return '<span class="text-muted">Aucune action disponible</span>';
        }
    }


    $(document).on('click', '.prendre-en-charge', function (e) {
        e.preventDefault();
        const doleanceId = $(this).data('id');
        prendreEnCharge(doleanceId);
    });
    loadTechnicienPortfolio();
    setInterval(loadTechnicienPortfolio, 300000);

    function getStatusColorClass(statut) {
        switch (statut) {
            case 'NEW':
                return 'bg-new';
            case 'ATT':
                return 'bg-att';
            case 'INT':
                return 'bg-int';
            case 'ATP':
                return 'bg-atp';
            case 'ATD':
                return 'bg-atd';
            default:
                return 'bg-light text-dark';
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Appelez cette fonction au chargement de la page et peut-être périodiquement