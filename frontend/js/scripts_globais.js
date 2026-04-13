// O evento DOMContentLoaded garante que o JS espere o HTML carregar primeiro
document.addEventListener("DOMContentLoaded", function () {
  // Bloqueia números (apenas letras)
  const camposLetras = document.querySelectorAll(".apenas-letras");
  camposLetras.forEach(function (campo) {
    campo.addEventListener("input", function (event) {
      event.target.value = event.target.value.replace(/[^a-zA-ZÀ-ÿ\s]/g, "");
    });
  });

  // Bloqueia letras (apenas números)
  const camposNumeros = document.querySelectorAll(".apenas-numeros");
  camposNumeros.forEach(function (campo) {
    campo.addEventListener("input", function (event) {
      event.target.value = event.target.value.replace(/\D/g, "");
    });
  });

  // 2. FUNÇÃO: MOSTRAR / OCULTAR SENHA (Olho)

  function configurarOlho(idBotao, idInput, idIcone) {
    const btn = document.getElementById(idBotao);
    const input = document.getElementById(idInput);
    const icone = document.getElementById(idIcone);

    // Se a página não tiver esses campos, a função para aqui silenciosamente
    if (!btn || !input || !icone) return;

    btn.addEventListener("click", function () {
      if (input.type === "password") {
        input.type = "text";
        icone.classList.remove("bi-eye-slash");
        icone.classList.add("bi-eye");
      } else {
        input.type = "password";
        icone.classList.remove("bi-eye");
        icone.classList.add("bi-eye-slash");
      }
    });
  }

  configurarOlho("btn_olho_senha", "senha", "icone_senha");
  configurarOlho("btn_olho_confirmar", "confirmar_senha", "icone_confirmar");

  // 3. MEDIDOR DE FORÇA E IGUALDADE DE SENHAS

  const inputSenha = document.getElementById("senha");
  const inputConfirmar = document.getElementById("confirmar_senha");
  const barraForca = document.getElementById("barra_forca");
  const textoForca = document.getElementById("texto_forca");
  const textoAvisoIgualdade = document.getElementById("texto_aviso_igualdade");

  // Só roda a lógica de força se o campo de senha principal e a barra existirem na página
  if (inputSenha && barraForca && textoForca) {
    inputSenha.addEventListener("input", function () {
      let senha = this.value;
      let pontuacao = 0;

      if (senha.length === 0) {
        barraForca.style.width = "0%";
        barraForca.className = "progress-bar";
        textoForca.innerText = "Mínimo de 8 caracteres.";
        textoForca.className = "text-muted fw-semibold";
        verificarSenhasIguais();
        return;
      }

      if (senha.length >= 8) pontuacao += 1;
      if (senha.match(/[A-Z]/)) pontuacao += 1;
      if (senha.match(/[0-9]/)) pontuacao += 1;
      if (senha.match(/[^a-zA-Z0-9]/)) pontuacao += 1;

      if (senha.length < 8) {
        barraForca.style.width = "25%";
        barraForca.className = "progress-bar bg-danger";
        textoForca.innerText = "Senha muito curta (fraca)";
        textoForca.className = "text-danger fw-semibold";
      } else if (pontuacao === 1 || pontuacao === 2) {
        barraForca.style.width = "50%";
        barraForca.className = "progress-bar bg-warning";
        textoForca.innerText = "Senha média (adicione números ou símbolos)";
        textoForca.className = "text-warning fw-semibold";
      } else if (pontuacao === 3) {
        barraForca.style.width = "75%";
        barraForca.className = "progress-bar bg-info";
        textoForca.innerText = "Senha boa";
        textoForca.className = "text-info fw-semibold";
      } else if (pontuacao === 4) {
        barraForca.style.width = "100%";
        barraForca.className = "progress-bar bg-success";
        textoForca.innerText = "Senha forte!";
        textoForca.className = "text-success fw-semibold";
      }

      verificarSenhasIguais();
    });
  }

  // Só roda a verificação de igualdade se o campo de confirmação existir
  if (inputConfirmar) {
    inputConfirmar.addEventListener("input", verificarSenhasIguais);
  }

  function verificarSenhasIguais() {
    // Se não tiver um dos campos ou o texto de erro na página, aborta
    if (!inputSenha || !inputConfirmar || !textoAvisoIgualdade) return;

    const valorSenha = inputSenha.value;
    const valorConfirmar = inputConfirmar.value;

    if (valorConfirmar.length > 0) {
      if (valorSenha !== valorConfirmar) {
        textoAvisoIgualdade.classList.remove("d-none");
      } else {
        textoAvisoIgualdade.classList.add("d-none");
      }
    } else {
      textoAvisoIgualdade.classList.add("d-none");
    }
  }

  // 4. BUSCA DE CEP AUTOMÁTICA (ViaCEP)

  const campoCep = document.getElementById("cep");

  // Só vai rodar a lógica se o campo de CEP existir na tela
  if (campoCep) {
    campoCep.addEventListener("blur", function (event) {
      // Pega o valor e tira tudo que não for número
      let cep = event.target.value.replace(/\D/g, "");

      if (cep.length === 8) {
        let url = `https://viacep.com.br/ws/${cep}/json/`;

        fetch(url)
          .then((resposta) => resposta.json())
          .then((dados) => {
            if (!dados.erro) {
              // Preenche os campos
              document.getElementById("logradouro").value = dados.logradouro;
              document.getElementById("bairro").value = dados.bairro;
              document.getElementById("cidade").value = dados.localidade;
              document.getElementById("estado").value = dados.uf;

              // Joga o cursor para o campo de número
              document.getElementById("numero").focus();
            } else {
              alert(
                "CEP não encontrado. Por favor, verifique o número digitado.",
              );
              limparCamposEndereco();
            }
          })
          .catch((erro) => {
            console.error(
              "Erro ao conectar com o serviço de busca de CEP.",
              erro,
            );
          });
      } else {
        if (cep.length > 0) {
          alert("Formato de CEP inválido.");
          limparCamposEndereco();
        }
      }
    });
  }

  // Função auxiliar para limpar os campos caso o CEP dê erro
  function limparCamposEndereco() {
    // if para evitar erros caso a página não tenha um dos campos
    if (document.getElementById("logradouro"))
      document.getElementById("logradouro").value = "";
    if (document.getElementById("bairro"))
      document.getElementById("bairro").value = "";
    if (document.getElementById("cidade"))
      document.getElementById("cidade").value = "";
    if (document.getElementById("estado"))
      document.getElementById("estado").value = "";
  }
});

