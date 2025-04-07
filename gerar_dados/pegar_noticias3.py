import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import pandas as pd
import math
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pipeline import fazer_previsao, inicializarModelo, BertFeatureExtractor

load_dotenv()
apikey = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(apikey=apikey)

page=None

model, _ = inicializarModelo()

feature_extractor = BertFeatureExtractor()

i = 0

while True:

    response = api.news_api(category="environment" , country = "br", language="pt", page=page)

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
        text = f"{titulo} {descricao}"

        print(f"\nTítulo: {titulo}")
        print(f"Descrição: {descricao}")
        print(f"Link: {link}")
        print(f"Data: {data}")
        
        resposta, _ = fazer_previsao(text, model, feature_extractor)

        print(f"\nResposta: {resposta}")

        sentimentos = ['Negativa', 'Positiva', 'Irrelevante']

        classify = sentimentos.index(resposta) if resposta in sentimentos else None

        dados = {
            'title': titulo,
            'date': data,
            'url': link,
            'content': descricao,
            'class': classify
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

