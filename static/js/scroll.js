// Guardar la posición del scroll antes de redireccionar
function guardarPosScroll() {
    localStorage.setItem('scrollPosition', window.scrollY);
}

// Restaurar la posición del scroll al cargar la página
function restaurarPosScroll() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition !== null) {
        window.scrollTo(0, parseInt(scrollPosition));
        localStorage.removeItem('scrollPosition');
    }
}

// // Añadir evento a todos los enlaces para guardar la posición del scroll antes de redireccionar
// document.querySelectorAll('a').forEach(anchor => {
//     anchor.addEventListener('click', guardarPosScroll);
// });

// Añadir evento a todos los formularios para guardar la posición del scroll antes de enviar
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', guardarPosScroll);
});

// // Restaurar la posición del scroll al cargar la página
window.addEventListener('load', restaurarPosScroll);


const searchInput = document.getElementById('filtro');
const elementos = document.querySelectorAll('.usuario');

searchInput.addEventListener('input', function () {
    const busqueda = searchInput.value.toLowerCase();

    elementos.forEach(elemento => {
        const nombre = elemento.querySelector('.nombre').textContent.toLowerCase();
        // const rol = elemento.querySelector('.rol').textContent.toLowerCase();
        // const email = elemento.querySelector('.email').textContent.toLowerCase();
        // const activo = elemento.querySelector('.activo').textContent.toLowerCase();

        if (busqueda === '' ||nombre.includes(busqueda)) { // email.includes(busqueda) || rol.includes(busqueda) || activo.includes(busqueda) || 
            elemento.style.display = 'table-row';
        } else {
            elemento.style.display = 'none';
        }
    });
});
