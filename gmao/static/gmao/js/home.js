$(document).ready(function () {
    let doleanceTable;
    let personnelTable;
    let portofolioTable;
    document.addEventListener('DOMContentLoaded', function () {
        const upperCaseInputs = document.querySelectorAll('input[type="text"], textarea');
        upperCaseInputs.forEach(input => {
            input.addEventListener('input', function () {
                this.value = this.value.toUpperCase();
            });
        });
    });

    function offsetAnchor() {
        if (location.hash.length !== 0) {
            window.scrollTo(window.scrollX, window.scrollY - 60);
        }
    }

    // Appliquer l'ajustement au chargement de la page
    $(window).on("hashchange", function () {
        offsetAnchor();
    });

    // Déclencher le hashchange initial
    window.setTimeout(function () {
        offsetAnchor();
    }, 1);

    function initDoleanceTable() {
        if ($('#demandeencours').length && !$.fn.DataTable.isDataTable('#demandeencours')) {
            doleanceTable = $('#demandeencours').DataTable({
                striping: false,
                'ajax': {
                    "type": "GET",

                    "url": "/home/getDoleanceEncours",
                    "dataSrc": function (json) {
                        return json;
                    }
                },
                'columns': [
                    {'data': "id"},
                    {'data': "ndi"},
                    {
                        'data': 'date_transmission',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                return moment(data).format('DD/MM/YYYY HH:mm');
                            }
                            return data;
                        }
                    },
                    {
                        'data': "statut",
                        'render': function (data, type, row) {
                            switch (data) {
                                case 'NEW':
                                    return 'NEW';
                                case 'ATT':
                                    return 'ATT';
                                case 'INT':
                                    return 'INT';
                                case 'ATP':
                                    return 'ATP';
                                case 'ATD':
                                    return 'ATD';
                                case 'TER':
                                    return 'TER';
                                default:
                                    return data;
                            }
                        }
                    },
                    {'data': "station.libelle_station"},
                    {'data': 'element'},
                    {'data': 'panne_declarer'},
                    {
                        'data': 'date_deadline',
                        render: function (data, type, row) {
                            if (type === 'display' || type === 'filter') {
                                return moment(data).format('DD/MM/YYYY HH:mm');
                            }
                            return data;
                        }
                    },
                    {'data': 'commentaire'},
                    /*            {
                                    'className': 'details-control',
                                    'orderable': false,
                                    'data': null,
                                    'defaultContent': ''
                                },*/
                    {
                        'data': null,
                        'render': function (data, type, row) {
                            let buttons = '';
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                buttons += '<button class="btn btn-primary btn-sm declencher-intervention" data-id="' + row.id + '">Déclencher intervention</button> ';
                            }
                            return buttons;
                        }
                    },
                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                dom: 'Bfrtip',
                buttons: [
                    'copy', 'csv', 'excel', 'pdf', 'print'
                ],
                ordering: false,
                columnDefs: [
                    {
                        targets: '_all',
                        className: 'dt-head-nowrap',
                        render: function (data, type, row) {
                            if (type === 'display' && data != null && data.length > 70) {
                                return `<span title="${data}">${data.substr(0, 70)}...</span>`;
                            }
                            return data;
                        }
                    },
                    {
                        targets: [0],
                        visible: false,
                        searchable: false
                    },
                    {responsivePriority: 1, targets: 1}, // NDI
                    {responsivePriority: 2, targets: 3}, // Statut
                    {responsivePriority: 3, targets: 6}, // Panne déclarée
                    {responsivePriority: 10000, targets: [2, 4, 5, 7, 8]}
                ],
                createdRow: function (row, data, dataIndex) {
                    if (data.statut === 'NEW') {
                        $(row).addClass('table-success');
                    } else if (data.statut === 'ATP') {
                        $(row).addClass('table-warning');
                    } else if (data.statut === 'ATD') {
                        $(row).addClass('table-infodanger');
                    }
                },
            });
        }

    }

    //initDoleanceTable();
    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });

    function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                'ajax': {
                    "type": "GET",
                    "url": "/home/getPersonnel/",
                    "dataSrc": function (json) {
                        console.log("Données du personnel reçues:", json);
                        return json;
                    }
                },
                'columns': [
                    {'data': "id"},
                    {'data': "nom_personnel"},
                    {'data': "prenom_personnel"},
                    {
                        'data': "statut",
                        'render': function (data, type, row) {
                            let statusIcon = '';
                            let statusText = '';
                            switch (data) {
                                case 'PRS':
                                    statusIcon = '<i class="fas fa-check-circle text-success"></i>';
                                    statusText = 'Présent';
                                    break;
                                case 'ABS':
                                    statusIcon = '<i class="fas fa-times-circle text-danger"></i>';
                                    statusText = 'Absent';
                                    break;
                                case 'ATT':
                                    statusIcon = '<i class="fas fa-clock text-warning"></i>';
                                    statusText = 'Tâche attribuée';
                                    break;
                                case 'INT':
                                    statusIcon = '<i class="fas fa-hard-hat text-info"></i>';
                                    statusText = 'En intervention';
                                    break;
                            }
                            return `${statusIcon} ${statusText}`;
                        }
                    },
                    {
                        'data': null,
                        'render': function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="'
                                    + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="'
                                    + row.id + '">Marquer départ</button>';
                            } else {
                                return '';
                            }
                        }
                    }

                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                ordering: false,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                dom: 'Bfrtip',
                columnDefs: [
                    {
                        targets: [0],
                        visible: false,
                        searchable: false,
                    },
                    {
                        targets: [3],
                        render: function (data) {
                            return data === 'PRS' ? '<span class="badge bg-success">PRS</span>' :
                                data === 'ATT' ? '<span class="badge bg-warning">ATT</span>' :
                                    data === 'INT' ? '<span class="badge bg-info">INT</span>' :
                                        '<span class="badge bg-danger">ABS</span>';
                        }
                    },
                    {
                        targets: '_all',
                        className: 'dt-head-nowrap'
                    },
                    {responsivePriority: 1000, targets: 1}, // Nom
                    {responsivePriority: 1, targets: 2}, //
                    {responsivePriority: 2, targets: 3},
                ]
            });
        }
    }

    //initPersonnelTable();
    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        if (!$.fn.DataTable.isDataTable('#demandeencours')) {
            initDoleanceTable();
        }
        if (!$.fn.DataTable.isDataTable('#personnel')) {
            initPersonnelTable();
        }
    } else if ($('#portfolioContainer').length) {
        //loadTechnicienPortfolio();
    }

    // Fonction pour rafraîchir la table des doléances
    function refreshDoleanceTable() {
        if (doleanceTable) {
            doleanceTable.ajax.reload(null, false);
        }
    }

    // Fonction pour rafraîchir la table du personnel
    function refreshPersonnelTable() {
        if (personnelTable) {
            personnelTable.ajax.reload(null, false);
        }
    }


    $(window).resize(function () {
        $('#demandeencours').DataTable().draw();
        $('#personnel').DataTable().draw();
    });
    $('#doleanceModal').on('show.bs.modal', function () {
        console.log('Modal is about to open');
    });
    $('#personnel').on('click', '.mark-arrivee', function () {
        const personnelId = $(this).data('id');
        markArriveeOrDepart(personnelId, true);
    });

    $('#personnel').on('click', '.mark-depart', function () {
        const personnelId = $(this).data('id');
        markArriveeOrDepart(personnelId, false);
    });

    function markArriveeOrDepart(personnelId, isArrivee) {
        $.ajax({
            url: isArrivee ? `/mark-arrivee/${personnelId}/` : `/mark-depart/${personnelId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    personnelTable.ajax.reload();
                } else {
                    alert('Erreur : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }

    function declencherIntervention(doleanceId) {
        $.ajax({
            url: '/home/get-techniciens-disponibles/',
            type: 'GET',
            dataType: 'json',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    afficherSelectionTechniciens(response.techniciens, doleanceId);
                } else {
                    alert('Erreur lors de la récupération des techniciens disponibles');
                }
            },
            error: function () {
                alert('Erreur lors de la communication avec le serveur');
            }
        });
    }


    function afficherSelectionTechniciens(techniciens, doleanceId) {
        let dialog = $('<div title="Sélectionner les techniciens">');
        let form = $('<form>');

        techniciens.forEach(function (tech) {
            form.append(`
                    <div>
                        <input type="checkbox" id="tech-${tech.id}" name="techniciens" value="${tech.id}">
                        <label for="tech-${tech.id}">${tech.nom_personnel} ${tech.prenom_personnel}</label>
                    </div>
                `);
        });

        dialog.append(form);

        dialog.dialog({
            modal: true,
            buttons: {
                "Confirmer": function () {
                    let techniciensSelecionnes = form.find('input:checked').map(function () {
                        return $(this).val();
                    }).get();

                    if (techniciensSelecionnes.length > 0) {
                        declencherInterventionAvecTechniciens(doleanceId, techniciensSelecionnes);
                        $(this).dialog("close");
                    } else {
                        alert("Veuillez sélectionner au moins un technicien.");
                    }
                },
                "Annuler": function () {
                    $(this).dialog("close");
                }
            }
        });
    }

    function declencherInterventionAvecTechniciens(doleanceId, techniciens) {
        $.ajax({
            url: '/home/declencher-intervention/' + doleanceId + '/',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({techniciens: techniciens}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function (response) {
                if (response.success) {
                    alert('Intervention déclenchée avec succès pour les techniciens sélectionnés.');
                    refreshPersonnelTable(); // Rafraîchir la table du personnel
                    window.location.href = '/home/intervention/' + response.intervention_id + '/';
                } else {
                    alert('Erreur lors du déclenchement de l\'intervention: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                alert('Erreur lors de la communication avec le serveur: ' + error);
            }
        });
    }


    $('#demandeencours').on('click', '.terminer-intervention', function () {
        const interventionId = $(this).data('id');
        terminerIntervention(interventionId);
    });

    $('#demandeencours').on('click', '.nouvelle-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });
    $('#demandeencours').on('click', '.commencer-intervention', function () {
        const interventionId = $(this).data('id');
        commencerIntervention(interventionId);
    });

    function formatInterventions(data, rowData) {
        if (!data.interventions || data.interventions.length === 0) {
            return '<p>Aucune intervention pour cette doléance.</p>';
        }

        var html = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
        html += '<tr><th>Date de début</th><th>Date de fin</th><th>Statut</th><th>Techniciens</th><th>Actions</th></tr>';

        data.interventions.forEach(function (intervention) {
            html += '<tr>';
            html += '<td>' + (intervention.top_depart || '-') + '</td>';
            html += '<td>' + (intervention.top_terminer || '-') + '</td>';
            html += '<td>' + (intervention.is_done ? 'Terminée' : (intervention.is_half_done ? 'En cours' : 'Non commencée')) + '</td>';
            html += '<td>' + (intervention.techniciens ? intervention.techniciens.join(', ') : '-') + '</td>';
            html += '<td>';
            if (!intervention.top_debut) {
                html += '<button class="btn btn-success btn-sm commencer-intervention" data-id="' + intervention.id + '">Commencer</button> ';
            } else if (!intervention.is_done) {
                html += '<button class="btn btn-primary btn-sm terminer-intervention" data-id="' + intervention.id + '">Terminer</button> ';
            }
            html += '</td>';
            html += '</tr>';
        });

        html += '</table>';
        if (rowData.statut === 'NEW' || rowData.statut === 'ATP' || rowData.statut === 'ATD') {
            html += '<button class="btn btn-success btn-sm nouvelle-intervention" data-id="' + rowData.id + '">Nouvelle intervention</button>';
        }
        return html;
    }


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

    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $('#interventionForm').submit(function (e) {
        e.preventDefault();

        var formData = new FormData(this);
        var interventionId = $('#intervention-id-input').val();

        $.ajax({
            url: '/home/intervention/' + interventionId + '/terminer/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                console.log("Réponse reçue:", response);  // Log de la réponse complète
                if (response.success) {
                    alert('Intervention terminée avec succès.');
                    window.location.href = '/home/';
                } else {
                    console.error("Erreur côté serveur:", response.message);
                    alert('Erreur lors de la terminaison de l\'intervention: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                alert('Erreur lors de la communication avec le serveur: ' + error);
            }
        });
    });


    function affecterTechniciens(doleanceId, technicienIds) {
        $.ajax({
            url: '/home/affecter-techniciens/' + doleanceId + '/',
            type: 'POST',
            dataType: 'json',
            data: JSON.stringify({techniciens: technicienIds}),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken()
            },
            success: function (response) {
                if (response.success) {
                    alert('Techniciens affectés avec succès.');
                    refreshTables();
                } else {
                    alert('Erreur lors de l\'affectation des techniciens: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                alert('Erreur lors de la communication avec le serveur: ' + error);
            }
        });
    }

    /*function loadTechnicienPortfolio() {
        $.ajax({
            url: '/get-technicien-portfolio/',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    updatePortfolioTable(response.doleances);
                } else {
                    alert('Erreur lors du chargement du portefeuille : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }*/


    // Charger le portefeuille au chargement de la page si l'utilisateur est un technicien


});


