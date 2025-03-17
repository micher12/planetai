import torch
from tqdm import tqdm


def treinar_modelo(model, train_loader, val_loader, device, feature_extractor, epochs=16):
    
    optimizer = torch.optim.Adam([
        {'params': model.parameters(), 'lr': 0.001},
        {'params': feature_extractor.model.parameters(), 'lr': 0.00005}
    ])
    criterion = torch.nn.CrossEntropyLoss()
    model = model.to(device)
    
    historico = {'train_loss': [], 'val_acc': []}
    
    best_val_acc = 0
    bes_val_loos = 2
    for epoch in range(epochs):
        print(f"Época {epoch+1}/{epochs}")
        model.train()
        total_loss = 0
            
        # Treino
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
        
        with torch.no_grad():
            for features, labels in tqdm(val_loader, desc="Validando"):
                features, labels = features.to(device), labels.to(device)
                outputs = model(features)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        historico['train_loss'].append(total_loss/len(train_loader))
        historico['val_acc'].append(correct/total)
        print(f"Loss: {historico['train_loss'][-1]:.4f} | Acurácia: {historico['val_acc'][-1]:.4f}")

        val_acc = historico['val_acc'][-1]
        val_loss = historico["train_loss"][-1]
        if (val_acc >= best_val_acc and val_loss < bes_val_loos) :
            best_val_acc = val_acc
            bes_val_loos = val_loss
            print(f"Salvei AQUI: {bes_val_loos, best_val_acc}")
            print("=" * 10)
            torch.save({
                'model_state_dict': model.state_dict(),
                'input_dim': model.classificador[0].in_features,  
                'hidden_dim': model.classificador[0].out_features,
                'n_classes': model.classificador[-1].out_features
            }, "PlanetAI.pth")


    return model, historico