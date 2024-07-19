// Esse script serve para adicionar inputs de produtos preço e quantidades no pedido:
function adicionarInput() {
    var container = document.getElementById("inputs_container");
    var novoInput = document.createElement("div");

    novoInput.innerHTML = `
        <input type="text" list="nomes_produtos" placeholder="Selecione um Produto" class="produto_input" name="nome_produto">
        <input type="number" placeholder="Quantidade" class="quantidade_input" name="quantidade_produto">
        <input type="number" placeholder="Preço" class="preco_input" name="preco_produto">
    `;

    container.appendChild(novoInput);
}

