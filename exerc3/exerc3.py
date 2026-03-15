from groq import Groq
import json

from exerc3tools import celsius_para_fahrenheit, fahrenheit_para_celsius


client = Groq(api_key="SUA_CHAVE_AQUI")

tools = [
    {
        "type": "function",
        "function": {
            "name": "celsius_para_fahrenheit",
            "description": "Converte temperatura de Celsius para Fahrenheit",
            "parameters": {
                "type": "object",
                "properties": {
                    "celsius": {"type": "number"}
                },
                "required": ["celsius"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fahrenheit_para_celsius",
            "description": "Converte temperatura de Fahrenheit para Celsius",
            "parameters": {
                "type": "object",
                "properties": {
                    "fahrenheit": {"type": "number"}
                },
                "required": ["fahrenheit"]
            }
        }
    }
]


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


if message.tool_calls:

    tool_call = message.tool_calls[0]

    nome_funcao = tool_call.function.name
    argumentos = json.loads(tool_call.function.arguments)

    if nome_funcao == "celsius_para_fahrenheit":
        resultado = celsius_para_fahrenheit(**argumentos)
        print("Resultado:", resultado)

    elif nome_funcao == "fahrenheit_para_celsius":
        resultado = fahrenheit_para_celsius(**argumentos)
        print("Resultado:", resultado)

    else:
        print("Função desconhecida:", nome_funcao)

else:
    print(message.content)