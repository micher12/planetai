import requests
import socket

def getProtocolo():
    response = requests.get(f"https://newsdata.io/api/1/news")
    versao = response.raw.version
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
    s.connect(("newsdata.io", 80))

    protocolo = ("TCP" if s.type == socket.SOCK_STREAM else "UDP")

    return protocolo, versao
    