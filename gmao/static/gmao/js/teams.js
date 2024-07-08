let interventionEncours = false;
$(document).ready(function () {

    function initPortfolioTable(data, interventionEnCoursGlobal) {
        if ($('#portfolioTable').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            $('#portfolioTable').DataTable({
                data: data,
                columns: [
                    {data: 'ndi', title: 'NDI'},
                    {data: 'station', title: 'Station'},
                    {data: 'element', title: 'Élément'},
                    {data: 'panne_declarer', title: 'Panne'},
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
                order: [[0, 'asc']],
                drawCallback: function (settings) {
                    console.log("DrawCallback - Intervention en cours (global):", interventionEnCoursGlobal);
                    $('.prendre-en-charge').prop('disabled', interventionEnCoursGlobal);
                }
            });
        }
    }

    function getActionButton(doleance, interventionEnCoursGlobal) {
        console.log("GetActionButton - Doléance:", doleance.id, "Intervention en cours (global):", interventionEnCoursGlobal);
        if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm btn-block">Détails intervention</a>`;
        } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP')) {
            return `<button class="btn btn-success btn-sm btn-block prendre-en-charge" data-id="${doleance.id}" ${interventionEnCoursGlobal ? 'disabled' : ''}>Prendre en charge</button>`;
        } else {
            return '<span class="text-muted">Aucune action disponible</span>';
        }
    }

    function loadTechnicienPortfolio() {
        $.ajax({
            url: '/get-technicien-portfolio/',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    interventionEnCours = response.intervention_en_cours;
                    console.log("Intervention en cours (global):", interventionEnCours);
                    initPortfolioTable(response.doleances, interventionEnCours);
                } else {
                    $('#portfolioContainer').html('<p>' + response.message + '</p>');
                }
            },
            error: function () {
                $('#portfolioContainer').html('<p>Erreur lors du chargement des données.</p>');
            }
        });
    }

    $(document).on('click', '.prendre-en-charge', function (e) {
        e.preventDefault();
        const doleanceId = $(this).data('id');
        prendreEnCharge(doleanceId);
    });

    /*function prendreEnCharge(doleanceId) {
        $.ajax({
            url: `/home/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    interventionEncours = response.intervention_en_cours;
                    console.log(interventionEncours)
                    $('.prendre-en-charge').prop('disabled', true);
                    loadTechnicienPortfolio();
                } else {
                    alert('Erreur : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }*/
    function prendreEnCharge(doleanceId) {
        $.ajax({
            url: `/home/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    interventionEnCours = true;
                    console.log("PrendreEnCharge - Nouvelle intervention en cours:", interventionEnCours);
                    loadTechnicienPortfolio();
                } else {
                    alert('Erreur : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }

    loadTechnicienPortfolio();
});