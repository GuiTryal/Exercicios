eventos = []

def criar_evento(titulo: str, data: str):

    evento = {
        "titulo": titulo.strip(),
        "data": data.strip()
    }

    eventos.append(evento)

    return evento


def listar_eventos():

    return eventos.copy()