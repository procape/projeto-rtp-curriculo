const API_BASE = 'http://localhost:5000'

let curriculosData = []

document.addEventListener('DOMContentLoaded', async function () {
    const token = localStorage.getItem('token')
    const cargo = localStorage.getItem('cargo')

    if (!token || cargo !== 'admin') {
        alert('Acesso restrito a administradores.')
        window.location.href = '../index.html'
        return
    }

    await carregarCurriculos()

    document.getElementById('confirmarExclusao').addEventListener('click', async function () {
        const id = this.getAttribute('data-id')
        try {
            const resposta = await fetch(`${API_BASE}/curriculo/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            })
            if (!resposta.ok) throw new Error('Erro ao excluir')
            bootstrap.Modal.getInstance(document.getElementById('modalExcluir')).hide()
            await carregarCurriculos()
        } catch (erro) {
            alert('Erro ao excluir: ' + erro.message)
        }
    })
})

async function carregarCurriculos() {
    const token = localStorage.getItem('token')
    const corpoTabela = document.getElementById('corpo_tabela_usuarios')
    const contador = document.getElementById('contador_registros')

    try {
        const resposta = await fetch(`${API_BASE}/curriculo`, {
            headers: { 'Authorization': `Bearer ${token}` }
        })
        if (!resposta.ok) throw new Error('Falha ao buscar curriculos')
        curriculosData = await resposta.json()

        corpoTabela.innerHTML = ''

        if (curriculosData.length === 0) {
            corpoTabela.innerHTML = '<tr><td colspan="4" class="text-center text-secondary py-4">Nenhum curriculo cadastrado.</td></tr>'
            contador.textContent = 'Mostrando 0 registros'
            return
        }

        curriculosData.forEach(curr => {
            const tr = document.createElement('tr')
            tr.innerHTML = `
                <td>${curr.nome_completo || '-'}</td>
                <td>${curr.atuacao || '-'}</td>
                <td>${curr.escolaridade || '-'}</td>
                <td class="text-end">
                    <button class="btn btn-sm text-primary p-0 me-2" data-bs-toggle="modal" data-bs-target="#modalVerCurriculo" onclick="prepararVer(${curr.id})">Ver</button>
                    <button type="button" class="btn btn-sm text-danger p-0" data-bs-toggle="modal" data-bs-target="#modalExcluir" onclick="prepararExclusao(${curr.id})">Excluir</button>
                </td>
            `
            corpoTabela.appendChild(tr)
        })

        contador.textContent = `Mostrando ${curriculosData.length} registros`
    } catch (erro) {
        corpoTabela.innerHTML = '<tr><td colspan="4" class="text-center text-danger py-4">Erro de conexao com o servidor.</td></tr>'
        contador.textContent = 'Erro de conexao'
    }
}

function prepararExclusao(id) {
    document.getElementById('confirmarExclusao').setAttribute('data-id', id)
}

function prepararVer(id) {
    const curr = curriculosData.find(c => c.id === id)
    if (!curr) return

    document.getElementById('modal_nome').textContent = curr.nome_completo || '-'
    document.getElementById('modal_email').textContent = curr.email || '-'
    document.getElementById('modal_telefone').textContent = curr.telefone || '-'
    document.getElementById('modal_logradouro').textContent = curr.rua_logradouro || '-'
    document.getElementById('modal_bairro').textContent = curr.bairro || '-'
    document.getElementById('modal_cidade').textContent = curr.cidade || '-'
    document.getElementById('modal_escolaridade').textContent = curr.escolaridade || '-'
    document.getElementById('modal_experiencia').textContent = curr.experiencia || 'Nao informada'
    document.getElementById('modal_atuacao').textContent = curr.atuacao || '-'
    document.getElementById('modal_habilidades').textContent = curr.habilidades || '-'
    document.getElementById('modal_observacoes').textContent = curr.observacoes || 'Nenhuma'
}

function logout() {
    localStorage.clear()
    window.location.href = '../index.html'
}
