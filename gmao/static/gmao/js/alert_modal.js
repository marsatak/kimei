// Pour un prompt texte
showDynamicModal({
    title: "Saisie du nom",
    inputType: "text",
    inputId: "nomInput",
    placeholder: "Entrez votre nom",
    confirmButtonText: "Valider",
    onConfirm: function (nom) {
        // Traitement avec le nom saisi
    }
});

// Pour un prompt numérique
showDynamicModal({
    title: "Saisie de l'âge",
    inputType: "number",
    inputId: "ageInput",
    placeholder: "Entrez votre âge",
    confirmButtonText: "Confirmer",
    onConfirm: function (age) {
        // Traitement avec l'âge saisi
    }
});