$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            }
        }
    });
    let currentEquipeId = null;

    loadEquipes();

    $('#creerEquipe').click(function () {
        $('#creerEquipeModal').modal('show');
    });

    $('#saveEquipe').click(function () {
        let formData = $('#creerEquipeForm').serialize();
        $.ajax({
            url: CREER_EQUIPE_URL,
            type: 'POST',
            data: formData,
            headers: {'X-CSRFToken': getCSRFToken()},
            success: function (data) {
                if (data.success) {
                    $('#creerEquipeModal').modal('hide');
                    loadEquipes();
                }
            }
        });
    });


    function loadEquipes() {
        $.get(LISTE_EQUIPES_URL, function (data) {
            let html = '<ul>';
            data.equipes.forEach(function (equipe) {
                html += '<li><a href="#" class="equipe-link" data-id="' + equipe.id + '">' + equipe.nom + '</a></li>';
            });
            html += '</ul>';
            $('#listeEquipes').html(html);
        });
    }

    $(document).on('click', '.equipe-link', function () {
        currentEquipeId = $(this).data('id');
        loadEquipeDetails(currentEquipeId);
    });

    function loadEquipeDetails(equipeId) {
        $.get(GET_EQUIPE_DETAILS_URL.replace('0', equipeId), function (data) {
            $('#equipeNom').text(data.nom);
            $('#equipeDescription').text(data.description);

            updateTechniciensList(data.techniciens, '#listeTechniciens');
            updateDoleancesList(data.doleances, '#listeDoléances');

            loadTechniciensDisponibles();
            loadDoleancesNonAttribuees();

            $('#detailsEquipe').show();
        });
    }

    function updateTechniciensList(techniciens, listId) {
        let html = '';
        techniciens.forEach(function (tech) {
            html += `
        <li class="list-group-item">
            ${tech.nom_personnel} ${tech.prenom_personnel}
            <button class="btn btn-sm btn-danger retirer-technicien float-right" data-id="${tech.id}">Retirer</button>
        </li>`;
        });
        $(listId).html(html);
    }

    function updateDoleancesList(doleances, listId) {
        let html = '';
        doleances.forEach(function (doleance) {
            html += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>${doleance.ndi} - ${doleance.panne_declarer}</span>
                <button class="btn btn-sm btn-danger retirer-doleance" data-id="${doleance.id}">Retirer</button>
            </li>`;
        });
        $(listId).html(html);
    }

    function loadTechniciensDisponibles() {
        $.get(GET_TECHNICIENS_DISPONIBLES_URL, function (data) {
            let html = '';
            data.techniciens.forEach(function (tech) {
                html += `
            <li class="list-group-item">
                ${tech.nom_personnel} ${tech.prenom_personnel}
                <button class="btn btn-sm btn-success affecter-technicien float-right" data-id="${tech.id}">Affecter</button>
            </li>`;
            });
            $('#listeTechniciensDisponibles').html(html);
        });
    }


    function loadDoleancesNonAttribuees() {
        let searchQuery = $('#searchDoleances').val();
        $.get(GET_DOLEANCES_NON_ATTRIBUEES_URL + '?search=' + searchQuery, function (data) {
            let html = '';
            data.doleances.forEach(function (doleance) {
                html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <span>${doleance.ndi} - ${doleance.station__libelle_station} - ${doleance.panne_declarer}</span>
                    <button class="btn btn-sm btn-success attribuer-doleance" data-id="${doleance.id}">Attribuer</button>
                </li>`;
            });
            $('#listeDoléancesNonAttribuées').html(html);
        });
    }

// Ajouter un gestionnaire d'événements pour la recherche
    $('#searchDoleances').on('input', function () {
        loadDoleancesNonAttribuees();
    });

    $(document).on('click', '.affecter-technicien', function (e) {
        e.preventDefault();
        let technicienId = $(this).data('id');
        console.log("Tentative d'affectation du technicien:", technicienId, "à l'équipe:", currentEquipeId);

        $.ajax({
            url: AFFECTER_TECHNICIEN_URL.replace('0', currentEquipeId),
            type: 'POST',
            data: {technicien: technicienId},
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            success: function (data) {
                console.log("Réponse reçue:", data);
                if (data.success) {
                    console.log("Affectation réussie");
                    loadEquipeDetails(currentEquipeId);
                } else {
                    console.error("Erreur d'affectation:", data.error || "Erreur inconnue");
                    alert("Une erreur est survenue lors de l'affectation du technicien: " + (data.error || "Erreur inconnue"));
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Erreur AJAX lors de l'affectation du technicien:", textStatus, errorThrown);
                console.log("Réponse complète:", jqXHR.responseText);
                alert("Une erreur est survenue lors de l'affectation du technicien. Veuillez vérifier la console pour plus de détails.");
            }
        });
    });

    $(document).on('click', '.attribuer-doleance', function () {
        let doleanceId = $(this).data('id');
        $.post(ATTRIBUER_DOLEANCE_URL.replace('0', currentEquipeId),
            {doleance: doleanceId},
            function (data) {
                if (data.success) {
                    loadEquipeDetails(currentEquipeId);
                }
            });
    });

    $(document).on('click', '.retirer-technicien', function () {
        let technicienId = $(this).data('id');
        $.post(RETIRER_TECHNICIEN_URL.replace('0', currentEquipeId),
            {technicien: technicienId},
            function (data) {
                if (data.success) {
                    loadEquipeDetails(currentEquipeId);
                }
            });
    });

    $(document).on('click', '.retirer-doleance', function () {
        let doleanceId = $(this).data('id');
        $.post(RETIRER_DOLEANCE_URL.replace('0', currentEquipeId),
            {doleance: doleanceId},
            function (data) {
                if (data.success) {
                    loadEquipeDetails(currentEquipeId);
                }
            });
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