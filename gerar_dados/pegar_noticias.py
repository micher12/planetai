import os
import pytz
from datetime import datetime
from gnews import GNews
import pandas as pd
from classify import classify
import logging
import json
import urllib.request
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from urllib.request import urlopen

# Configurações
logging.basicConfig(level=logging.ERROR)
output_dir = os.path.join(os.getcwd(), 'gerar_dados')
os.makedirs(output_dir, exist_ok=True)
brazil_tz = pytz.timezone('America/Sao_Paulo')

def format_date(published_date):
    """Formata a data para o padrão brasileiro"""
    try:
        dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ")
        dt_brazil = dt.astimezone(brazil_tz)
        return dt_brazil.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return "Data desconhecida"
    
def process_news_newsapi():
    dados = []
    load_dotenv()
    
    apikey = os.getenv("NEWSAPI_API_KEY")
    if not apikey:
        raise ValueError("Chave de API não encontrada. Configure a variável de ambiente NEWSAPI_API_KEY.")

    # Calcula as datas com 300 e 500 dias atrás
    to_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
    from_date = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")
    
    query = 'desmatamento+AND+meio+ambiente'  # Query adaptada para formato NewsAPI

    # URL da NewsAPI com parâmetros ajustados
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&"
        f"language=pt&"
       #f"from={from_date}&"
        #f"to={to_date}&"
        f"pageSize=100&"
        f"sortBy=popularity&"
        f"apiKey={apikey}"
    )

    try:
        with urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            
            # Verifica se a requisição foi bem-sucedida
            if data.get('status') != 'ok':
                raise Exception(f"Erro na API: {data.get('message', 'Status desconhecido')}")
            
            articles = data["articles"]

            results = data["totalResults"]

            for article in articles:
                print(f"\nTotal de resultados: {results}")
                title = article.get('title', 'Título não disponível')
                content = f"{article.get('content', '')} {article.get('description', '')}"
                published_at = article.get('publishedAt', '')
                url = article.get('url', '')

                print(f"\nTitle: {title}")
                print(f"Content: {content}")
                print(f"Link: {url}")
                print(f"Publicado: {published_at}")

                try:
                    # texto = f"Título: {title} Conteúdo: {content}"
                    # resposta = classify(texto.strip())  # Função de classificação existente

                    # Classificação
                    while True:
                        resposta = input("Digite a sua classificação (sair ou 's' para skipar): ")
                        if resposta in ["0", "1", "2", "s", "sair"]:
                            break
                    if resposta == "s":
                        continue
                    if resposta == "sair":
                        return dados

                    print(f"\nResposta: {resposta}")

                    dados.append({
                        'title': title,
                        'date': format_date(published_at),  # Função de formatação existente
                        'url': article.get('url', ''),
                        'content': content,
                        'class': resposta
                    })
                except Exception as e:
                    print(f"Erro processando artigo '{title}': {str(e)}")
                    continue

    except Exception as e:
        print(f"Erro na requisição à API: {str(e)}")
        raise

    return dados

def process_news_GNEWS():

    dados = []

    load_dotenv()
    apikey = os.getenv("GNEWS_API_KEY")
    if not apikey:
        raise ValueError("Chave de API não encontrada. Configure a variável de ambiente GNEWS_API_KEY.")

    to_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    from_date = (datetime.now(timezone.utc) - timedelta(days=70)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    query = "desmatamento+AND+meio+ambiente" #meio+ambiente

    #url = f"https://gnews.io/api/v4/search?q={query}&lang=pt&from={from_date}&to={to_date}&country=br&max=10&apikey={apikey}"
    url = f"https://gnews.io/api/v4/search?q={query}&lang=pt&country=br&max=10&apikey={apikey}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):

            title = articles[i]['title']
            print(f"\nTitulo: {title}")
            link = articles[i]["url"]
            content = articles[i]['content'] + " "+articles[i]['description']
            print(f"Conteudo: {content}")
            print(f"Link: {link}")
            print("Publicado em: "+articles[i]['publishedAt'])

            try:


                # Classificação
                while True:
                    resposta = input("Digite a sua classificação (sair ou 's' para skipar): ")
                    if resposta in ["0", "1", "2", "s", "sair"]:
                        break
                if resposta == "s":
                    continue
                if resposta == "sair":
                    return dados

                print(f"\nResposta: {resposta}")
                
                dados.append({
                    'title': title,
                    'date': format_date(articles[i]['publishedAt']),
                    'url': articles[i]['url'],
                    'content': content,
                    'class': resposta
                })
            
            except Exception as e:
                print(f"Erro processando artigo: {str(e)}")
                continue

    return dados

def save_news():
    """Salva os dados no CSV"""
    csv_path = os.path.join(output_dir, 'noticias.csv')
    news = process_news_GNEWS()
    if news:
        df = pd.DataFrame(news)
        df.to_csv(
            csv_path,
            index=False,
            mode='a' if os.path.exists(csv_path) else 'w',
            header=not os.path.exists(csv_path),
            encoding='utf-8-sig'
        )
        return len(df)
    return 0

if __name__ == "__main__":
    count = save_news()
    print(f"{count} notícias processadas com sucesso!")