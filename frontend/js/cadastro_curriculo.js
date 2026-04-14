const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token')
    const user_id = localStorage.getItem('user_id')

    if (!token || !user_id) {
        window.location.href = '../index.html'
        return
    }

    const form = document.getElementById('formCurriculo')
    if (!form) return

    form.addEventListener('submit', async function (e) {
        e.preventDefault()

        const logradouro = document.getElementById('logradouro').value
        const numero = document.getElementById('numero').value

        const dados = {
            nome_completo: document.getElementById('nome_completo').value,
            email: document.getElementById('email').value,
            telefone: document.getElementById('telefone').value,
            rua_logradouro: numero ? `${logradouro}, ${numero}` : logradouro,
            bairro: document.getElementById('bairro').value,
            cidade: document.getElementById('cidade').value,
            escolaridade: document.getElementById('escolaridade').value,
            experiencia: document.getElementById('tempo_experiencia').value,
            atuacao: document.getElementById('area_atuacao').value,
            habilidades: document.getElementById('habilidades_tecnicas').value,
            observacoes: document.getElementById('observacoes').value,
            user_id: parseInt(user_id)
        }

        const curriculo_id = localStorage.getItem('curriculo_id')
        const metodo = curriculo_id ? 'PUT' : 'POST'
        const url = curriculo_id ? `${API_BASE}/curriculo/${user_id}` : `${API_BASE}/curriculo`

        try {
            const resposta = await fetch(url, {
                method: metodo,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(dados)
            })
            const resultado = await resposta.json()
            if (!resposta.ok) throw new Error(resultado.mensagem || resultado.erro || 'Erro ao salvar curriculo')

            alert('Curriculo salvo com sucesso!')
            window.location.href = 'meu_curriculo.html'
        } catch (erro) {
            alert('Erro: ' + erro.message)
        }
    })
})