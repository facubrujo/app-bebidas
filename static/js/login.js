document.addEventListener('DOMContentLoaded', function () {
    let todosUsuarios = JSON.parse(localStorage.getItem("usuarios"));
    const formLogin = document.getElementById('login');
    const inputEmail = document.getElementById('email');
    const imgPerfil = document.getElementById("img-login");
    let inputEmailValor = '';
    let usuarioLog = '';

    // ecucha input email y muestra la imagen del usuario
    inputEmail.addEventListener('input', function (event) {
        inputEmailValor = event.target.value;

        usuarioLog = todosUsuarios.find(function (usuario) {
            //console.log(usuario)
            return usuario.email === inputEmailValor;
        });

        if (usuarioLog) {
            inputEmail.style.border = "3px solid #00c900";
            //imgPerfil.style.border = "3px solid #00c900";
            imgPerfil.src = usuarioLog.imagen;
        } else {
            console.log("se setea imagen por defecto");
            inputEmail.style.border = "3px solid #ff0000";
            imgPerfil.src = "../img/usuario_icono.png";
        }
    });

    // si el usuario y contraseña son correctos carga el perfil de usuario
    formLogin.addEventListener('submit', function (event) {
        event.preventDefault();
        const inputContraseña = document.getElementById('pass');
        const contraseña = inputContraseña.value;
        const error = document.getElementById("error");

        if (usuarioLog) {
            if (usuarioLog.password === contraseña) {
                usuarioLog.sesion = true;
                
                inputContraseña.style.border = '3px solid #00c900';
                error.className = "error-ok";
                error.textContent = "Logueado correctamente";
                login.appendChild(error);

                // guarda (actualiza) el usuario que loguea
                const guardarUsu = JSON.stringify(todosUsuarios)
                localStorage.setItem("usuarios", guardarUsu);
                
                // guarda un estado de usuario online en la session del navegador
                sessionStorage.setItem("usuarioOnline", JSON.stringify(usuarioLog));

                window.location.href = "perfil_usuario.html";

            } else {
                // si la contraseña no existe o es incorrecta
                // muestra mensaje de error
                inputContraseña.style.border = '3px solid #ff0000';
                error.className = "error";
                error.textContent = "contraseña incorrecta";
                login.appendChild(error);
            }
        } else {
            // si ni email ni contraseña coinciden muestra mensaje de error
            inputEmail.style.border = '3px solid #ff0000';
            inputContraseña.style.border = '3px solid #ff0000';
            error.className = "error";
            error.textContent = "usuario no registrado o no existe";
            login.appendChild(error);
        }
    });
});