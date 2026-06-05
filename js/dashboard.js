const API_BASE = 'http://192.168.171.93:5000'

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

    const modalFileSection = document.getElementById('modal_file_section')

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

    if (curr.arquivo) {
        const fileUrl = `${API_BASE}/curriculo/file/${encodeURIComponent(curr.arquivo)}`
        modalFileSection.innerHTML = `
            <div class="text-center">
                <a href="${fileUrl}" target="_blank" class="btn btn-primary mb-3">Abrir arquivo</a>
                <button type="button" id="btn_remover_arquivo" class="btn btn-danger mb-3 ms-2">Remover arquivo</button>
                <div class="mt-3">
                    <iframe src="${fileUrl}" style="width:100%;height:500px;" frameborder="0"></iframe>
                </div>
            </div>
        `
        const btnRem = document.getElementById('btn_remover_arquivo')
        if (btnRem) {
            btnRem.addEventListener('click', async () => {
                if (!confirm('Remover arquivo do currículo?')) return
                try {
                    const token = localStorage.getItem('token')
                    const resposta = await fetch(`${API_BASE}/curriculo/${curr.id}/file`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    })
                    const data = await resposta.json()
                    if (!resposta.ok) throw new Error(data.mensagem || data.erro || 'Erro ao remover arquivo')
                    alert('Arquivo removido com sucesso')
                    modalFileSection.innerHTML = '<div class="text-center text-secondary">Nenhum arquivo anexado.</div>'
                } catch (erro) {
                    alert('Erro ao remover arquivo: ' + erro.message)
                }
            })
        }
    } else {
        modalFileSection.innerHTML = '<div class="text-center text-secondary">Nenhum arquivo anexado.</div>'
    }
}

function logout() {
    localStorage.clear()
    window.location.href = '../index.html'
}
