let interventionEncours = false;
$(document).ready(function () {

    function initPortfolioTable(data, interventionEnCours) {
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
                            return getActionButton(row, interventionEnCours);
                        }
                    }
                ],
                responsive: true,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                order: [[0, 'asc']],
                drawCallback: function (settings) {
                    if (interventionEnCours) {
                        $('.prendre-en-charge').prop('disabled', true);
                    }
                }
            });
        }
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

    function loadTechnicienPortfolio() {
        $.ajax({
            url: '/get-technicien-portfolio/',
            type: 'GET',
            success: function (response) {
                if (response.success) {
                    interventionEncours = response.intervention_en_cours;
                    initPortfolioTable(response.doleances, interventionEncours);
                    /*if (response.intervantion_en_cours) {
                        $('.prendre-en-charge').prop('disabled', true);
                    }*/
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

    function prendreEnCharge(doleanceId) {
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
    }


    loadTechnicienPortfolio();
});