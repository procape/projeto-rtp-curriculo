// Funções de autenticação reutilizáveis
window.logout = function () {
    localStorage.clear()
    // Redireciona para a página de login (ajusta caminho conforme local)
    window.location.href = '/index.html'
}

window.fillDemoCredentials = function (type = 'user') {
    const cpfInput = document.getElementById('cpf')
    const senhaInput = document.getElementById('senha')
    if (!cpfInput || !senhaInput) return

    if (type === 'admin') {
        cpfInput.value = '00000000000'
        senhaInput.value = 'demo_admin'
    } else {
        cpfInput.value = '11111111111'
        senhaInput.value = 'demo_user'
    }
    cpfInput.focus()
}

window.demoLogin = function (type = 'user') {
    // valores de demo locais: não dependem do backend
    const demoUser = {
        user: { cpf: '11111111111', senha: 'demo_user', cargo: 'usuario', user_id: 2 },
        admin: { cpf: '00000000000', senha: 'demo_admin', cargo: 'admin', user_id: 1 }
    }

    const sel = type === 'admin' ? demoUser.admin : demoUser.user
    localStorage.setItem('token', 'demo-token-' + sel.cpf)
    localStorage.setItem('user_id', sel.user_id)
    localStorage.setItem('cargo', sel.cargo)
    // redireciona conforme cargo
    if (sel.cargo === 'admin') window.location.href = '../pages/dashboard.html'
    else window.location.href = '../pages/meu_curriculo.html'
}
