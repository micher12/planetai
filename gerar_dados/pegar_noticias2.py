from pygooglenews import GoogleNews
from classify import classify
import pandas as pd
import os

gn = GoogleNews(lang="pt",country="br")

search = gn.topic_headlines("CAAqJggKIiBDQkFTRWdvSkwyMHZNREp3ZVRBNUVnVndkQzFDVWlnQVAB") # codigo para categoria meio ambiente

# Verifica se há resultados
if search and 'entries' in search:
    
    try:
        for i, noticia in enumerate(search['entries'], 1):
            print(noticia)
            print(f"\n**Notícia {i}:**")
            print(f"Título: {noticia.get('title', 'N/A')}")
            print(f"Data: {noticia.get('published', 'N/A')}")

            while True:
                resposta = input("Digite a sua classificação (sair ou 's' para skipar): ")
                if resposta in ["0","1","2", "s", "sair"]:
                    break

            #resposta = classify(str(noticia.get("title")))
            if(resposta == "s"):
                continue
            elif(resposta == "sair"):
                break

            print(f"Resposta: {resposta}")
            print("-" * 80)

            dados = {
                'title': noticia.get('title', 'N/A'),
                'date': noticia.get('published', 'N/A'),
                'url': "",
                'content': noticia.get('title', 'N/A'),
                'class': resposta
            }

            df = pd.DataFrame([dados])

            df.to_csv(
                "gerar_dados/noticias4.csv",
                index=False,
                mode='a' if os.path.exists("gerar_dados/noticias4.csv") else 'w',
                header=not os.path.exists("gerar_dados/noticias4.csv"),
                encoding='utf-8-sig'
            )

    except Exception as e:
        print("ERRO: "+str(e))

else:
    print("Nenhuma notícia encontrada.")