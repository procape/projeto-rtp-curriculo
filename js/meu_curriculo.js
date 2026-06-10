const API_BASE = 'http://192.168.171.93:5003'

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
        // show arquivo if present
        if (curr.arquivo) {
            const fileUrl = `${API_BASE}/curriculo/file/${curr.arquivo}`
            const section = document.getElementById('curr_file_section')
            section.innerHTML = `\n                <div class="text-center">\n                    <a href="${fileUrl}" target="_blank" class="btn btn-primary mb-2">Abrir PDF</a>\n                    <button id="btn_remover_arquivo" class="btn btn-danger ms-2">Remover arquivo</button>\n                    <div class="mt-3">\n                        <iframe src="${fileUrl}" style="width:100%;height:600px;" frameborder="0"></iframe>\n                    </div>\n                </div>\n            `
            const btnRem = document.getElementById('btn_remover_arquivo')
            if (btnRem) {
                btnRem.addEventListener('click', async () => {
                    if (!confirm('Remover arquivo do currículo?')) return
                    try {
                        const res = await fetch(`${API_BASE}/curriculo/${user_id}/file`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } })
                        const js = await res.json()
                        if (!res.ok) throw new Error(js.mensagem || js.erro || 'Erro')
                        alert('Arquivo removido')
                        section.innerHTML = ''
                    } catch (err) {
                        alert('Erro: ' + err.message)
                    }
                })
            }
        }
    } catch (erro) {
        console.error('Erro ao carregar curriculo:', erro)
    }
})

function logout() {
    localStorage.clear()
    window.location.href = '../index.html'
}
