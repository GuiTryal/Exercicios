import os
import json
from dotenv import load_dotenv
from groq import Groq

from exerc4tools import buscar_produto


load_dotenv()

client = Groq(api_key="SUA_CHAVE_AQUI")


tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_produto",
            "description": "Busca o preço de um produto pelo nome",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_produto": {"type": "string"}
                },
                "required": ["nome_produto"]
            }
        }
    }
]

mensagem = input("Pergunta: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": "Você é um assistente que responde com o preço de produtos. Sempre use a function disponível quando o usuário pedir preço de um produto."
        },
        {
            "role": "user",
            "content": mensagem
        }
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message


if message.tool_calls:
    tool_call = message.tool_calls[0]
    nome_funcao = tool_call.function.name
    argumentos = json.loads(tool_call.function.arguments)

    if nome_funcao == "buscar_produto":
        preco = buscar_produto(**argumentos)
        if preco is None:
            print("Produto não encontrado.")
        else:
            print(f"Preço: R$ {preco}")
    else:
        print("Função desconhecida solicitada pelo modelo:", nome_funcao)
else:
    
    print(message.content)