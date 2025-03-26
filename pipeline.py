from nlp import AutoTokenizer, BertFeatureExtractor
from model import ClassificadorNoticiasAvancado
from train import treinar_modelo_completo
import torch
import os

def inicializarModelo():
    # Definir o dispositivo (GPU ou CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Usando dispositivo: {device}")

    # Inicializar modelo
    
    model_path = "melhor_modelo_noticias.pth"

    # Criar diretório se necessário (se o caminho tiver subdiretórios)
    if os.path.dirname(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

    # Verificar se o arquivo do modelo existe
    if os.path.exists(model_path):
        print("\nInicializando modelo de classificação...")
        # Carregar o checkpoint do arquivo
        checkpoint = torch.load(model_path)

        # Instanciar o modelo com os parâmetros de arquitetura
        model = ClassificadorNoticiasAvancado(
            input_dim=1024,
            hidden_dim=256,
            n_classes=3,
            use_attention=True
        )

        # Carregar os pesos salvos no modelo
        model.load_state_dict(checkpoint['model_state_dict'])

    else:
        print("\nNenhum modelo encontrado, iniciando novo modelo...")
        model = ClassificadorNoticiasAvancado(
            input_dim=1024,
            hidden_dim=256,
            n_classes=3,
            use_attention=True
        )

    # Mover o modelo para o dispositivo (ex: CPU ou GPU)
    model = model.to(device)

    return model, device

def fazer_previsao(texto, modelo, extrator, device='cuda'):

    # Converter para lista (o extrator espera uma lista)
    texto = [texto]
    
    # Extrair features
    features, masks = extrator.extract_features(texto, return_all_tokens=True)
    
    # Converter para tensor
    features_cls = torch.tensor(features[:, 0, :]).float().to(device)
    all_tokens = torch.tensor(features).float().to(device)
    attn_mask = torch.tensor(masks).float().to(device)
    
    # Fazer previsão
    modelo.eval()
    with torch.no_grad():
        outputs = modelo(features_cls, all_tokens, attn_mask)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        prediction = torch.argmax(probs, dim=1).item()
    
    # Mapear para rótulos
    sentimentos = ['Negativa', 'Positiva', 'Irrelevante']
    return sentimentos[prediction], probs[0].cpu().numpy()

def main():

    model, device = inicializarModelo()

    feature_extractor = BertFeatureExtractor()

    model = treinar_modelo_completo(
        model,
        device,
        feature_extractor,
        caminho_arquivo="gerar_dados/noticias.csv",
        epochs=16,
        batch_size=20,
        learning_rate=1e-5
    )

    texto_exemplo = "Desmatamento na Amazônia atinge maiores níveis em uma década, preocupando ambientalistas."
    sentimento, probabilidades = fazer_previsao(texto_exemplo, model, feature_extractor)

    print(f"Notícia: {texto_exemplo}")
    print(f"Sentimento: {sentimento}")
    print(f"Probabilidades: Negativa {probabilidades[0]:.2f}, Positiva {probabilidades[1]:.2f}, Irrelevante {probabilidades[2]:.2f}")

#main()