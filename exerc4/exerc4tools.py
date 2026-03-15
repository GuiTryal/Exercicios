produtos = {
    "notebook": 4500,
    "mouse": 80,
    "teclado": 150
}

def buscar_produto(nome_produto: str):
    
    chave = nome_produto.lower().strip()
    if chave in produtos:
        return produtos[chave]
    return None