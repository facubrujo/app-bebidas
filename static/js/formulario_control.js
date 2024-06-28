document.addEventListener("DOMContentLoaded", function () {
    const alerta = document.getElementById("carga-correcta");
    alerta.style.display = "none";

    // objetos validaciones y mensajes de error
    const validaciones = {
        nombre: /^[a-zA-Z]+$/,
        apellido: /^[a-zA-Z]+$/,
        email: /^(?!\s*$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, // /^[^\s@]+@[^\s@]+\.[^\s@]+$/, 
        password1: /^(?=.*[A-Z])(?=.*[^\s]).{8,}$/ //  /^\S+$/
    };

    const mensajesError = {
        nombre: "El nombre debe contener solo letras y sin espacios.",
        apellido: "El apellido debe contener solo letras y sin espacios.",
        email: "El email debe tener un formato valido (email@email.com).",
        password1: "La contraseña debe ser de 8 o mas caracteres, no debe contener espacios y debe tener al menos una mayuscula",
        password2: "Las contraseñas deben coincidir.",
        esMayor: "Debe seleccionar una opción.",
        genero: "Debe seleccionar una opción."
    };

    // control nombre 
    const nombre = document.getElementById("nombre").addEventListener("input", function () {
        const error = document.getElementById("nombre-error");
        if (validaciones.nombre.test(this.value)) {
            error.className = "error-ok";
            error.textContent = "OK";
        } else {
            error.className = "error";
            error.textContent = mensajesError.nombre;
        }
    });

    // control apellido
    const apellido = document.getElementById("apellido").addEventListener("input", function () {
        const error = document.getElementById("apellido-error");
        if (validaciones.apellido.test(this.value)) {
            error.className = "error-ok";
            error.textContent = "OK";
        } else {
            error.className = "error";
            error.textContent = mensajesError.apellido;
        }
    });

    // control email
    const email = document.getElementById("email").addEventListener("input", function () {
        const error = document.getElementById("email-error");
        console.log("desde input : "+this.value);

        if (validaciones.email.test(this.value) ) { //&& !existe
            error.className = "error-ok";
            error.textContent = "OK";
        } else if (validaciones.email.test(this.value) ) { //&& existe !== null
            error.textContent = `ya existe un usuario con email : ${this.value}`;
            error.className = "error";
        } else {
            error.className = "error";
            error.textContent = mensajesError.email;
        }
    });

    // control contraseña 1
    const password1 = document.getElementById("password1").addEventListener("input", function () {
        const error = document.getElementById("password1-error");
        if (validaciones.password1.test(this.value)) {
            error.className = "error-ok";
            error.textContent = "OK";
        } else {
            error.className = "error";
            error.textContent = mensajesError.password1;
        }
    });

    // control contraseña 2
    const password2 = document.getElementById("password2").addEventListener("input", function () {
        var pass1 = document.getElementById("password1").value;
        const error = document.getElementById("password2-error");
        if (pass1 === this.value.toString()) {
            error.className = "error-ok";
            error.textContent = "OK";
        } else {
            error.className = "error";
            error.textContent = mensajesError.password2;
        }
    });

    // control campo select edad
    const mayorEdad = document.getElementById("esMayor").addEventListener("input", function () {
        console.log(this.value);
        const error = document.getElementById("esMayor-error");
        if (this.value === "si" || this.value === "no") {
            console.log("ok");
            error.className = "error-ok";
            error.textContent = "OK";
        } else {
            console.log("error");
            error.className = "error";
            error.textContent = mensajesError.esMayor;
        }
    });

    // control campo select radio genero
    document.querySelectorAll('input[type="radio"]').forEach(input => {
        input.addEventListener('change', () => {
            const error = document.getElementById("genero-error");
            if (input.checked) {
                error.className = "error-ok"
                error.textContent = "OK";
            } else {
                error.className = "error";
                error.textContent = mensajesError.genero;
            }
        });
    });

    // carga y muestra de imagen
    let imagenUrl = "../img/usuario_icono.png";
    document.querySelector('#archivo').addEventListener('change', function (event) {
        const imagenInput = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            imagenUrl = e.target.result;

            const imagenMuestra = document.getElementById('imagen-muestra');
            imagenMuestra.src = e.target.result;
            document.getElementById('contenedor-de-imagen').style.display = 'block';
        }
        reader.readAsDataURL(imagenInput);
    });

});

