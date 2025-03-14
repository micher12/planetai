import torch
from pln import BertFeatureExtractor, combinar_textos
from data_handler import carregar_csv, preparar_dataloaders
from model import ClassificadorNoticias
from train import treinar_modelo
from utils import avaliar_modelo, classificar_noticia

def main():
    # Configurações
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    class_mapping = {0: "Ruim", 1: "Boa", 2: "Irrelevante"}
    
    # Carregar dados
    print("Carregando dados...")
    dados = carregar_csv("data_sintetica.csv")
    textos = combinar_textos(dados)
    labels = dados['class'].tolist()
    
    # Extração de features
    print("\nExtraindo features...")
    feature_extractor = BertFeatureExtractor()
    features = feature_extractor.extract_features(textos)
    
    # Preparar modelo
    print("\nPreparando modelo...")
    model = ClassificadorNoticias(
        input_dim=features.shape[1],
        hidden_dim=256,
        n_classes=3
    )
    
    # Treinar
    train_loader, val_loader = preparar_dataloaders(features, labels)
    model, historico = treinar_modelo(
        model, train_loader, val_loader, device, epochs=10
    )
    
    # Avaliar
    print("\nAvaliando modelo...")
    avaliar_modelo(model, feature_extractor, textos, labels, device)
    
    # Exemplo de uso
    print("\nTestando classificação:")
    resultado = classificar_noticia(
        model, feature_extractor,
        titulo="Novo método de reciclagem revoluciona indústria",
        conteudo="Empresa desenvolve técnica que aumenta eficiência em 300%...",
        device=device
    )
    
    print(f"Classificação: {class_mapping[resultado['classe']]}")
    print(f"Confiança: {resultado['confianca']:.1f}%")

if __name__ == "__main__":
    main()