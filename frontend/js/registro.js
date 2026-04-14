const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formRegistro')
    if (!form) return

    form.addEventListener('submit', async function (e) {
        e.preventDefault()

        const senha = document.getElementById('senha').value
        const confirmar = document.getElementById('confirmar_senha').value

        if (senha !== confirmar) {
            alert('As senhas não coincidem!')
            return
        }

        const dados = {
            cpf: document.getElementById('cpf').value,
            nome: document.getElementById('nome_completo').value,
            email: document.getElementById('email').value,
            senha: senha
        }

        try {
            const resposta = await fetch(`${API_BASE}/user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            })
            const resultado = await resposta.json()
            if (!resposta.ok) throw new Error(resultado.erro || resultado.mensagem || 'Erro ao criar conta')

            alert('Conta criada com sucesso!')
            window.location.href = '../index.html'
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})
