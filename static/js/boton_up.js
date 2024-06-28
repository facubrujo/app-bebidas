document.addEventListener('DOMContentLoaded', () => {
    // Obtener el botón
    const scrollBtn = document.getElementById("scrollBtn");

    // Mostrar el botón cuando se desplaza 20px desde la parte superior
    window.addEventListener('scroll', () => {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            scrollBtn.style.display = "block";
        } else {
            scrollBtn.style.display = "none";
        }
    });

    // Cuando se hace clic en el botón, se desplaza hacia arriba de la página
    scrollBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});