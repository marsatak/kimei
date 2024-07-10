$(document).ready(function () {
    let doleanceTable, personnelTable, portofolioTable;
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
                ajax: {
                    url: "/home/getDoleanceEncours",
                    dataSrc: ""
                },
                columns: [
                    {data: "ndi", width: "7%%"},
                    {
                        data: "date_transmission", width: "8%",
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: "statut", width: "3%"},
                    {data: "station.libelle_station", width: "8%"},
                    {data: 'element', width: "17%"},
                    {
                        data: 'panne_declarer', width: "24%",
                        render: function (data, type, row) {
                            return '<div class="text-wrap width-500">' + data + '</div>';
                        }
                    },
                    {
                        data: 'date_deadline', width: "8%",
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: 'commentaire', width: "15%"},
                    {
                        data: null, width: "10%",
                        render: function (data, type, row) {
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                return '<button class="btn btn-primary btn-sm declencher-intervention" data-id="' + row.id + '">' +
                                    '<i class="fas fa-arrow-alt-circle-up"></i>' +
                                    '</button>';
                            }
                            return '';
                        }
                    },
                ],
                responsive: true,
                autoWidth: false,
                ordering: false,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                createdRow: function (row, data, dataIndex) {
                    $(row).addClass('status-' + data.statut)
                },
                columnDefs: [
                    {targets: [1, 6], className: 'date-column'},
                    {targets: [2], className: 'status-column'},
                    {
                        targets: '_all', render: function (data, type, row) {
                            if (type === 'display' && data != null && data.length > 70) {
                                return `<span title="${data}">${data.substr(0, 70)}...</span>`;
                            }
                            return data;
                        }
                    },
                    {responsivePriority: 1, targets: 1}, // NDI
                    {responsivePriority: 2, targets: 3}, // Statut
                    {responsivePriority: 3, targets: 6}, // Panne déclarée
                    {responsivePriority: 4, targets: 8}, // Actions
                    {responsivePriority: 10000, targets: [2, 4, 5, 7]}
                ]
            });
        }
    }


    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });

    function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                ajax: {
                    url: "/home/getPersonnel/",
                    dataSrc: function (json) {
                        // Trier les techniciens en premier
                        return json.sort((a, b) => {
                            if (a.poste.nom_poste === 'Technicien' && b.poste.nom_poste !== 'Technicien') return -1;
                            if (a.poste.nom_poste !== 'Technicien' && b.poste.nom_poste === 'Technicien') return 1;
                            return 0;
                        });
                    }
                },
                columns: [
                    {data: "nom_personnel"},
                    {data: "prenom_personnel"},
                    {
                        data: "statut",
                        render: function (data, type, row) {
                            const statusClasses = {
                                'PRS': 'bg-success',
                                'ATT': 'bg-warning',
                                'INT': 'bg-info',
                                'ABS': 'bg-danger'
                            };
                            return `<span class="badge ${statusClasses[data] || 'bg-secondary'}">${data}</span>`;
                        },
                        className: 'status-column'
                    },
                    {
                        data: null,
                        render: function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="' + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="' + row.id + '">Marquer départ</button>';
                            }
                            return '';
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                ordering: false,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                }
            });
        }
    }

    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        initDoleanceTable();
        initPersonnelTable();
    } else if ($('#portfolioContainer').length) {
        loadTechnicienPortfolio();
    }

    function refreshDoleanceTable() {
        if (doleanceTable) {
            doleanceTable.ajax.reload(null, false);
        }
    }

    setTimeout(refreshDoleanceTable, 60000)

    function refreshPersonnelTable() {
        if (personnelTable) {
            personnelTable.ajax.reload(null, false);
        }
    }


    $(window).resize(function () {
        if (doleanceTable) doleanceTable.columns.adjust().draw();
        if (personnelTable) personnelTable.columns.adjust().draw();
        $('#demandeencours').DataTable().draw();
        $('#personnel').DataTable().draw();
    });
    /*$('#doleanceModal').on('show.bs.modal', function () {
        console.log('Modal is about to open');
    });*/
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
            width: 400,
            height: 400,
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


});