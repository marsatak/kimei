console.log('teams')
$(document).ready(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const upperCaseInputs = document.querySelectorAll('input[type="text"], textarea');
        upperCaseInputs.forEach(input => {
            input.addEventListener('input', function () {
                this.value = this.value.toUpperCase();
            });
        });
    });

    function initPortfolioTable(data) {
        if ($('#portfolioContainer').length) {
            if ($.fn.DataTable.isDataTable('#portfolioTable')) {
                $('#portfolioTable').DataTable().destroy();
            }
            let tableHtml = '<table id="portfolioTable" class="table table-striped">';
            tableHtml += '<thead><tr><th>NDI</th><th>Station</th><th>Élément</th><th>Panne</th><th>Statut</th><th>Actions</th></tr></thead><tbody>';
            const activeDoleances = data.filter(doleance => doleance.statut !== 'TER');

            activeDoleances.forEach(function (doleance) {
                tableHtml += `<tr>
                    <td>${doleance.ndi}</td>
                    <td>${doleance.station}</td>
                    <td>${doleance.element}</td>
                    <td>${doleance.panne_declarer}</td>
                    <td>${doleance.statut}</td>
                    <td>
                        ${doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP' ?
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
                    console.log("Technicien sans équipe ou autre situation:", response.message);
                    $('#portfolioContainer').html('<p>Aucune doléance disponible. Veuillez contacter votre administrateur si vous pensez qu\'il s\'agit d\'une erreur.</p>');
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", error);
                $('#portfolioContainer').html('<p>Une erreur est survenue lors du chargement des données. Veuillez réessayer plus tard.</p>');
            }
        });
    }

    function prendreEnCharge(doleanceId) {
        $.ajax({
            url: `/home/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    $(`.prendre-en-charge[data-id="${doleanceId}"]`).fadeOut();
                    loadTechnicienPortfolio();
                    window.location.href = response.redirect_url;
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