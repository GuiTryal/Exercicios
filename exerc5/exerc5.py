from groq import Groq
import json

from exerc5tools import buscar_produto, verificar_estoque


client = Groq(api_key="SUA_CHAVE_AQUI")


tools = [
    {
        "type": "function",
        "function": {
            "name": "buscar_produto",
            "description": "Verifica se um produto existe no estoque",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome_produto": {"type": "string"}
                },
                "required": ["nome_produto"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verificar_estoque",
            "description": "Retorna a quantidade em estoque do produto",
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
            "content": "Você é um assistente de estoque. Sempre use as funções disponíveis para responder perguntas sobre produtos."
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
        existe = buscar_produto(**argumentos)

        if existe:
            quantidade = verificar_estoque(argumentos["nome_produto"])
            print("Temos", quantidade, "unidades em estoque.")
        else:
            print("Produto não encontrado.")

    elif nome_funcao == "verificar_estoque":
        quantidade = verificar_estoque(**argumentos)

        if quantidade is None:
            print("Produto não encontrado.")
        else:
            print("Quantidade em estoque:", quantidade)

    else:
        print("Função desconhecida:", nome_funcao)

else:
    print(message.content)