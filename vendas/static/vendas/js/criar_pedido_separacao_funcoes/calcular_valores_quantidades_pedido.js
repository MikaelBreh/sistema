// Esse scritp serve para calcular os totais dentro do pedido:

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
}
