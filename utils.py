from sklearn.metrics import classification_report, confusion_matrix
import torch

def avaliar_modelo(model, feature_extractor, textos, labels, device):
    features = feature_extractor.extract_features(textos)
    features_tensor = torch.FloatTensor(features).to(device)
    labels_tensor = torch.LongTensor(labels).to(device)
    
    model.eval()
    with torch.no_grad():
        outputs = model(features_tensor)
        _, preds = torch.max(outputs, dim=1)
    
    print("\nRelatório de Classificação:")
    print(classification_report(labels_tensor.cpu(), preds.cpu()))
    
    print("\nMatriz de Confusão:")
    print(confusion_matrix(labels_tensor.cpu(), preds.cpu()))

def classificar_noticia(model, feature_extractor, titulo, conteudo, device):
    texto = f"{titulo} {conteudo}"
    features = feature_extractor.extract_features([texto])
    features_tensor = torch.FloatTensor(features).to(device)
    
    with torch.no_grad():
        outputs = model(features_tensor)
        probs = torch.nn.functional.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, dim=1)
    
    return {
        'classe': pred.item(),
        'confianca': conf.item() * 100
    }