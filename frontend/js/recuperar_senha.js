const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form')
    if (!form) return

    form.addEventListener('submit', async function (e) {
        e.preventDefault()
        const email = document.getElementById('email').value

        try {
            const resposta = await fetch(`${API_BASE}/auth/forgot-password`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email })
            })
            const dados = await resposta.json()
            if (!resposta.ok) throw new Error(dados.erro || 'Erro ao enviar token')

            localStorage.setItem('email_recuperacao', email)
            alert('Token enviado para o seu e-mail.')
            window.location.href = 'nova_senha.html'
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})
