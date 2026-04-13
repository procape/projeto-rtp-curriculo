document.getElementById("formCurriculo").addEventListener("submit", async function(e) {
    e.preventDefault();

    const dados = {
        nome_completo: document.getElementById("nome_completo").value,
        email: document.getElementById("email").value,
        telefone: document.getElementById("telefone").value,
        cep: document.getElementById("cep").value,
        logradouro: document.getElementById("logradouro").value,
        numero: document.getElementById("numero").value,
        bairro: document.getElementById("bairro").value,
        cidade: document.getElementById("cidade").value,
        estado: document.getElementById("estado").value,
        escolaridade: document.getElementById("escolaridade").value,
        tempo_experiencia: document.getElementById("tempo_experiencia").value,
        area_atuacao: document.getElementById("area_atuacao").value,
        habilidades_tecnicas: document.getElementById("habilidades_tecnicas").value,
        observacoes: document.getElementById("observacoes").value
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/curriculo/post", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const result = await response.json();

        console.log(result);
        alert("Currículo salvo com sucesso!");


        
        setTimeout(() => {
            window.location.href = "meu_curriculo.html";
        }, 1500);



    } catch (error) {
        console.error(error);
        alert("Erro ao salvar currículo");
    }

});