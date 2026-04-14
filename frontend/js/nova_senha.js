const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', function () {
    const emailSalvo = localStorage.getItem('email_recuperacao')
    const emailInfo = document.getElementById('email_info')
    if (emailInfo && emailSalvo) {
        emailInfo.textContent = emailSalvo
    }

    const form = document.querySelector('form')
    if (!form) return

    form.addEventListener('submit', async function (e) {
        e.preventDefault()

        const senha = document.getElementById('senha').value
        const confirmar = document.getElementById('confirmar_senha').value

        if (senha !== confirmar) {
            alert('As senhas nao coincidem.')
            return
        }

        const tokenRecuperacao = document.getElementById('token_recuperacao').value
        const email = localStorage.getItem('email_recuperacao')

        if (!email) {
            alert('Sessao expirada. Solicite um novo token.')
            window.location.href = 'recuperar_senha.html'
            return
        }

        try {
            const resposta = await fetch(`${API_BASE}/auth/reset-password`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, token: tokenRecuperacao, senha })
            })
            const dados = await resposta.json()
            if (!resposta.ok) throw new Error(dados.erro || 'Erro ao redefinir senha')

            localStorage.removeItem('email_recuperacao')
            alert('Senha atualizada com sucesso!')
            window.location.href = '../index.html'
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})
