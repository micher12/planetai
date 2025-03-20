import torch
from tqdm import tqdm


def treinar_modelo(model, train_loader, val_loader, device, epochs=16):
    
    # então não precisamos otimizá-lo aqui
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=2, factor=0.5)
    
    model = model.to(device)
    
    historico = {'train_loss': [], 'val_loss': [], 'val_acc': []}
    
    best_val_acc = 0
    
    for epoch in range(epochs):
        print(f"Época {epoch+1}/{epochs}")
        model.train()
        total_loss = 0
            
        # Treino (features já foram extraídas anteriormente)
        for features, labels in tqdm(train_loader, desc="Treinando"):
            features, labels = features.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        # Validação
        model.eval()
        correct = 0
        total = 0
        val_loss = 0
        
        with torch.no_grad():
            for features, labels in tqdm(val_loader, desc="Validando"):
                features, labels = features.to(device), labels.to(device)
                
                outputs = model(features)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        avg_train_loss = total_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        val_acc = correct / total
        
        historico['train_loss'].append(avg_train_loss)
        historico['val_loss'].append(avg_val_loss)
        historico['val_acc'].append(val_acc)
        
        print(f"Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Acurácia: {val_acc:.4f}")

        # Atualiza o scheduler com base na perda de validação
        scheduler.step(avg_val_loss)
        
        # Salva o melhor modelo baseado na acurácia e, em caso de empate, na perda
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            print(f"Melhor modelo salvo! Acurácia: {best_val_acc:.4f}")
            print("=" * 50)
            
            model_path = "PlanetAI.pth"
            torch.save({
                'model_state_dict': model.state_dict(),
                'input_dim': model.classificador[0].in_features,  
                'hidden_dim': model.classificador[0].out_features,
                'n_classes': model.classificador[-1].out_features,
                'dropout': 0.3,  # Salvando o valor de dropout para reprodutibilidade
                'epoch': epoch,
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_val_acc': best_val_acc,
            }, model_path)

    return model, historico