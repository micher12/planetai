from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support
import torch
import matplotlib.pyplot as plt
import seaborn as sns
import os

def avaliar_modelo(model, feature_extractor, textos, labels, device, historico,
                  confusion_matrix_path='matriz_confusao.png', 
                  metrics_plot_path='metricas_treinamento.png'):

    # Avaliação do modelo
    features = feature_extractor.extract_features(textos)
    features_tensor = torch.FloatTensor(features).to(device)
    labels_tensor = torch.LongTensor(labels).to(device)
    
    model.eval()
    with torch.no_grad():
        outputs = model(features_tensor)
        _, preds = torch.max(outputs, dim=1)
    
    # Relatório de Classificação (impresso no console)
    print("\nRelatório de Classificação:")
    print(classification_report(labels_tensor.cpu(), preds.cpu()))
    
    # Matriz de Confusão como Heatmap
    cm = confusion_matrix(labels_tensor.cpu(), preds.cpu())
    
    # Salvar Matriz de Confusão como imagem
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Matriz de Confusão')
    plt.xlabel('Predito')
    plt.ylabel('Real')
    
    # Verificar se o caminho contém diretório e criar apenas se existir
    dirname = os.path.dirname(confusion_matrix_path)
    if dirname:  # Se dirname não for uma string vazia
        os.makedirs(dirname, exist_ok=True)
    
    plt.savefig(confusion_matrix_path, bbox_inches='tight')
    plt.close()  # Fechar a figura para liberar memória
    
    # Criação do gráfico de métricas de treinamento
    plt.figure(figsize=(12, 5))
    
    # Verificar quais métricas estão disponíveis no histórico
    metricas_disponiveis = list(historico.keys())
    
    # Configuração para diferentes combinações de métricas
    num_plots = len(metricas_disponiveis)
    if num_plots > 0:
        # Criar subplots dinâmicos baseados nas métricas disponíveis
        for i, metrica in enumerate(metricas_disponiveis):
            plt.subplot(1, num_plots, i+1)
            
            # Escolher cor baseada no tipo de métrica
            cor = 'blue'
            if 'acc' in metrica or 'accuracy' in metrica:
                cor = 'green'
            elif 'loss' in metrica:
                cor = 'red'
                
            # Plotar métrica
            plt.plot(historico[metrica], label=metrica, color=cor)
            plt.title(f'{metrica.replace("_", " ").title()} por Época')
            plt.xlabel('Época')
            
            # Ajustar rótulo do eixo Y baseado no tipo de métrica
            if 'acc' in metrica or 'accuracy' in metrica:
                plt.ylabel('Acurácia (%)')
            elif 'loss' in metrica:
                plt.ylabel('Loss')
            else:
                plt.ylabel('Valor')
                
            plt.legend()
    
    plt.tight_layout()
    
    # Verificar se o caminho contém diretório e criar apenas se existir
    dirname = os.path.dirname(metrics_plot_path)
    if dirname:  # Se dirname não for uma string vazia
        os.makedirs(dirname, exist_ok=True)
    
    plt.savefig(metrics_plot_path, bbox_inches='tight')
    plt.close()  # Fechar a figura
    
    print(f"\nGráficos salvos")


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