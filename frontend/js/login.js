const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', function () {
    const formLogin = document.getElementById('form_login')
    if (!formLogin) return

    formLogin.addEventListener('submit', async function (e) {
        e.preventDefault()
        const email = document.getElementById('email').value
        const senha = document.getElementById('senha').value

        try {
            const resposta = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, senha })
            })
            const dados = await resposta.json()
            if (!resposta.ok) throw new Error(dados.status || dados.mensagem || 'Erro ao fazer login')

            localStorage.setItem('token', dados.access_token)
            localStorage.setItem('user_id', dados.user_id)
            localStorage.setItem('cargo', dados.cargo)

            if (dados.cargo === 'admin') {
                window.location.href = 'pages/dashboard.html'
            } else {
                window.location.href = 'pages/meu_curriculo.html'
            }
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})
