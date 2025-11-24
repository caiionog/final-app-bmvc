document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('messageForm');
    const authorInput = document.getElementById('author');
    const textInput = document.getElementById('text');

    const authorError = document.getElementById('authorError');
    const textError = document.getElementById('textError');

    const validateForm = (event) => {
        let isValid = true;

        // limpa erros
        authorError.textContent = '';
        textError.textContent = '';

        authorInput.classList.remove('input-error');
        textInput.classList.remove('input-error');

        // valida nome
        if (authorInput.value.trim() === '') {
            authorError.textContent = 'O nome é obrigatório.';
            authorInput.classList.add('input-error');
            isValid = false;
        }

        // valida texto
        if (textInput.value.trim() === '') {
            textError.textContent = 'A mensagem não pode estar vazia.';
            textInput.classList.add('input-error');
            isValid = false;
        } else if (textInput.value.trim().length < 3) {
            textError.textContent = 'A mensagem deve ter pelo menos 3 caracteres.';
            textInput.classList.add('input-error');
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        }
    };

    form.addEventListener('submit', validateForm);
});
