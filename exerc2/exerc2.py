from groq import Groq
import os
import json
from dotenv import load_dotenv

from exerc2tools import somar, subtrair, multiplicar, dividir


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


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
            "name": "subtrair",
            "description": "Subtrai o segundo número do primeiro",
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
    },
    {
        "type": "function",
        "function": {
            "name": "dividir",
            "description": "Divide o primeiro número pelo segundo",
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


def main():

    mensagem = input("Pergunta: ")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Você é uma calculadora. Sempre use as functions disponíveis para resolver operações matemáticas."
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

        if nome_funcao == "somar":
            resultado = somar(**argumentos)
            print("Resultado:", resultado)

        elif nome_funcao == "subtrair":
            resultado = subtrair(**argumentos)
            print("Resultado:", resultado)

        elif nome_funcao == "multiplicar":
            resultado = multiplicar(**argumentos)
            print("Resultado:", resultado)

        elif nome_funcao == "dividir":
            resultado = dividir(**argumentos)
            print("Resultado:", resultado)

        else:
            print("Função desconhecida:", nome_funcao)

    else:
        print(message.content)


if __name__ == "__main__":
    main()