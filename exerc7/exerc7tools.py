clima = {
    "sao paulo": "24°C e nublado",
    "bauru": "30°C e ensolarado",
    "curitiba": "18°C e chuvoso"
}

def buscar_clima(cidade: str):
    
    chave = cidade.lower().strip()
   
    chave = chave.replace("á", "a").replace("ã", "a").replace("â", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ç", "c")
    return clima.get(chave)