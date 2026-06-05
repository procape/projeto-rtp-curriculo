const API_BASE = 'http://192.168.171.93:5000'

document.addEventListener('DOMContentLoaded', function () {
    const token = localStorage.getItem('token')
    const user_id = localStorage.getItem('user_id')

    if (!token || !user_id) {
        window.location.href = '../index.html'
        return
    }

    const form = document.getElementById('formCurriculo')
    if (!form) return

    // preload existing curriculo if present
    async function preload() {
        try {
            const res = await fetch(`${API_BASE}/curriculo/${user_id}`, { headers: { 'Authorization': `Bearer ${token}` } })
            const lista = await res.json()
            if (Array.isArray(lista) && lista.length > 0) {
                const curr = lista[0]
                document.getElementById('nome_completo').value = curr.nome_completo || ''
                document.getElementById('email').value = curr.email || ''
                document.getElementById('telefone').value = curr.telefone || ''
                // split rua_logradouro into rua and numero if possible
                const rua = curr.rua_logradouro || ''
                if (rua.includes(',')) {
                    const parts = rua.split(',').map(s => s.trim())
                    document.getElementById('logradouro').value = parts[0]
                    document.getElementById('numero').value = parts[1] || ''
                } else {
                    document.getElementById('logradouro').value = rua
                }
                document.getElementById('bairro').value = curr.bairro || ''
                document.getElementById('cidade').value = curr.cidade || ''
                document.getElementById('escolaridade').value = curr.escolaridade || ''
                document.getElementById('tempo_experiencia').value = curr.experiencia || ''
                document.getElementById('area_atuacao').value = curr.atuacao || ''
                document.getElementById('habilidades_tecnicas').value = curr.habilidades || ''
                document.getElementById('observacoes').value = curr.observacoes || ''
                localStorage.setItem('curriculo_id', curr.id)
                if (curr.arquivo) {
                    document.getElementById('arquivo_info').textContent = `Arquivo atual: ${curr.arquivo}`
                    document.getElementById('remover_arquivo').checked = false
                }
            }
        } catch (err) {
            console.error('Erro preload curriculo', err)
        }
    }

    preload()

    form.addEventListener('submit', async function (e) {
        e.preventDefault()

        const logradouro = document.getElementById('logradouro').value
        const numero = document.getElementById('numero').value

        const formData = new FormData()
        formData.append('nome_completo', document.getElementById('nome_completo').value)
        formData.append('email', document.getElementById('email').value)
        formData.append('telefone', document.getElementById('telefone').value)
        formData.append('rua_logradouro', numero ? `${logradouro}, ${numero}` : logradouro)
        formData.append('bairro', document.getElementById('bairro').value)
        formData.append('cidade', document.getElementById('cidade').value)
        formData.append('escolaridade', document.getElementById('escolaridade').value)
        formData.append('experiencia', document.getElementById('tempo_experiencia').value)
        formData.append('atuacao', document.getElementById('area_atuacao').value)
        formData.append('habilidades', document.getElementById('habilidades_tecnicas').value)
        formData.append('observacoes', document.getElementById('observacoes').value)
        formData.append('user_id', parseInt(user_id))

        const fileInput = document.getElementById('arquivo')
        if (fileInput && fileInput.files && fileInput.files[0]) {
            formData.append('arquivo', fileInput.files[0])
        }
        const remover = document.getElementById('remover_arquivo')
        if (remover && remover.checked) {
            formData.append('remover_arquivo', 'true')
        }

        const curriculo_id = localStorage.getItem('curriculo_id')
        const metodo = curriculo_id ? 'PUT' : 'POST'
        const url = curriculo_id ? `${API_BASE}/curriculo/${user_id}` : `${API_BASE}/curriculo`

        try {
            const resposta = await fetch(url, {
                method: metodo,
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
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