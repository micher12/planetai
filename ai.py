import torch
from model import ClassificadorNoticias  # Importar a classe do modelo
from pln import BertFeatureExtractor
import uvicorn
from pydantic import BaseModel
from model import ClassificadorNoticias
from pln import BertFeatureExtractor
from fastapi import FastAPI, HTTPException


app = FastAPI(title="API de Classificação de Notícias Ambientais")

class InputApi(BaseModel):
    titulo: str
    conteudo: str

class OutputApi(BaseModel):
    classe: int
    confianca: float   


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class_mapping = {0: "Negativa", 1: "Positiva", 2: "Irrelevante"}

# Carregar o checkpoint
checkpoint = torch.load("PlanetAI.pth", map_location=device)

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




@app.post("/classificar", response_model=OutputApi)
async def api_classificar_noticia(input_data: InputApi):
    if model is None or feature_extractor is None:
        raise HTTPException(status_code=500, detail="Modelo não carregado corretamente")
    
    try:
        resultado = classificar_noticia(
            titulo=input_data.titulo,
            conteudo=input_data.conteudo
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao classificar notícia: {str(e)}")

# Endpoint para verificar se a API está funcionando
@app.get("/")
async def root():
    return {"status": "online", "message": "API de Classificação de Notícias Ambientais"}
 

if __name__ == "__main__":
    # uvicorn.run("ai:app", host="0.0.0.0", port=8000, reload=True)
    while True:
        text = input("Digite a noticia (sair): ")

        if text == "sair":
            break
    
        res = classificar_noticia(text,"")
        print(f"Classificação: {class_mapping[res['classe']]}")
        print(res["confianca"])