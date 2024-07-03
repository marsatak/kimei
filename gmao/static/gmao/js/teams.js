console.log('teams')
$(document).ready(function () {
    function initPortfolioTable(data) {
        if ($('#portfolioContainer').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }
            let tableHtml = '<table id="portfolioTable" class="table table-striped">';
            tableHtml += '<thead><tr><th>NDI</th><th>Station</th><th>Élément</th><th>Panne</th><th>Statut</th><th>Actions</th></tr></thead><tbody>';

            data.forEach(function (doleance) {
                tableHtml += `<tr>
                        <td>${doleance.ndi}</td>
                        <td>${doleance.station}</td>
                        <td>${doleance.element}</td>
                        <td>${doleance.panne_declarer}</td>
                        <td>${doleance.statut}</td>
                        <td>
                            ${doleance.statut === 'NEW' || doleance.statut === 'ATT' ?
                    `<button class="btn btn-primary btn-sm prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>` :
                    ''}
                        </td>
                    </tr>`;
            });

            tableHtml += '</tbody></table>';
            $('#portfolioContainer').html(tableHtml);

            portfolioTable = $('#portfolioTable').DataTable({
                responsive: true,
                language: {
                    // url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                }
            });
        }
    }


    function loadTechnicienPortfolio() {
        console.log("Chargement du portefeuille du technicien...");
        $.ajax({
            url: '/get-technicien-portfolio/',
            type: 'GET',
            success: function (response) {
                console.log("Réponse reçue:", response);
                if (response.success) {
                    if (response.doleances && response.doleances.length > 0) {
                        console.log("Initialisation du tableau avec", response.doleances.length, "doléances");
                        initPortfolioTable(response.doleances);
                    } else {
                        console.log("Aucune doléance trouvée");
                        $('#portfolioContainer').html('<p>Aucune doléance attribuée pour le moment.</p>');
                    }
                } else {
                    console.error("Erreur lors du chargement du portefeuille:", response.message);
                    alert('Erreur lors du chargement du portefeuille : ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", error);
                alert('Erreur de communication avec le serveur');
            }
        });
    }


    function refreshPortfolioTable() {
        if ($('#portfolioContainer').length) {
            loadTechnicienPortfolio();
        }
    }

    loadTechnicienPortfolio();

    function prendreEnCharge(doleanceId) {
        $.ajax({
            url: `/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert('Doléance prise en charge avec succès');
                    refreshDoleanceTable(); // On garde cet appel
                } else {
                    alert('Erreur : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }

    $('#portfolioContainer').on('click', '.prendre-en-charge', function () {
        console.log("Bouton 'prendre en charge' cliqué");
        const doleanceId = $(this).data('id');
        prendreEnCharge(doleanceId);
    });
});