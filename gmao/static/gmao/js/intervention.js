import {showDynamicModal} from './modal.js';

$(document).ready(function () {

    /*function commencerIntervention(interventionId) {
        console.log("Début de commencerIntervention", interventionId);
        let kilometrage = prompt("Veuillez entrer le kilométrage de départ (chiffres uniquement):");
        if (kilometrage === null) return; // L'utilisateur a annulé

        kilometrage = kilometrage.replace(/[^0-9]/g, '');  // Supprime tous les caractères non numériques
        if (kilometrage === '') {
            showNotification("Veuillez entrer un kilométrage valide.", 'error');
            return;
        }

        $.ajax({
            url: '/home/commencer-intervention/' + interventionId + '/',
            type: 'POST',
            data: {
                kilometrage: kilometrage,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    $('#top_debut').text(new Date(response.top_debut).toLocaleString(
                        'fr-FR', {
                            day: '2-digit', month: '2-digit', year: 'numeric',
                            hour: '2-digit', minute: '2-digit'
                        }));
                    $('.progress-bar').removeClass('bg-info').addClass('bg-warning')
                        .css('width', '66%')
                        .attr('aria-valuenow', 66)
                        .text('En cours');
                    $('.commencer-intervention').hide();
                    window.location.reload();
                } else {
                    showNotification('Erreur lors du démarrage de l\'intervention: ' + response.message, 'error');
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                showNotification('Erreur lors de la communication avec le serveur: ' + error, 'error');
            }
        });
    }*/
    function commencerIntervention(interventionId) {
        console.log("Début de commencerIntervention", interventionId);

        showDynamicModal({
            title: "Saisie du kilométrage",
            inputType: "number",
            inputId: "kilometrageInput",
            placeholder: "Entrez le kilométrage de départ",
            confirmButtonText: "Confirmer",
            onConfirm: function (kilometrage) {
                if (kilometrage === '') {
                    showNotification("Veuillez entrer un kilométrage valide.", 'error');
                    return;
                }

                $.ajax({
                    url: '/home/commencer-intervention/' + interventionId + '/',
                    type: 'POST',
                    data: {
                        kilometrage: kilometrage,
                        csrfmiddlewaretoken: getCookie('csrftoken')
                    },
                    headers: {'X-CSRFToken': getCookie('csrftoken')},
                    success: function (response) {
                        if (response.success) {
                            $('#top_debut').text(new Date(response.top_debut).toLocaleString(
                                'fr-FR', {
                                    day: '2-digit', month: '2-digit', year: 'numeric',
                                    hour: '2-digit', minute: '2-digit'
                                }));
                            $('.progress-bar').removeClass('bg-info').addClass('bg-warning')
                                .css('width', '66%')
                                .attr('aria-valuenow', 66)
                                .text('En cours');
                            $('.commencer-intervention').hide();
                            window.location.reload();
                        } else {
                            showNotification('Erreur lors du démarrage de l\'intervention: ' + response.message, 'error');
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("Erreur AJAX:", xhr.responseText);
                        showNotification('Erreur lors de la communication avec le serveur: ' + error, 'error');
                    }
                });
            }
        });
    }

    function annulerIntervention(interventionId) {
        if (confirm("Êtes-vous sûr de vouloir annuler cette intervention ?")) {
            $.ajax({
                url: `/home/intervention/${interventionId}/annuler/`,
                type: 'POST',
                data: {
                    csrfmiddlewaretoken: getCookie('csrftoken')
                },
                success: function (response) {
                    if (response.success) {
                        alert('Intervention annulée avec succès.');
                        window.location.href = '/home/';

                    } else {
                        alert('Erreur lors de l\'annulation de l\'intervention: ' + response.message);
                    }
                },
                error: function (xhr, status, error) {
                    console.error("Erreur AJAX:", xhr.responseText);
                    alert('Erreur lors de la communication avec le serveur: ' + error);
                }
            });
        }
    }


    function loadElements(stationId) {
        //("Loading elements for station:", stationId);
        const currentElement = $("#element").val();
        //console.log("Current element:", currentElement);

        $.ajax({
            url: '/home/load-elements/',
            data: {'station': stationId},
            dataType: 'json',
            success: function (data) {
                //console.log(JSON.stringify(data, null, 2));
                //console.log("Received elements data:", data);
                const elementSelect = $('#element');
                elementSelect.empty();

                // Ajouter l'option actuelle
                elementSelect.append($('<option>', {
                    value: currentElement,
                    text: currentElement
                }));

                $.each(data, function (category, elements) {
                    const optgroup = $('<optgroup label="Elem">').attr('label', category);
                    $.each(elements, function (key, value) {
                        let displayText, optionValue;
                        if (typeof value === 'string') {
                            displayText = value.split(',').pop().trim();
                            optionValue = key;
                        } else if (Array.isArray(value)) {
                            displayText = value[1];
                            optionValue = value[0];
                        } else {
                            console.error("Unexpected data format for element:", value);
                            return;
                        }

                        if (optionValue !== currentElement) {
                            optgroup.append($('<option>', {
                                value: optionValue,
                                text: displayText
                            }));
                        }
                    });
                    if (optgroup.children().length > 0) {
                        elementSelect.append(optgroup);
                    }
                });

                elementSelect.val(currentElement);

                //console.log("Select options:", elementSelect.find('option').length);
                //console.log("Select value:", elementSelect.val());
            },
            error: function (xhr, status, error) {
                console.error("Erreur lors du chargement des éléments:", error);
            }
        });
    }

    $('#commencer-travail').on('click', function () {
        //console.log('travail')
        const interventionId = $(this).data('intervention-id');
        commencerIntervention(interventionId);
    });

    $('#terminer-travail , #modifier-intervention').on('click', function () {

        const interventionId = $(this).data('intervention-id');
        const stationId = interventionData ? interventionData.station_id : null;
        if (stationId) {
            $('#interventionFormModal').data('intervention-id', interventionId).modal('show');
            loadElements(stationId);
        } else {
            console.error('Station ID is not available');
        }

    });

    $('#annuler-intervention').click(function (e) {
        e.preventDefault();
        //console.log("annuler")
        annulerIntervention($(this).data('intervention-id'));
    });
    $('#numero_fiche').on('input', function (e) {
        // Remplace tout ce qui n'est pas un chiffre par une chaîne vide
        this.value = this.value.replace(/[^0-9]/g, '');

        // Limite la longueur à 5 chiffres
        if (this.value.length > 7) {
            this.value = this.value.slice(0, 7);
        }
    });

    /* INTERVENTIONFORM POUR ADMIN */

    function capitalizeSentences(string) {
        return string.replace(/(^\s*\w|[.!?]\s*\w)/g, function (c) {
            return c.toUpperCase();
        });
    }


    $('#interventionForm input[type="text"], #interventionForm textarea').on('blur', function () {
        //console.log("Capitalizing sentences for:", this.value);
        this.value = capitalizeSentences(this.value);
    });
    $('#interventionForm').submit(function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const interventionId = $('#interventionFormModal').data('intervention-id');
        const numeroFiche = $('#numero_fiche').val()
        if (!/^\d{7}$/.test(numeroFiche)) {
            alert("Le numéro de fiche doit contenir exactement 7 chiffres.");
            e.preventDefault();
            return false;
        }
        // Calculer la durée de l'intervention
        const endTime = new Date();
        const duration = calculateDuration(interventionStartTime, endTime);
        formData.append('duree_intervention', duration);
        $.ajax({
            url: '/home/intervention/' + interventionId + '/terminer/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            success: function (response) {
                if (response.success) {
                    alert('Intervention terminée avec succès.');
                    window.location.href = '/home/';
                } else {
                    alert('Erreur lors de la terminaison de l\'intervention: ' + response.message);
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX:", xhr.responseText);
                alert('Erreur lors de la communication avec le serveur: ' + error);
            }
        });
    });
    let flatpickrDate;
    let flatpickrDebut;
    let flatpickrFin;
    let interventionStartTime;
    $('#interventionFormModal').on('show.bs.modal', function () {
        if (flatpickrDebut || flatpickrFin || flatpickrDate) {
            flatpickrDate.destroy();
            flatpickrDebut.destroy();
            flatpickrFin.destroy();
        }

        flatpickrDate = flatpickr("#date", {
            allowInput: true,
            enableCalendar: true,
            dateFormat: "d/m/yy",
            time_24hr: true,
            onReady: function (selectedDates, dateStr, instance) {
                //console.log("Flatpickr initialized with:", dateStr);  // Pour le débogage
            }
        });

        flatpickrDebut = flatpickr("#heure_debut", {
            allowInput: true,
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",
            time_24hr: true,
            onReady: function (selectedDates, dateStr, instance) {
                //console.log("Flatpickr initialized with:", dateStr);  // Pour le débogage
            }
        });

        flatpickrFin = flatpickr("#heure_fin", {
            allowInput: true,
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",
            time_24hr: true,
            defaultDate: new Date(),  // Utilise la date et l'heure courantes
            onReady: function (selectedDates, dateStr, instance) {
                //console.log("Flatpickr initialized with:", dateStr);  // Pour le débogage
            }
        });
        const now = new Date();
        const currentTime = now.getHours().toString().padStart(2, '0') + ':' +
            now.getMinutes().toString().padStart(2, '0');

        // Définir l'heure de fin comme l'heure actuelle
        $('#heure_fin').val(currentTime);

    });

    function calculateDuration(start, end) {
        const diff = end - start; // différence en millisecondes
        const hours = Math.floor(diff / 3600000);
        const minutes = Math.floor((diff % 3600000) / 60000);
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});