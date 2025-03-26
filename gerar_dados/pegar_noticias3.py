import os
from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import pandas as pd
import math
import requests
import socket
import urllib.parse
import json

load_dotenv()
apikey = os.getenv("NEWSDATA_API_KEY")

api = NewsDataApiClient(apikey=apikey)

page=None



def identificar_protocolo_url(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        return {
            'protocolo_url': parsed_url.scheme,
            'hostname': parsed_url.hostname
        }
    except Exception as e:
        print(f"Erro ao identificar protocolo da URL: {e}")
        return None

def identificar_protocolo_socket(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname
        porta = 443 if parsed_url.scheme == 'https' else 80
        
        # Criar socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Tentar conectar
        sock.connect((hostname, porta))
        
        detalhes = {
            'familia_socket': sock.family,
            'tipo_socket': sock.type,
            'protocolo_socket': sock.proto
        }
        
        sock.close()
        return detalhes
    
    except Exception as e:
        print(f"Erro com socket: {e}")
        return None

def mapear_protocolos_socket():
    return {
        socket.IPPROTO_TCP: 'TCP',
        socket.IPPROTO_UDP: 'UDP',
        socket.IPPROTO_ICMP: 'ICMP',
        0: 'Padrão/Não Especificado'
    }

def identificar_protocolos(url):
    """
    Função consolidada para identificação de protocolos
    """
    print("Identificando protocolos:")
    
    # Identificar protocolo da URL
    resultado_url = identificar_protocolo_url(url)
    
    # Identificar detalhes do socket
    resultado_socket = identificar_protocolo_socket(url)
    
    # Mapear protocolo de socket
    mapeamento_protocolos = mapear_protocolos_socket()
    
    # Adicionar nome legível ao protocolo do socket
    if resultado_socket and 'protocolo_socket' in resultado_socket:
        protocolo_socket = resultado_socket['protocolo_socket']
        resultado_socket['protocolo_nome'] = mapeamento_protocolos.get(
            protocolo_socket, 
            f'Protocolo Desconhecido ({protocolo_socket})'
        )
    
    return {
        'protocolo_url': resultado_url,
        'detalhes_socket': resultado_socket
    }

url = f"https://twelvecommerce.vercel.app/api/checkout"

protocolo = identificar_protocolos(url)

while True:
    response = api.news_api(q="meio ambiente" , country = "br", language="pt", page=page)
  

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
        
