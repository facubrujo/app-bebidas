function mostrarCarga() {
    document.getElementById("ventana-carga").style.display = "flex";
    document.getElementById("contenido").style.display = "none";
}

function ocultarCarga() {
    document.getElementById("ventana-carga").style.display = "none";
    document.getElementById("contenido").style.display = "block";
}

window.onload = function () {
    mostrarCarga();
};