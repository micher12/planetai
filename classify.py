from pipeline import fazer_previsao, inicializarModelo, BertFeatureExtractor
import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort
from functools import wraps
from protocolo import getProtocolo
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model, _ = inicializarModelo()

feature_extractor = BertFeatureExtractor()

load_dotenv()
apikey = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(apikey=apikey)


def classificar(text):

    sentimento, _ = fazer_previsao(text, model, feature_extractor, device=device)

    return sentimento


def pegar_noticias():
    page = None

    dados = []

    while True:
        news = api.news_api(category="environment", country="br", language="pt", page=page)

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

        page = news.get('nextPage',None)

        if not page:
            break

    return dados

app = Flask(__name__)

API_KEY = os.getenv("MY_API_KEY")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header == f"Bearer {API_KEY}":
            return f(*args, **kwargs)
        else:
            abort(401, description="Autorização Inválida.")
    return decorated

@app.route('/api/noticias', methods=['POST'])
@require_api_key
def noticias_response():
    dados = pegar_noticias()
    return jsonify(dados)

@app.route('/api/protocolo', methods=['POST'])
@require_api_key
def protocolo_response():
    protocolo, versao = getProtocolo()
    return jsonify(protocolo, versao)


# app.rung(debug=True) # use para debugar


app.run(host="0.0.0.0", port=5000, debug=False) # use para expor o ip da máquina, juntamente no ngrok para tornar uma api pública.
