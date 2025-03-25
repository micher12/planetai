from pipeline import fazer_previsao, inicializarModelo, BertFeatureExtractor

def main():
    print("\nIniciando modelo...")

    model, _ = inicializarModelo()

    feature_extractor = BertFeatureExtractor()

    while True:
        texto_exemplo = input("\nDigite uma notícia para análise de sentimento (ou 'sair' para encerrar): ")
        if texto_exemplo.lower() == 'sair':
            break

        sentimento, probabilidades = fazer_previsao(texto_exemplo, model, feature_extractor)

        print(f"\nNotícia: {texto_exemplo}")
        print(f"Sentimento: {sentimento}")
        print(f"Probabilidades: Negativa {probabilidades[0]:.2f}, Positiva {probabilidades[1]:.2f}, Irrelevante {probabilidades[2]:.2f}")

main()