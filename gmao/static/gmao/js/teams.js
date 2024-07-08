$(document).ready(function () {

    /*function initPortfolioTable(data) {
        if ($('#portfolioTable').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            $('#portfolioTable').DataTable({
                data: data,
                columns: [
                    {data: 'ndi'},
                    {data: 'station'},
                    {data: 'element'},
                    {data: 'panne_declarer'},
                    {data: 'statut'},
                    {
                        data: null,
                        render: function (data, type, row) {
                            return getActionButton(row);
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                order: [[0, 'asc']]
            });
        }
    }*/
    function initPortfolioTable(data) {
        if ($('#portfolioTable').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            $('#portfolioTable').DataTable({
                data: data,
                columns: [
                    {data: 'ndi'},
                    {data: 'station'},
                    {data: 'element'},
                    {data: 'panne_declarer'},
                    {data: 'statut'},
                    {
                        data: null,
                        render: function (data, type, row) {
                            return getActionButton(row);
                        },
                        className: 'action-cell'
                    }
                ],
                responsive: {
                    details: {
                        display: $.fn.dataTable.Responsive.display.childRowImmediate,
                        type: 'none',
                        target: ''
                    }
                },
                autoWidth: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {responsivePriority: 1, targets: 0},
                    {responsivePriority: 2, targets: -1},
                    {responsivePriority: 3, targets: 4}
                ],
                order: [[0, 'asc']]
            });
        }
    }

    /*function getActionButton(doleance, hasOngoingIntervention) {
        if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm w-100">Détails intervention</a>`;
        } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !hasOngoingIntervention) {
            return `<button class="btn btn-success btn-sm w-100 prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
        } else {
            return '<span class="text-muted">Aucune action disponible</span>';
        }
    }*/
    function getActionButton(doleance) {
        if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm btn-block">Détails intervention</a>`;
        } else if (doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') {
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
                    initPortfolioTable(response.doleances);
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

    loadTechnicienPortfolio();
});