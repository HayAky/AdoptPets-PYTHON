document.addEventListener('DOMContentLoaded', () => {
    const headerUp = document.getElementById('headerup');

    // MODIFICACIÓN PRINCIPAL:
    // Intentamos buscar la barra de Admin, si no existe, buscamos la de Refugio
    const headSecondary = document.getElementById('headadmin') || document.getElementById('headrefugio');

    const root = document.documentElement;

    // Validación de seguridad:
    // Si la página no tiene doble header (ej. login o adoptante), el script se detiene para no causar errores.
    if (!headerUp || !headSecondary) return;

    // Variables para el scroll
    let lastScroll = 0;
    const scrollThreshold = 50; // Mínimo scroll para activar

    function calcularAlturas() {
        const hUp = headerUp.offsetHeight;
        // Usamos la variable genérica headSecondary en lugar de headAdmin
        const hSec = headSecondary.offsetHeight;
        const hTotal = hUp + hSec;

        // 1. Asignamos la altura del header superior a una variable CSS
        root.style.setProperty('--altura-header-up', `${hUp}px`);

        // 2. Asignamos la altura TOTAL al spacer
        root.style.setProperty('--altura-header-total', `${hTotal}px`);
    }

    // Calculamos al inicio y si cambia el tamaño de la ventana
    calcularAlturas();
    window.addEventListener('resize', calcularAlturas);

    // Lógica del Scroll
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll <= 0) {
            document.body.classList.remove('scroll-hide-header');
            return;
        }

        // Si bajamos Y pasamos el umbral...
        if (currentScroll > lastScroll && currentScroll > scrollThreshold) {
            document.body.classList.add('scroll-hide-header');
        }
        // Si subimos...
        else if (currentScroll < lastScroll) {
            document.body.classList.remove('scroll-hide-header');
        }

        lastScroll = currentScroll;
    });
});