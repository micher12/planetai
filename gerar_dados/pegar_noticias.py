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

# Configurações
logging.basicConfig(level=logging.ERROR)
output_dir = os.path.join(os.getcwd(), 'APS', 'gerar_dados')
os.makedirs(output_dir, exist_ok=True)
csv_path = os.path.join(output_dir, 'noticias.csv')
brazil_tz = pytz.timezone('America/Sao_Paulo')

def format_date(published_date):
    """Formata a data para o padrão brasileiro"""
    try:
        dt = datetime.strptime(published_date, "%Y-%m-%dT%H:%M:%SZ")
        dt_brazil = dt.astimezone(brazil_tz)
        return dt_brazil.strftime("%d/%m/%Y %H:%M:%S")
    except Exception:
        return "Data desconhecida"

def process_news():

    dados = []

    apikey = "f718830f9ab52ea8530516eda91b655b"

    to_date = (datetime.now(timezone.utc) - timedelta(days=5)).strftime("%Y-%m-%dT%H:%M:%SZ")
    from_date = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://gnews.io/api/v4/search?q=meio+ambiente&lang=pt&country=br&from={from_date}&to={to_date}&max=10&apikey={apikey}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):

            title = articles[i]['title']
            print(f"Titulo: {title}")

            content = articles[i]['content'] + " "+articles[i]['description']
            print(f"Conteudo: {content}")

            try:
                # Montar texto para classificação
                texto = f"""
                Título: {title}
                Conteúdo: {content}
                """
                
                # Classificação
                resposta = classify(texto.strip())

                print(f"Resposta: {resposta}")
                
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
    news = process_news()
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