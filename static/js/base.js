document.addEventListener('DOMContentLoaded', function () {
    var equipmentDropdown = document.getElementById('navbarDropdownEquipements');
    if (equipmentDropdown) {
        console.log("Dropdown trouvé, initialisation...");
        new bootstrap.Dropdown(equipmentDropdown);
    } else {
        console.log("Dropdown non trouvé");
    }
});