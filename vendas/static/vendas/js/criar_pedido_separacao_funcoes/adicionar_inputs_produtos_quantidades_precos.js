document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("pedido_form").addEventListener("submit", validarFormulario);
    document.getElementById("cliente_input").addEventListener("input", setClienteId);
});

function adicionarInput() {
    var container = document.getElementById("inputs_container");
    var novoInput = document.createElement("div");
    novoInput.classList.add("produto-linha");

    novoInput.innerHTML = `
        <input type="text" list="nomes_produtos" placeholder="Selecione um Produto" class="produto_input" name="nome_produto" oninput="setProductInfo(this)" onblur="validarProduto(this)">
        <input type="text" placeholder="Código do Produto" class="codigo_produto_input" name="codigo_produto" readonly tabindex="-1">
        <input type="text" placeholder="Quantidade da Caixa" class="quantidade_caixa_input" name="quantidade_caixa" readonly tabindex="-1">
        <input type="number" placeholder="Quantidade" class="quantidade_input" name="quantidade_produto" oninput="calcularQuantidadeCaixas(this)">
        <input type="text" placeholder="Quantidade de Caixas" class="quantidade_caixas_calculada" name="quantidade_caixas" readonly tabindex="-1">
        <span class="icone-erro" style="display: none;">&#9888;</span>
        <button type="button" class="remove-button" onclick="removerLinha(this)">X</button>
    `;

    container.appendChild(novoInput);
}

function setProductInfo(input) {
    var datalist = document.getElementById("nomes_produtos");
    var options = datalist.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === input.value) {
            input.nextElementSibling.value = options[i].getAttribute('data-code');
            input.nextElementSibling.nextElementSibling.value = options[i].getAttribute('data-box-quantity');
            break;
        }
    }
}

function validarProduto(input) {
    var datalist = document.getElementById("nomes_produtos");
    var options = datalist.options;
    var valorValido = false;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === input.value) {
            valorValido = true;
            break;
        }
    }
    if (!valorValido) {
        input.value = '';
        input.nextElementSibling.value = '';
        input.nextElementSibling.nextElementSibling.value = '';
        input.nextElementSibling.nextElementSibling.nextElementSibling.value = ''; // limpa o campo de quantidade
        input.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.value = ''; // limpa o campo de quantidade de caixas
        alert("Por favor, selecione um produto válido da lista.");
    }
}

function calcularQuantidadeCaixas(input) {
    var quantidade = input.value;
    var quantidadeCaixa = input.previousElementSibling.value;
    var quantidadeCaixasInput = input.nextElementSibling;
    var iconeErro = quantidadeCaixasInput.nextElementSibling;

    if (quantidade && quantidadeCaixa) {
        var quantidadeCaixas = quantidade / quantidadeCaixa;
        quantidadeCaixasInput.value = quantidadeCaixas.toFixed(1);

        if (quantidadeCaixas % 1 !== 0) {
            iconeErro.style.display = 'inline';
        } else {
            iconeErro.style.display = 'none';
        }
    } else {
        quantidadeCaixasInput.value = '';
        iconeErro.style.display = 'none';
    }

}


function calcularTotal() {
    var inputsQuantidade = document.querySelectorAll('.quantidade_input');
    var inputsCaixa = document.querySelectorAll('.quantidade_caixas_calculada');
    var quantidades_somas = 0;
    var quantidades_caixas_somadas = 0;

    for (var i = 0; i < inputsQuantidade.length; i++) {
        var quantidade = parseFloat(inputsQuantidade[i].value) || 0; // Converter para número ou 0 se não for válido
        var quantidadeCaixa = parseFloat(inputsCaixa[i].value) || 0; // Converter para número ou 0 se não for válido

        quantidades_somas += quantidade;
        quantidades_caixas_somadas += quantidadeCaixa;
    }

    document.getElementById('quantidade_total').innerText = 'Quantidade Total Unidades: ' + quantidades_somas.toString();
    document.getElementById('caixas_total').innerText = 'Quantidade Total Caixas: ' + quantidades_caixas_somadas.toString();

    document.getElementById('quant_caixas_total').value = quantidades_caixas_somadas.toString();
}


function setClienteId() {
    var clienteInput = document.getElementById("cliente_input");
    var datalist = document.getElementById("nomes_clientes");
    var options = datalist.options;
    for (var i = 0; i < options.length; i++) {
        if (options[i].value === clienteInput.value) {
            document.getElementById("cliente_id").value = options[i].getAttribute('data-id');
            break;
        }
    }
}

function removerLinha(button) {
    var linha = button.parentElement;
    linha.remove();
}

function validarFormulario(event) {
    var inputsRegime = document.getElementById('regime_input');
    var inputsProduto = document.querySelectorAll(".produto_input");
    var inputsQuantidade = document.querySelectorAll(".quantidade_input");
    var iconesErro = document.querySelectorAll(".icone-erro");
    var clienteId = document.getElementById("cliente_id").value;
    const checkbox = document.getElementById('amostra_checkbox');

    calcularTotal();

    if (!inputsRegime.value) {
        alert("Selecione um regime.");
        event.preventDefault();
        return;
    }

    var todosPreenchidos = true;
    inputsProduto.forEach(function(input) {
        if (!input.value) {
            todosPreenchidos = false;
            input.classList.add("input-erro");
        } else {
            input.classList.remove("input-erro");
        }
    });

    inputsQuantidade.forEach(function(input) {
        if (!input.value) {
            todosPreenchidos = false;
            input.classList.add("input-erro");
        } else {
            input.classList.remove("input-erro");
        }
    });

    if (checkbox.checked) {
        console.log('modo de amostras - nao respeitar quantidade caixa')
    } else {
        var erroCaixa = Array.from(iconesErro).some(function(icone) {
        return icone.style.display === 'inline';
    });
    }

    if (!clienteId) {
        alert("Selecione um cliente.");
        event.preventDefault();
        return;
    }

    if (!todosPreenchidos) {
        alert("Preencha todos os campos de produto e quantidade.");
        event.preventDefault();
    } else if (erroCaixa) {
        alert("Há erros na quantidade de caixas. Verifique e corrija.");
        event.preventDefault();
    }
}
