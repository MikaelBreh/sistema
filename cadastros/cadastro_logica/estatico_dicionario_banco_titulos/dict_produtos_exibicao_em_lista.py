# Diretamente relacionado ao arquivo exibicao_cadastros.html
# Esse arquivo visa criar e definir o dicionario que ditará os titulos,
# e os nomes das colunas no banco de dados
# Sendo assim, padrao:  Nome Produto(chave): Nome da coluna no banco de dados(valor)

# Dicionario da lista de exibicao de cadastros(Produtos):
dicionario_produtos = {
    #    'Nome Produto': 'name',
    'Codigo Produto': 'product_code',
    'Codigo de Barras': 'product_bar_code',
    'Codigo de Barras da Caixa': 'box_bar_code',
    'Quantidade na Caixa': 'box_quantity',
    'categoria': 'category',
}

dicionario_clientes = {
    'CNPJ': 'cnpj',
    'CEP': 'cep',
    'Regime': 'regime',
}

dicionario_fornecedores = {
    'CNPJ': 'cnpj',
    'CEP': 'cep',
    'Telefone': 'phone',
    'Email': 'email',
    'Endereco': 'address',
}

dicionario_materiais_de_trabalho = {
    'Unidade': 'unit',
    'Fornecedor': 'supplier',
    'Categoria': 'category',
}

dicionario_vendedeores = {
    'CPF': 'cpf',
    'Telefone': 'phone',
    'Email': 'email',
    'Endereco': 'address',
}