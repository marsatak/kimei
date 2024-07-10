function refreshEquipesData() {
    $.ajax({
        url: '/get-equipes-data/',  // Créez cette nouvelle vue
        method: 'GET',
        success: function (data) {
            // Mettre à jour l'affichage avec les nouvelles données
            updateEquipesDisplay(data);
        },
        error: function (error) {
            console.error("Erreur lors du rafraîchissement des données:", error);
        }
    });
}

function updateEquipesDisplay(data) {
    // Logique pour mettre à jour l'affichage des équipes et de leurs doléances
    // ...
}

// Appelez cette fonction périodiquement ou après certaines actions
setInterval(refreshEquipesData, 60000);  // Rafraîchir toutes les minutes, par exemple