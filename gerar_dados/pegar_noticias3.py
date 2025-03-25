import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import pandas as pd
import math

load_dotenv()
apikey = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(apikey=apikey)

page=None

while True:
    response = api.news_api( q='meio+ambiente' , country = "br", language="pt", page=page)

    resultados = response['totalResults']

    print(f"Notícias encontradas: {resultados}")

    todos_artigos = response['results']
    total_results = response['totalResults']
    total_pages = math.ceil(total_results / 10)

    for artigo in todos_artigos:
        titulo = artigo['title']
        link = artigo['link']
        descricao = artigo['description']
        data = artigo['pubDate']

        print(f"\nTítulo: {titulo}")
        print(f"Descrição: {descricao}")
        print(f"Link: {link}")
        print(f"Data: {data}")
        while True:
            resposta = input("Digite a sua classificação (sair ou 's' para skipar): ")
            if resposta in ["0", "1", "2", "s", "sair"]:
                break
        if resposta == "s":
            continue
        if resposta == "sair":
            break

        print(f"\nResposta: {resposta}")

        dados = {
            'title': titulo,
            'date': data,
            'url': link,
            'content': descricao,
            'class': resposta
        }

        df = pd.DataFrame([dados])

        df.to_csv(
            "gerar_dados/noticias3.csv",
            index=False,
            mode='a' if os.path.exists("gerar_dados/noticias3.csv") else 'w',
            header=not os.path.exists("gerar_dados/noticias3.csv"),
            encoding='utf-8-sig'
        )

    if resposta == "sair":
        break

    page = response.get('nextPage',None)

    if not page:
        break
        
