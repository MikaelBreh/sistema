# Exibindo os resultados
for produto in entrada_produtos_validados:
    print(f"Produto: {produto['produto__name']}, Quantidade Unitária: {produto['quantidade_unitaria']}")



# Exibir os resultados com o objeto real
for item in misto_items:
    print(f"Produto: {item.produto_misto}, Quantidade Unitária: {item.quantidade_unitaria}")



# Exibir as informações
print(f"Produto: {produto}, Quantidade: {quantidade}, Quantidade de Caixas: {quantidade_de_caixas}")