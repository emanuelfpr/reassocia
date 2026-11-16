// JavaScript simples do site

// Esconde as mensagens de aviso depois de alguns segundos
var aviso = document.querySelector(".flash");
if (aviso) {
  setTimeout(function () {
    aviso.style.display = "none";
  }, 5000);
}

// Botão de mostrar/ocultar senha (página de login)
var botaoSenha = document.getElementById("ver-senha");
if (botaoSenha) {
  botaoSenha.addEventListener("click", function () {
    var campo = document.getElementById("senha");
    if (campo.type === "password") {
      campo.type = "text";
      botaoSenha.textContent = "Ocultar";
    } else {
      campo.type = "password";
      botaoSenha.textContent = "Mostrar";
    }
  });
}
