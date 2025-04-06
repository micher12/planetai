from pipeline import fazer_previsao, inicializarModelo, BertFeatureExtractor
import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
from flask import Flask, jsonify


model, _ = inicializarModelo()

feature_extractor = BertFeatureExtractor()

load_dotenv()
apikey = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(apikey=apikey)


def classificar(text):

    sentimento, _ = fazer_previsao(text, model, feature_extractor)

    return sentimento


def pegar_noticias():
    news = api.news_api(category="environment", country="br", language="pt")

    dados = []

    artigos = news['results']

    for artigo in artigos:  # Limitando artigos
        titulo = artigo['title']
        link = artigo['link']
        descricao = artigo['description']
        data = artigo['pubDate']

        text = f"{titulo} {descricao}"

        classificacao = classificar(text)

        dados.append({
            'title': titulo,
            "description": descricao,
            'url': link,
            'class': classificacao,
            'date': data,
        })

    return dados

app = Flask(__name__)

@app.route('/api/noticias', methods=['POST'])
def response():
    dados = pegar_noticias()
    return jsonify(dados)

if __name__ == '__main__':
    app.run(debug=True)
