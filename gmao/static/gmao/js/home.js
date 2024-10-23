$(document).ready(function () {
    // INITIALISATION DES VARIABLES
    let doleanceTable, personnelTable;
    // VEROUILLAGE MAJUSCULE ET AUTRES

    document.addEventListener('DOMContentLoaded', function () {
        const upperCaseInputs = document.querySelectorAll('input[type="text"], textarea');
        upperCaseInputs.forEach(input => {
            input.addEventListener('input', function () {
                this.value = this.value.toUpperCase();
            });
        });
    });
    p

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
    $(window).resize(function () {
        if (doleanceTable) doleanceTable.columns.adjust().draw();
        if (personnelTable) personnelTable.columns.adjust().draw();
        $('#demandeencours').DataTable().draw();
        $('#personnel').DataTable().draw();
    });
    // FIN FONCTIONS DE MISE EN PAGE

    // AFFICHAGE DOLÉANCES EN COURS ET STATUTS
    function initDoleanceTable() {
        if ($('#demandeencours').length && !$.fn.DataTable.isDataTable('#demandeencours')) {
            doleanceTable = $('#demandeencours').DataTable({
                ajax: {
                    url: "/home/getDoleanceEncours",
                    dataSrc: ""
                },
                columns: [
                    {data: "ndi", width: "5%%"},
                    {
                        data: "date_transmission", width: "8%",
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: "statut", width: "3%"},
                    {
                        data: "station.libelle_station", width: "10%",
                        render: function (data, type, row) {
                            if (type === 'display' && data != null && data.length > 15) {
                                return `<span title="${data}">${data.substr(0, 15)}...</span>`;
                            }
                            return data;
                        }
                    },
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
                            let actions = '';
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                actions += '<button class="btn btn-primary btn-sm declencher-intervention mr-1" data-id="' + row.id + '">' +
                                    '<i class="fas fa-arrow-alt-circle-up"></i>' +
                                    '</button>';
                            }
                            actions += '<button class="btn btn-warning btn-sm update-doleance mr-1 mx-1" data-id="' + row.id + '">' +
                                '<i class="fas fa-edit"></i>' +
                                '</button>';
                            return actions;
                        }
                    },
                ],
                responsive: {
                    details: {
                        display: $.fn.dataTable.Responsive.display.childRowImmediate,
                        type: 'none',
                        target: ''
                    }
                },
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
                    {responsivePriority: 1, targets: 0}, // NDI
                    {responsivePriority: 2, targets: 3},
                    {responsivePriority: 3, targets: 5}, // Panne déclarée
                    {responsivePriority: 4, targets: 8},
                    {responsivePriority: 5, targets: 1},
                    {responsivePriority: 10000, targets: [2, 4, 6, 7]}
                ]
            });
        }
    }

    // FIN AFFICHAGE DOLÉANCES EN COURS ET STATUTS
    // AFFICHAGE EQUIPES ET LEURS DOLEANCES
    function loadEquipesData() {
        $.ajax({
            url: '/home/get-equipes-data/',
            type: 'GET',
            success: function (data) {
                updateEquipesSection(data);
            },
            error: function (xhr, status, error) {
                console.error("Erreur lors du chargement des données des équipes:", error);
            }
        });
    }

    function updateEquipesSection(equipes_data) {
        let html = '';
        equipes_data.forEach(function (equipe) {
            html += `
            <div class="col-md-4 mb-4">
                <div class="card h-100" style="width: 90%;">
                    <a href="/equipes/gestion-equipes">
                        <div class="card-header bg-primary text-white">
                            <h5 class="card-title mb-0">${equipe.nom}</h5>
                        </div>
                    </a>
                    <div class="card-body">
                        ${equipe.description}
                        <h6 class="mt-3">Techniciens :</h6>
                        <ul>
                            ${equipe.techniciens.slice(0, 3).map(tech => `
                                <li>${tech.prenom} ${tech.nom} 
                                    <span class="badge bg-${tech.statut === 'PRS' ? 'success' : tech.statut === 'ABS' ? 'danger' : 'warning'} float-end">
                                        ${tech.statut}
                                    </span>
                                </li>
                            `).join('')}
                        </ul>
                        ${equipe.techniciens.length > 3 ? `<p>Et ${equipe.techniciens.length - 3} autres...</p>` : ''}
                        <h6 class="mt-3">Doléances actives :</h6>
                        <ul>
                            ${equipe.doleances.slice(0, 5).map(dol => `
                                <li>${dol.ndi} - ${dol.station.substring(0, 20)} - ${dol.panne_declarer.substring(0, 50)}
                                    <span class="badge bg-${getBadgeClass(dol.statut)} float-end">${dol.statut}</span>
                                </li>
                            `).join('')}
                        </ul>
                        ${equipe.doleances.length > 5 ? `<p>Et ${equipe.doleances.length - 5} autres...</p>` : ''}
                    </div>
                    <div class="card-footer">
                        <a href="/gmao_teams/get_equipe_details/${equipe.id}/" class="btn btn-primary btn-sm">Détails de l'équipe</a>
                    </div>
                </div>
            </div>
        `;
        });
        $('#equipes-section .row').html(html);
    }

    function getBadgeClass(statut) {
        const statusClasses = {
            'NEW': 'primary',
            'ATT': 'warning',
            'INT': 'info',
            'ATP': 'danger',
            'ATD': 'secondary'
        };
        return statusClasses[statut] || 'light';
    }

    if ($('#equipes-section').length) {
        loadEquipesData();
        setInterval(loadEquipesData, 60000);  // Rafraîchir toutes les 60 secondes
    }

    // FIN AFFICHAGE EQUIPES ET LEURS DOLEANCES


    // ATTRIBUTION DOLEANCES POUR TECHNICIENS
    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
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

    // FIN ATTRIBUTION DOLEANCES POUR TECHNICIENS

    // AFFICHAGE EMPLOYEES ET STATUTS
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

    // MISE A JOUR DES DONNEES DES EQUIPES ET DOLÉANCES

    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        initDoleanceTable();
        initPersonnelTable();
        setInterval(refreshDoleanceTable, 60000);
        setInterval(refreshPersonnelTable, 60000);
    } else if ($('#portfolioContainer').length) {
        loadTechnicienPortfolio();
    }

    //  REFRESH SUR LES DOLEANCES
    function refreshDoleanceTable() {
        console.log("Refreshing doleanceTable");
        if (doleanceTable) {
            doleanceTable.ajax.reload(null, false);
        } else {
            console.log("doleanceTable is not defined try initialize...");
            initDoleanceTable()
        }
    }

    // ACTIONS SUR LES EMPLOYEES
    function refreshPersonnelTable() {
        if (personnelTable) {
            personnelTable.ajax.reload(null, false);
        } else {
            initPersonnelTable()
        }
    }

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

    // FIN DES ACTIONS SUR LES EMPLOYEES

    // ACTION POUR LES TECHNICIENS ET LES DOLEANCES
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

    // FIN ACTION POUR LES TECHNICIENS ET LES DOLEANCES

    function formatInterventions(data, rowData) {
        if (!data.interventions || data.interventions.length === 0) {
            return '<p>Aucune intervention pour cette doléance.</p>';
        }

        let html = '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">';
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


    // SAISIE DE LA FICHE D'INTERVENTION
    /*$('#interventionForm').submit(function (e) {
        e.preventDefault();

        const formData = new FormData(this);
        const interventionId = $('#intervention-id-input').val();
        $(this).prop('disabled', true);
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
            },
            complete: function () {
                // Réactiver le bouton après la soumission
                $('#submitDoleance').prop('disabled', false);
            }
        });
    });*/
    // FIN SAISIE DE LA FICHE D'INTERVENTION


});

// COOKIES ET CSRF
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

// FIN COOKIES ET CSRF


// AFFICHAGE INTERVENTION EN COURS (STAND BY)
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

// FIN AFFICHAGE INTERVENTION EN COURS (STAND BY)