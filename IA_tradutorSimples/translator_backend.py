

import requests

def traduzir_texto(texto, idioma_destino='pt'):
    url = "https://api.mymemory.translated.net/get"

    # Parâmetros para a requisição
    params = {
        "q": texto,
        "langpair": "en|pt" if idioma_destino == 'pt' else "pt|en"
    }

    # Faz a requisição à API MyMemory
    response = requests.get(url, params=params)

    # Trata a resposta da API
    if response.status_code == 200:
        data = response.json()
        traducao = data.get("responseData", {}).get("translatedText")
        return traducao
    else:
        raise Exception("Erro na tradução: Não foi possível obter a tradução.")


