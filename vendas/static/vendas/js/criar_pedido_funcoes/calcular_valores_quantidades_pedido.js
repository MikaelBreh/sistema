// Esse scritp serve para calcular os totais dentro do pedido:

function calcularTotal() {
    var inputsQuantidade = document.querySelectorAll('.quantidade_input');
    var inputsPreco = document.querySelectorAll('.preco_input');
    var total = 0;
    var quantidades_somas = 0;

    for (var i = 0; i < inputsQuantidade.length; i++) {
        var quantidade = parseFloat(inputsQuantidade[i].value) || 0; // Converter para número ou 0 se não for válido
        var preco = parseFloat(inputsPreco[i].value) || 0; // Converter para número ou 0 se não for válido

        quantidades_somas += quantidade;

        total += quantidade * preco;
    }

    document.getElementById('total_pedido').innerText = 'Total do Pedido: R$ ' + total.toFixed(2); // Exibir o total formatado com 2 casas decimais
    document.getElementById('quantidade_total').innerText = 'Quantidade Total: ' + quantidades_somas.toString();
}
