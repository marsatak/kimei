document.addEventListener('DOMContentLoaded', function () {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    // Fonction pour fermer le menu
    function closeMenu() {
        const bsCollapse = new bootstrap.Collapse(navbarCollapse, {toggle: false});
        bsCollapse.hide();
    }

    // Ferme le menu quand on clique en dehors
    document.addEventListener('click', function (event) {
        const isClickInside = navbarToggler.contains(event.target) || navbarCollapse.contains(event.target);
        console.log('click inside: ' + isClickInside);
        if (!isClickInside && navbarCollapse.classList.contains('show')) {
            closeMenu();
        }
    });

    // Ferme le menu quand on clique sur un lien (pour les appareils mobiles)
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            if (navbarCollapse.classList.contains('show')) {
                closeMenu();
            }
        });
    });

    // Gestion de l'événement de fermeture du menu
    navbarCollapse.addEventListener('hidden.bs.collapse', function () {
        document.body.classList.remove('menu-open');
    });

    // Gestion de l'événement d'ouverture du menu
    navbarCollapse.addEventListener('shown.bs.collapse', function () {
        document.body.classList.add('menu-open');
    });
});