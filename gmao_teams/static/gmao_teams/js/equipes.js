$(document).ready(function () {
    let currentEquipeId = null;

    loadEquipes();

    $('#creerEquipe').click(function () {
        $('#creerEquipeModal').modal('show');
    });

    $('#saveEquipe').click(function () {
        let formData = $('#creerEquipeForm').serialize();
        $.post(CREER_EQUIPE_URL, formData, function (data) {
            if (data.success) {
                $('#creerEquipeModal').modal('hide');
                loadEquipes();
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
            html += '<li>' + tech.nom_personnel + ' ' + tech.prenom_personnel +
                ' <button class="btn btn-sm btn-danger retirer-technicien" data-id="' + tech.id + '">Retirer</button></li>';
        });
        $(listId).html(html);
    }

    function updateDoleancesList(doleances, listId) {
        let html = '';
        doleances.forEach(function (doleance) {
            html += '<li>' + doleance.ndi + ' - ' + doleance.panne_declarer +
                ' <button class="btn btn-sm btn-danger retirer-doleance" data-id="' + doleance.id + '">Retirer</button></li>';
        });
        $(listId).html(html);
    }

    function loadTechniciensDisponibles() {
        $.get(GET_TECHNICIENS_DISPONIBLES_URL, function (data) {
            let html = '';
            data.techniciens.forEach(function (tech) {
                html += '<li>' + tech.nom_personnel + ' ' + tech.prenom_personnel +
                    ' <button class="btn btn-sm btn-success affecter-technicien" data-id="' + tech.id + '">Affecter</button></li>';
            });
            $('#listeTechniciensDisponibles').html(html);
        });
    }

    function loadDoleancesNonAttribuees() {
        $.get(GET_DOLEANCES_NON_ATTRIBUEES_URL, function (data) {
            let html = '';
            data.doleances.forEach(function (doleance) {
                html += '<li>' + doleance.ndi + ' - ' + doleance.panne_declarer +
                    ' <button class="btn btn-sm btn-success attribuer-doleance" data-id="' + doleance.id + '">Attribuer</button></li>';
            });
            $('#listeDoléancesNonAttribuées').html(html);
        });
    }

    $(document).on('click', '.affecter-technicien', function () {
        let technicienId = $(this).data('id');
        $.post(AFFECTER_TECHNICIEN_URL.replace('0', currentEquipeId),
            {technicien: technicienId},
            function (data) {
                if (data.success) {
                    loadEquipeDetails(currentEquipeId);
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
});