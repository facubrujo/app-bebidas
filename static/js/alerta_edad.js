window.onload = function () {
    const session = sessionStorage.getItem('session'); // null, true o false
    console.log(`1 --- estado de la sesion = ${sessionStorage.getItem("session")}`);

    venAlerta = document.querySelector(".alerta-edad-contenedor");
    venBloqueo = document.getElementById("bloqueo");
    const body = document.querySelector("body");

    body.style.overflow = "hidden";

    btnSi = document.getElementById("si");
    btnNo = document.getElementById("no");

    if (session !== null) {
        venAlerta.style.display = "none";
        venBloqueo.style.display = "none";
        body.style.removeProperty("overflow", true);
    } else {
        btnSi.addEventListener("click", function () {
            sessionStorage.setItem("session", true);
            venAlerta.style.display = "none";
            venBloqueo.style.display = "none";
            
        });

        btnNo.addEventListener("click", function () {
            sessionStorage.setItem("session", true);
            venAlerta.style.display = "none";
            venBloqueo.style.display = "none";
            body.style.removeProperty("overflow", true);
        });
    };
};