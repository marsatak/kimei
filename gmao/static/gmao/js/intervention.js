$(document).ready(function () {
    //let gauge;


    /*function initGauge() {
        if (typeof interventionData === 'undefined') {
            console.error('interventionData is not defined');
            return;
        }
        gauge = new JustGage({
            id: "gauge-container",
            value: interventionData.duree_intervention,
            min: 0,
            max: interventionData.duree_prevue,
            title: "Temps passé",
            label: "secondes",
            gaugeWidthScale: 0.6,
            counter: true
        });
    }*/

    function updateProgressBar(state) {
        var progressBar = document.querySelector('.progress-bar-fill');
        console.log("Updating progress bar to state:", state, "Element found:", progressBar);
        if (!progressBar) {
            console.error("Progress bar element not found.");
            return;
        }
        switch (state) {
            case 'debut':
                progressBar.style.height = '0%';
                break;
            case 'travail':
                progressBar.style.height = '50%';
                break;
            case 'fin':
                progressBar.style.height = '100%';
                break;
            default:
                progressBar.style.height = '0%';
        }
    }

    const etatIntervention = 'travail'; // Exemple : 'debut', 'travail', 'fin'
    updateProgressBar(etatIntervention);

    /*function updateGauge() {
        if (!gauge || typeof interventionData === 'undefined') {
            return;
        }
        var currentTime = new Date();
        var startTime = interventionData.top_debut && interventionData.top_debut !== 'null' ? new Date(interventionData.top_debut) : currentTime;
        var duration = Math.floor((currentTime - startTime) / 60000); // durée en minutes
        gauge.refresh(Math.min(duration, interventionData.duree_prevue));
    }*/

    if (typeof interventionData !== 'undefined') {
        //initGauge();
        //console.log(etatIntervention)
        //updateProgressBar(etatIntervention);
        //setInterval(updateGauge, 60000);
    } else {
        console.error('interventionData is not defined');
    }

    function commencerIntervention(interventionId) {
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
        console.log("Loading elements for station:", stationId);
        const currentElement = $("#element").val();
        console.log("Current element:", currentElement);

        $.ajax({
            url: '/home/load-elements/',
            data: {'station': stationId},
            dataType: 'json',
            success: function (data) {
                console.log(JSON.stringify(data, null, 2));
                console.log("Received elements data:", data);
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

                console.log("Select options:", elementSelect.find('option').length);
                console.log("Select value:", elementSelect.val());
            },
            error: function (xhr, status, error) {
                console.error("Erreur lors du chargement des éléments:", error);
            }
        });
    }

    $('#commencer-travail').on('click', function () {
        console.log('travail')
        const interventionId = $(this).data('intervention-id');
        commencerIntervention(interventionId);
    });

    $('#terminer-travail').on('click', function () {

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
        console.log("annuler")
        annulerIntervention($(this).data('intervention-id'));
    });
    $('#numero_fiche').on('input', function (e) {
        // Remplace tout ce qui n'est pas un chiffre par une chaîne vide
        this.value = this.value.replace(/[^0-9]/g, '');

        // Limite la longueur à 5 chiffres
        if (this.value.length > 5) {
            this.value = this.value.slice(0, 5);
        }
    });
    $('#interventionForm').submit(function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const interventionId = $('#interventionFormModal').data('intervention-id');
        const numeroFiche = $('#numero_fiche').val()
        if (!/^\d{5}$/.test(numeroFiche)) {
            alert("Le numéro de fiche doit contenir exactement 5 chiffres.");
            e.preventDefault();
            return false;
        }
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
                    window.location.reload();
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
    let flatpickrInstance;

    $('#interventionFormModal').on('show.bs.modal', function () {
        if (flatpickrInstance) {
            flatpickrInstance.destroy();
        }

        flatpickrInstance = flatpickr("#heure_fin", {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",
            time_24hr: true,
            defaultDate: new Date(),  // Utilise la date et l'heure courantes
            onReady: function (selectedDates, dateStr, instance) {
                console.log("Flatpickr initialized with:", dateStr);  // Pour le débogage
            }
        });
    });

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