// 5. Sidebar
const sidebar = document.getElementById("sidebar");

// O "if" garante que o código não quebre nas telas que NÃO têm sidebar (como o Login)
if (sidebar) {
  sidebar.addEventListener("mouseenter", () => {
    sidebar.classList.remove("collapsed");
  });

  sidebar.addEventListener("mouseleave", () => {
    sidebar.classList.add("collapsed");
  });
}

// 6. REMOVER TELA DE LOADING (Fora do DOMContentLoaded)

window.addEventListener("load", function () {
  // Busca o ID com HÍFEN, igual está no seu HTML
  const telaLoading = document.getElementById("tela-loading");

  if (telaLoading) {
    // Mudei para 800ms. Dá tempo de ver o coração bater 1x e já entra no sistema.
    setTimeout(function () {
      telaLoading.style.opacity = "0"; // Deixa transparente suavemente

      // Espera a transição do CSS terminar (meio segundo) e apaga a div de vez
      setTimeout(function () {
        telaLoading.style.display = "none";
      }, 500);
    }, 2000);
  }
});

// Aguarda a tela carregar por completo
document.addEventListener("DOMContentLoaded", function () {
  // Procura o formulário de login na tela
  const formLogin = document.getElementById("form_login");

  if (formLogin) {
    formLogin.addEventListener("submit", function (event) {
      // 1. Evita que a página recarregue (não pisca a tela)
      event.preventDefault();

      // 2. Pega os valores que o usuário digitou
      const emailDigitado = document.getElementById("email").value;
      const senhaDigitada = document.getElementById("senha").value;

      // 3. Cria a caixinha JSON com os dados
      const dadosDoLogin = {
        email: emailDigitado,
        senha: senhaDigitada,
      };

      // 4. Envia para o servidor Flask
      // ATENÇÃO: Confirme com a equipe do Back-end se a rota é exatamente essa!
      fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dadosDoLogin),
      })
        .then((resposta) => resposta.json())
        .then((retornoDoFlask) => {
          // 5. Analisa a resposta do Flask
          if (retornoDoFlask.sucesso === true) {
            // Login autorizado! Vai para o currículo
            window.location.href = "pages/meu_curriculo.html";
          } else {
            // Login negado! Exibe o erro do back-end
            alert("Ops! " + retornoDoFlask.mensagem);
          }
        })
        .catch((erro) => {
          console.error("Erro na comunicação com o Flask:", erro);
          alert(
            "Erro ao conectar com o servidor. Verifique se o Back-end está rodando.",
          );
        });
    });
  }
});
