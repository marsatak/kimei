document.addEventListener('DOMContentLoaded', function () {
    var navbarToggler = document.querySelector('.navbar-toggler');
    var equipmentsDropdown = document.getElementById('equipmentsDropdown');
    var navbarCollapse = document.getElementById('navbarNav');

    function toggleEquipmentsDropdown() {
        if (window.innerWidth <= 991) { // Si en mode mobile
            equipmentsDropdown.classList.add('show');
        } else {
            equipmentsDropdown.classList.remove('show');
        }
    }

    // Développer le dropdown "Équipements" par défaut en mode mobile
    toggleEquipmentsDropdown();

    // Ajuster lorsque la fenêtre est redimensionnée
    window.addEventListener('resize', toggleEquipmentsDropdown);

    // Assurer la fermeture des autres dropdowns lorsqu'on clique en dehors
    document.addEventListener('click', function (event) {
        var isClickInside = navbarCollapse.contains(event.target);
        if (!isClickInside) {
            document.querySelectorAll('.dropdown-menu.show').forEach(function (openDropdown) {
                openDropdown.classList.remove('show');
            });
        }
    });

    // Assurer la fermeture des autres dropdowns lorsqu'on utilise le bouton hamburger
    navbarToggler.addEventListener('click', function () {
        setTimeout(function () {
            document.querySelectorAll('.dropdown-menu.show').forEach(function (openDropdown) {
                openDropdown.classList.remove('show');
            });
            toggleEquipmentsDropdown(); // Re-développer le dropdown "Équipements" si en mode mobile
        }, 300);
    });
});
