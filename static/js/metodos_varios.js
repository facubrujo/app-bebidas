function traducir() {
    const textosEnIngles = document.querySelectorAll('.texto');

    const idiomaOrigen = 'en';
    const idiomaDestino = 'es';

    textosEnIngles.forEach(texto => {
        const textoEnIngles = texto.textContent;

        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${idiomaOrigen}&tl=${idiomaDestino}&dt=t&q=${encodeURIComponent(textoEnIngles)}`;

        fetch(url)
            .then(respuesta => respuesta.json())
            .then(data => {
                const textoTraducido = data[0][0][0];
                texto.textContent = textoTraducido;
            })
            .catch(error => console.error('Error al traducir:', error));
    });
}