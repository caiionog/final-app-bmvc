document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const usernameError = document.getElementById('usernameError');
    const passwordError = document.getElementById('passwordError');

    // Função de validação
    const validateForm = (event) => {
        let isValid = true;

        // Limpa as mensagens de erro anteriores
        usernameError.textContent = '';
        passwordError.textContent = '';
        
        // Remove a classe de erro (caso exista)
        usernameInput.classList.remove('input-error');
        passwordInput.classList.remove('input-error');


        // Validação do Nome de Usuário
        if (usernameInput.value.trim() === '') {
            usernameError.textContent = 'O nome de usuário é obrigatório.';
            usernameInput.classList.add('input-error');
            isValid = false;
        }

        // Validação da Senha
        if (passwordInput.value.trim() === '') {
            passwordError.textContent = 'A senha é obrigatória.';
            passwordInput.classList.add('input-error');
            isValid = false;
        } else if (passwordInput.value.trim().length < 6) {
             // Exemplo de regra de validação adicional
            passwordError.textContent = 'A senha deve ter no mínimo 6 caracteres.';
            passwordInput.classList.add('input-error');
            isValid = false;
        }

        // Se a validação falhar, impede o envio do formulário
        if (!isValid) {
            event.preventDefault();
        }
    };

    // Adiciona o ouvinte de evento para o envio do formulário
    form.addEventListener('submit', validateForm);
    
    // Adiciona um estilo de erro aos inputs para validação visual (opcional)
    const style = document.createElement('style');
    style.textContent = `
        .input-error {
            border-color: var(--error-color) !important;
            box-shadow: 0 0 5px rgba(231, 76, 60, 0.5) !important;
        }
    `;
    document.head.append(style);
});