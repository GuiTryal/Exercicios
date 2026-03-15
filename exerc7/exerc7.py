# exerc7.py
from groq import Groq
import os
import json
from dotenv import load_dotenv

from exerc7tools import buscar_clima



client = Groq(api_key="SUA_CHAVE_AQUI")

tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_clima",
            "description": "Busca o clima de uma cidade (base fictícia). Recebe 'cidade' como string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {"type": "string"}
                },
                "required": ["cidade"]
            }
        }
    }
]

mensagem = input("Pergunta: ").strip()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": "Você é um assistente de clima. Sempre que o usuário pedir o clima de uma cidade, USE a function 'buscar_clima' com o parâmetro 'cidade'. Não invente formatos diferentes."
        },
        {"role": "user", "content": mensagem}
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message


if message.tool_calls:
    tool_call = message.tool_calls[0]
    nome_funcao = tool_call.function.name
    argumentos = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}

    if nome_funcao == "buscar_clima":
        cidade = argumentos.get("cidade", "")
        resultado = buscar_clima(cidade)
        if resultado is None:
            print("Cidade não encontrada na base de dados.")
        else:
            print(f"Clima em {cidade}: {resultado}")
    else:
        print("Função desconhecida solicitada pelo modelo:", nome_funcao)


else:
    print(message.content)