estoque = {
    "notebook": 5,
    "mouse": 20,
    "teclado": 8
}

def buscar_produto(nome_produto: str):
    
    chave = nome_produto.lower().strip()
    return chave in estoque

def verificar_estoque(nome_produto: str):
    
    chave = nome_produto.lower().strip()
    return estoque.get(chave)