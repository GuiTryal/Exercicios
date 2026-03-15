from groq import Groq
import os
import json
from dotenv import load_dotenv

from exerc1tools import somar, multiplicar

# carregar variáveis do .env
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# definição das tools que o modelo pode usar
tools = [
    {
        "type": "function",
        "function": {
            "name": "somar",
            "description": "Soma dois números",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number"},
                    "num2": {"type": "number"}
                },
                "required": ["num1", "num2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multiplicar",
            "description": "Multiplica dois números",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number"},
                    "num2": {"type": "number"}
                },
                "required": ["num1", "num2"]
            }
        }
    }
]

# pergunta do usuário
mensagem = input("Pergunta: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": mensagem}
    ],
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message

# verificar se o modelo quer usar uma tool
if message.tool_calls:

    tool_call = message.tool_calls[0]

    nome_funcao = tool_call.function.name
    argumentos = json.loads(tool_call.function.arguments)

    if nome_funcao == "somar":
        resultado = somar(**argumentos)
        print("Resultado:", resultado)

    elif nome_funcao == "multiplicar":
        resultado = multiplicar(**argumentos)
        print("Resultado:", resultado)

    else:
        print("Função desconhecida:", nome_funcao)

else:
    print(message.content)