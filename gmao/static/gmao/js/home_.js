$(document).ready(function () {
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

    // Initialiser les DataTables
    // Liste des doléances en cours

    let doleanceTable = $('#demandeencours').DataTable({
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
            {'data': "statut"},
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
            // {
            //     'className': 'details-control',
            //     'orderable': false,
            //     'data': null,
            //     'defaultContent': ''
            // },
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
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
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

    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });

    /*$('#demandeencours tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);

        if (row.child.isShown()) {
            row.child.hide();
            tr.removeClass('shown');
        } else {
            $.ajax({
                url: '/home/interventions-doleance/' + row.data().id + '/',
                type: 'GET',
                success: function (data) {
                    row.child(formatInterventions(data, row.data())).show();
                    tr.addClass('shown');
                },
                error: function () {
                    alert('Erreur lors du chargement des interventions');
                }
            });
        }
    });*/

    /*$('#personnel').DataTable({
        'ajax': {
            "type": "GET",
            "url": "/home/getPersonnel",
            "dataSrc": function (json) {
                console.log("Données reçues:", json);
                return json;
            }
        },
        'columns': [
            {'data': "id"},
            {'data': "nom_personnel"},
            {'data': "prenom_personnel"},
            {'data': "statut"},
        ],
        responsive: true,
        autoWidth: false,
        pageLength: 10,
        ordering: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
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
                    return data === 'PRS' ? '<span class="badge bg-success">PRS</span>' : '<span class="badge bg-danger">ABS</span>';
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
    });*/
    let personnelTable = $('#personnel').DataTable({
        'ajax': {
            "type": "GET",
            "url": "/home/getPersonnel",
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
                            statusText = 'Tâches attribuées';
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
                        return '<button class="btn btn-success btn-sm mark-arrivee" data-id="' + row.id + '">Marquer arrivée</button>';
                    } else if (row.statut === 'PRS') {
                        return '<button class="btn btn-danger btn-sm mark-depart" data-id="' + row.id + '">Marquer départ</button>';
                    } else {
                        return '';
                    }
                }
            },
        ],
        responsive: true,
        autoWidth: false,
        pageLength: 10,
        ordering: false,
        language: {
            url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
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

    /*function refreshPersonnelTable() {
        personnelTable.ajax.reload(null, false);
    }*/

    /*function refreshDoleanceTable() {
        doleanceTable.ajax.reload(null, false);
    }*/

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


    $(window).resize(function () {
        $('#demandeencours').DataTable().draw();
        $('#personnel').DataTable().draw();
    });

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

//     function commencerIntervention(interventionId) {
//     $.ajax({
//         url: '/home/commencer-intervention/' + interventionId + '/',
//         type: 'POST',
//         dataType: 'json',
//         headers: {'X-CSRFToken': getCookie('csrftoken')},
//         success: function (response) {
//             if (response.success) {
//                 alert('Intervention commencée avec succès.');
//                 table.ajax.reload();
//             } else {
//                 alert('Erreur lors du démarrage de l\'intervention: ' + response.message);
//             }
//         },
//         error: function (xhr, status, error) {
//             console.error("Erreur AJAX:", xhr.responseText);
//             alert('Erreur lors de la communication avec le serveur: ' + error);
//         }
//     });
// }

    function commencerIntervention(interventionId) {
        $.ajax({
            url: '/home/commencer-intervention/' + interventionId + '/',
            type: 'POST',
            dataType: 'json',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert('Intervention commencée avec succès.');
                    // Rafraîchir la table des doléances
                    $('#demandeencours').DataTable().ajax.reload(null, false);
                    // Rafraîchir la table du personnel
                    refreshPersonnelTable();
                } else {
                    alert('Erreur lors du démarrage de l\'intervention: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                alert('Erreur lors de la communication avec le serveur: ' + error);
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

    /*function declencherInterventionAvecTechniciens(doleanceId, techniciens) {
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
                    // Rafraîchir la table des doléances
                $('#demandeencours').DataTable().ajax.reload(null, false);
                // Rafraîchir la table du personnel
                $('#personnel').DataTable().ajax.reload(null, false);

                    alert('Intervention déclenchée avec succès pour les techniciens sélectionnés.');
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
    }*/
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

    function terminerIntervention(interventionId) {
        console.log("Tentative de clôture de l'intervention", interventionId);
        let dialog = $(`<div title="Terminer l'intervention">`);
        let form = $('<form>');
        form.append('<textarea name="description_panne" placeholder="Description de la panne"></textarea>');
        form.append('<textarea name="travaux_effectues" placeholder="Travaux effectués"></textarea>');
        form.append('<textarea name="observations" placeholder="Observations"></textarea>');
        form.append('<textarea name="pieces_changees" placeholder="Pièces changées"></textarea>');
        form.append('<select name="statut_final"><option value="TER">Terminée</option><option value="ATP">Attente Pièces</option><option value="ATD">Attente Devis</option></select>');

        dialog.append(form);

        dialog.dialog({
            modal: true,
            buttons: {
                "Confirmer": function () {
                    const formData = new FormData(form[0]);
                    console.log("Données du formulaire:", Object.fromEntries(formData));
                    $.ajax({
                        url: '/home/terminer-intervention/' + interventionId + '/',
                        type: 'POST',
                        data: formData,
                        processData: false,
                        contentType: false,
                        headers: {'X-CSRFToken': getCookie('csrftoken')},
                        success: function (response) {
                            console.log("Réponse du serveur:", response);
                            if (response.success) {
                                alert('Intervention mise à jour avec succès.');
                                // Rafraîchir la table des doléances
                                $('#demandeencours').DataTable().ajax.reload(null, false);
                                // Rafraîchir la table du personnel
                                $('#personnel').DataTable().ajax.reload(null, false);

                                //table.ajax.reload();
                            } else {
                                alert(`Erreur lors de la mise à jour de l'intervention: ` + response.message);
                            }
                        },
                        error: function (xhr, status, error) {
                            console.error("Erreur AJAX:", xhr.responseText);
                            alert('Erreur lors de la communication avec le serveur: ' + error);
                        }
                    });
                    $(this).dialog("close");
                },
                "Annuler": function () {
                    $(this).dialog("close");
                }
            }
        });
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


});


