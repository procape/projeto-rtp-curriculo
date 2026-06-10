const API_BASE = 'http://192.168.171.93:5003'

function navigateTo(path) {
    const base = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/') + 1)
    window.location.href = base + path
}

document.addEventListener('DOMContentLoaded', function () {
    const formLogin = document.getElementById('form_login')
    if (!formLogin) return

    formLogin.addEventListener('submit', async function (e) {
        e.preventDefault()
        const cpf = document.getElementById('cpf').value
        const senha = document.getElementById('senha').value

        try {
            const resposta = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cpf, senha })
            })
            const dados = await resposta.json()
            if (!resposta.ok) throw new Error(dados.status || dados.mensagem || 'Erro ao fazer login')

            localStorage.setItem('token', dados.access_token)
            localStorage.setItem('user_id', dados.user_id)
            localStorage.setItem('cargo', dados.cargo)

            if (dados.cargo === 'admin') {
                navigateTo('pages/dashboard.html')
            } else {
                navigateTo('pages/meu_curriculo.html')
            }
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})
