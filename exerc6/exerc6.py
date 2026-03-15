from groq import Groq
import json

from exerc6tools import criar_evento, listar_eventos

client = Groq(api_key="SUA_CHAVE_AQUI")

tools = [
    {
        "type": "function",
        "function": {
            "name": "criar_evento",
            "description": "Cria um evento com título e data",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"},
                    "data": {"type": "string"}
                },
                "required": ["titulo", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_eventos",
            "description": "Lista todos os eventos",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

print("Agenda iniciada. Digite 'sair' para encerrar.")

while True:

    pergunta = input("Pergunta: ")

    if pergunta.lower() == "sair":
        break

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente de agenda. Se o usuário quiser criar um evento, chame criar_evento. Se quiser ver eventos, chame listar_eventos."
            },
            {
                "role": "user",
                "content": pergunta
            }
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_call = message.tool_calls[0]
        nome_funcao = tool_call.function.name

        argumentos = {}

        if tool_call.function.arguments:
            argumentos = json.loads(tool_call.function.arguments)

        if nome_funcao == "criar_evento":

            titulo = argumentos.get("titulo", "Evento")
            data = argumentos.get("data", "Data não informada")

            evento = criar_evento(titulo, data)

            print("Evento criado:", evento["titulo"], "-", evento["data"])

        elif nome_funcao == "listar_eventos":

            eventos = listar_eventos()

            if len(eventos) == 0:
                print("Não há eventos na agenda.")
            else:
                print("Seus eventos:")
                for i, e in enumerate(eventos, start=1):
                    print(f"{i}. {e['titulo']} - {e['data']}")

    else:
        print(message.content)