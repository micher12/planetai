import pandas as pd
import numpy as np
import torch
from torch import nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def preparar_dados(df):
    # Combinar título e conteúdo
    textos = (df['title'] + ' ' + df['content']).tolist()
    
    # Converter classes para valores inteiros
    classes = df['class'].values
    
    return textos, classes

def carregar_csv(caminho_arquivo):
    """Carrega os dados do CSV"""
    return pd.read_csv(caminho_arquivo)


def plotar_metricas(historico):
    """Plota gráficos de perda e acurácia do treinamento"""
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(historico['train_loss'], label='Treino')
    plt.plot(historico['val_loss'], label='Validação')
    plt.title('Perda durante o treinamento')
    plt.xlabel('Época')
    plt.ylabel('Perda')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(historico['train_acc'], label='Treino')
    plt.plot(historico['val_acc'], label='Validação')
    plt.title('Acurácia durante o treinamento')
    plt.xlabel('Época')
    plt.ylabel('Acurácia (%)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('metricas_treinamento.png')


def plotar_matriz_confusao(y_true, y_pred, classes=None):
    """Plota a matriz de confusão"""
    if classes is None:
        classes = ['Negativa', 'Positiva', 'Irrelevante']
    
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Matriz de Confusão')
    plt.ylabel('Classe Real')
    plt.xlabel('Classe Prevista')
    plt.savefig('matriz_confusao.png')

def treinar_modelo_completo(
                        model,
                        device,
                        feature_extractor,
                        caminho_arquivo, 
                        batch_size=16, 
                        epochs=5, 
                        learning_rate=2e-5, 
                        test_size=0.2,
                        random_state=42,
                        salvar_modelo=True
    ):
    """Treina o modelo completo a partir do arquivo CSV"""

    
    # Carregar dados
    print("Carregando dados...")
    dados = carregar_csv(caminho_arquivo)
    
    # Verificar distribuição de classes
    print("\nDistribuição de classes:")
    print(dados['class'].value_counts())
    
    # Preparar dados
    textos, classes = preparar_dados(dados)
    
    # Dividir em conjuntos de treino e teste
    print("\nDividindo dados em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        textos, classes, test_size=test_size, random_state=random_state, stratify=classes
    )
    
    # Converter para listas e arrays numpy
    X_train, X_test = list(X_train), list(X_test)
    y_train, y_test = np.array(y_train), np.array(y_test)
    
    print(f"Dados de treino: {len(X_train)} amostras")
    print(f"Dados de teste: {len(X_test)} amostras")
    

    # Extrair features para este epoch (pode ser feito em lotes para conjuntos muito grandes)
    print(f"\nExtraindo features de treino...")
    features_train, masks_train = feature_extractor.extract_features(
        X_train, batch_size=batch_size, return_all_tokens=True
    )

    input_dim = features_train.shape[2]  # [1, seq_len, input_dim]
    print(f"Dimensão de input: {input_dim}")
    
    # Definir otimizador e função de perda
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()
    
    # Histórico de treinamento
    historico = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    # Melhor acurácia para salvar o modelo
    best_val_acc = 0.0
    
    # Loop de treinamento
    print("\nIniciando treinamento...")
    for epoch in range(epochs):
        # Modo de treinamento
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        # Dividir em batches
        num_samples = len(X_train)
        indices = np.random.permutation(num_samples)
        
        print(f"Treinando com {num_samples} amostras...")
        for i in range(0, num_samples, batch_size):
            # Selecionar índices para o batch atual
            batch_indices = indices[i:min(i+batch_size, num_samples)]
            
            # Preparar batch
            batch_features = torch.tensor(features_train[batch_indices, 0, :]).float().to(device)
            batch_all_tokens = torch.tensor(features_train[batch_indices]).float().to(device)
            batch_attn_mask = torch.tensor(masks_train[batch_indices]).float().to(device)
            batch_labels = torch.tensor(y_train[batch_indices]).to(device)
            
            # Zerar gradientes
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(batch_features, batch_all_tokens, batch_attn_mask)
            loss = criterion(outputs, batch_labels)
            
            # Backward pass e otimização
            loss.backward()
            optimizer.step()
            
            # Estatísticas
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += batch_labels.size(0)
            correct += (predicted == batch_labels).sum().item()
            
            # Exibir progresso a cada 10 batches
            if (i // batch_size) % 10 == 0:
                print(f"  Batch {i//batch_size+1}/{(num_samples-1)//batch_size+1}, "
                      f"Loss: {loss.item():.4f}, "
                      f"Acc: {100 * correct/total:.2f}%")
        
        # Métricas de treino
        train_loss = running_loss / ((num_samples - 1) // batch_size + 1)
        train_acc = 100 * correct / total
        
        # Validação
        model.eval()
        print(f"\nExtraindo features de validação...")
        features_val, masks_val = feature_extractor.extract_features(
            X_test, batch_size=batch_size, return_all_tokens=True
        )
        
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for i in range(0, len(X_test), batch_size):
                end_idx = min(i + batch_size, len(X_test))
                batch_size_val = end_idx - i
                
                # Preparar batch
                batch_features = torch.tensor(features_val[i:end_idx, 0, :]).float().to(device)
                batch_all_tokens = torch.tensor(features_val[i:end_idx]).float().to(device)
                batch_attn_mask = torch.tensor(masks_val[i:end_idx]).float().to(device)
                batch_labels = torch.tensor(y_test[i:end_idx]).to(device)
                
                # Forward pass
                outputs = model(batch_features, batch_all_tokens, batch_attn_mask)
                loss = criterion(outputs, batch_labels)
                
                # Estatísticas
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += batch_size_val
                val_correct += (predicted == batch_labels).sum().item()
                
                # Coletar predições e rótulos para relatório de classificação
                all_preds.extend(predicted.cpu().numpy())
                all_labels.extend(batch_labels.cpu().numpy())
        
        # Métricas de validação
        val_loss = val_loss / ((len(X_test) - 1) // batch_size + 1)
        val_acc = 100 * val_correct / val_total
        
        # Atualizar histórico
        historico['train_loss'].append(train_loss)
        historico['train_acc'].append(train_acc)
        historico['val_loss'].append(val_loss)
        historico['val_acc'].append(val_acc)
        
        # Exibir métricas
        print(f"\nEpoch {epoch+1}/{epochs}:")
        print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")
        print(f"  Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%")
        
        # Salvar melhor modelo
        if val_acc > best_val_acc and salvar_modelo:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'val_loss': val_loss,
                'val_acc': val_acc,
            }, 'melhor_modelo_noticias.pth')
            print(f"  Novo melhor modelo salvo com {val_acc:.2f}% de acurácia!")
    
    # Relatório de classificação final
    print("\nRelatório de classificação:")
    target_names = ['Negativa', 'Positiva', 'Irrelevante']
    print(classification_report(all_labels, all_preds, target_names=target_names))
    
    # Plotar métricas
    plotar_metricas(historico)
    
    # Plotar matriz de confusão
    plotar_matriz_confusao(all_labels, all_preds, target_names)
    
    return model