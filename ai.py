import torch
from model import ClassificadorNoticias  # Importar a classe do modelo
from pln import BertFeatureExtractor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_mapping = {0: "Ruim", 1: "Boa", 2: "Irrelevante"}

# Carregar o checkpoint
checkpoint = torch.load("APS/PlanetAI.pth", map_location=device)

required_keys = ['model_state_dict', 'input_dim', 'hidden_dim', 'n_classes']
for key in required_keys:
    if key not in checkpoint:
        raise ValueError(f"Checkpoint corrompido! Chave faltando: {key}")

# Recriar o modelo com parâmetros padrão (caso não existam no checkpoint)
model = ClassificadorNoticias(
    input_dim=checkpoint['input_dim'],
    hidden_dim=checkpoint['hidden_dim'],
    n_classes=checkpoint['n_classes']
)

# Carregar os pesos
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

# Inicializar extrator de features
feature_extractor = BertFeatureExtractor()

def classificar_noticia(titulo, conteudo):
    texto = f"{titulo} {conteudo}"
    
    # Extrair features
    features = feature_extractor.extract_features([texto])
    
    # Converter para tensor
    features_tensor = torch.FloatTensor(features).to(device)
    
    # Fazer predição
    with torch.no_grad():
        outputs = model(features_tensor)
        probabilidades = torch.nn.functional.softmax(outputs, dim=1)
        confianca, classe = torch.max(probabilidades, dim=1)
    
    return {
        'classe': classe.item(),
        'confianca': confianca.item() * 100
    }

# Teste

while(True):

    text = input("Digite o titulo da reportagem: ")

    res = classificar_noticia(
        titulo=f"{text}",
        conteudo=""
    )

    print(f"Classificação: {class_mapping[res['classe']]}")
    print(f"Confiança: {res['confianca']:.1f}%")