const API_BASE = 'http://localhost:5000'

document.addEventListener('DOMContentLoaded', async function () {
    const token = localStorage.getItem('token')
    const user_id = localStorage.getItem('user_id')

    if (!token || !user_id) {
        window.location.href = '../index.html'
        return
    }

    try {
        const resposta = await fetch(`${API_BASE}/curriculo/${user_id}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })

        if (resposta.status === 401 || resposta.status === 403) {
            localStorage.clear()
            window.location.href = '../index.html'
            return
        }

        const lista = await resposta.json()

        if (!Array.isArray(lista) || lista.length === 0) {
            window.location.href = 'cadastro_curriculo.html'
            return
        }

        const curr = lista[0]

        document.getElementById('curr_nome').textContent = curr.nome_completo || '-'
        document.getElementById('curr_email').textContent = curr.email || '-'
        document.getElementById('curr_telefone').textContent = curr.telefone || '-'
        document.getElementById('curr_logradouro').textContent = curr.rua_logradouro || '-'
        document.getElementById('curr_bairro').textContent = curr.bairro || '-'
        document.getElementById('curr_cidade').textContent = curr.cidade || '-'
        document.getElementById('curr_escolaridade').textContent = curr.escolaridade || '-'
        document.getElementById('curr_experiencia').textContent = curr.experiencia || 'Não informada'
        document.getElementById('curr_atuacao').textContent = curr.atuacao || '-'
        document.getElementById('curr_habilidades').textContent = curr.habilidades || '-'
        document.getElementById('curr_observacoes').textContent = curr.observacoes || 'Nenhuma'

        localStorage.setItem('curriculo_id', curr.id)
    } catch (erro) {
        console.error('Erro ao carregar curriculo:', erro)
    }
})

function logout() {
    localStorage.clear()
    window.location.href = '../index.html'
}
