$(document).ready(function () {
    /*function initPortfolioTable(data) {
        if ($('#portfolioContainer').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            let tableHtml = '<div class="table-responsive">';
            tableHtml += '<table id="portfolioTable" class="table table-striped" style="width:100%">';
            tableHtml += '<thead><tr><th></th><th>NDI</th><th>Station</th><th>Élément</th><th>Panne</th><th>Statut</th><th>Actions</th></tr></thead><tbody>';

            const hasOngoingIntervention = data.some(doleance => doleance.statut === 'ATT' || doleance.statut === 'INT');

            data.forEach(function (doleance) {
                tableHtml += `<tr>
                    <td></td>
                    <td>${doleance.ndi}</td>
                    <td>${doleance.station}</td>
                    <td>${doleance.element}</td>
                    <td class="panne-cell">${doleance.panne_declarer}</td>
                    <td>${doleance.statut}</td>
                    <td class="action-cell">${getActionButton(doleance, hasOngoingIntervention)}</td>
                </tr>`;
            });

            tableHtml += '</tbody></table></div>';
            $('#portfolioContainer').html(tableHtml);

            $('#portfolioTable').DataTable({
                responsive: true,
                autoWidth: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {
                        className: 'control',
                        orderable: false,
                        targets: 0
                    },
                    {responsivePriority: 1, targets: 1}, // NDIZ
                    {responsivePriority: 2, targets: -1}, // Actions
                    {responsivePriority: 3, targets: 5}, // Statut
                    {width: "25%", targets: 4, className: 'panne-cell'}, // Panne
                    {width: "15%", targets: -1, className: 'action-cell'} // Actions
                ],
                /!*dom: 'Bfrtip',
                buttons: [
                    'copy', 'excel', 'pdf'
                ],*!/
                order: [[1, 'asc']]
            });
        }
    }*/
    function initPortfolioTable(data) {
        if ($('#portfolioContainer').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }

            let tableHtml = '<div class="table-responsive">';
            tableHtml += '<table id="portfolioTable" class="table table-striped table-bordered" style="width:100%">';
            tableHtml += '<thead><tr><th>NDI</th><th>Station</th><th>Élément</th><th>Panne</th><th>Statut</th><th>Actions</th></tr></thead><tbody>';

            data.forEach(function (doleance) {
                tableHtml += `<tr>
                <td>${doleance.ndi}</td>
                <td>${doleance.station}</td>
                <td>${doleance.element}</td>
                <td>${doleance.panne_declarer}</td>
                <td>${doleance.statut}</td>
                <td>${getActionButton(doleance)}</td>
            </tr>`;
            });

            tableHtml += '</tbody></table></div>';
            $('#portfolioContainer').html(tableHtml);

            $('#portfolioTable').DataTable({
                responsive: true,
                autoWidth: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {responsivePriority: 1, targets: 0}, // NDI
                    {responsivePriority: 2, targets: -1}, // Actions
                    {responsivePriority: 3, targets: 4}, // Statut
                    {responsivePriority: 4, targets: 3}, // Panne
                ],
                order: [[0, 'asc']]
            });
        }
    }

    function getActionButton(doleance, hasOngoingIntervention) {
        if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm w-100">Détails intervention</a>`;
        } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !hasOngoingIntervention) {
            return `<button class="btn btn-success btn-sm w-100 prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
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