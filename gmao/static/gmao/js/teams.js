$(document).ready(function () {
    function initPortfolioTable(data) {
        const portfolioContainer = $('#portfolioContainer');
        portfolioContainer.empty();

        if (data.length === 0) {
            portfolioContainer.append('<p>Aucune doléance dans votre portfolio.</p>');
            return;
        }

        const table = $('<table id="portfolioTable" class="table table-striped">').appendTo(portfolioContainer);
        const thead = $('<thead>').appendTo(table);
        const tbody = $('<tbody>').appendTo(table);

        thead.append(`
            <tr>
                <th>NDI</th>
                <th>Station</th>
                <th>Élément</th>
                <th>Panne déclarée</th>
                <th>Statut</th>
                <th>Action</th>
            </tr>
        `);

        data.forEach(doleance => {
            const tr = $('<tr>').appendTo(tbody);
            tr.append(`
                <td>${doleance.ndi}</td>
                <td>${doleance.station}</td>
                <td>${doleance.element}</td>
                <td>${doleance.panne_declarer}</td>
                <td>${doleance.statut}</td>
                <td>${getActionButton(doleance)}</td>
            `);
        });

        $('#portfolioTable').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            }
        });
    }

    function getActionButton(doleance) {
        if (doleance.statut === 'ATT' && doleance.intervention_id) {
            return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm">Détails intervention</a>`;
        } else if (doleance.statut === 'NEW' || doleance.statut === 'ATP' || doleance.statut === 'ATD') {
            return `<button class="btn btn-success btn-sm prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
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

    function prendreEnCharge(doleanceId) {
        $.ajax({
            url: `/home/prendre-en-charge/${doleanceId}/`,
            type: 'POST',
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert(response.message);
                    if (response.redirect_url) {
                        window.location.href = response.redirect_url;
                    } else {
                        loadTechnicienPortfolio();
                    }
                } else {
                    alert('Erreur : ' + response.message);
                }
            },
            error: function () {
                alert('Erreur de communication avec le serveur');
            }
        });
    }

    $(document).on('click', '.prendre-en-charge', function (e) {
        e.preventDefault();
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