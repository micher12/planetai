import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
import torch

def carregar_csv(caminho):
    """Carrega dados de um arquivo CSV"""
    df = pd.read_csv(caminho)
    df = df.fillna('')
    return df

def preparar_dataloaders(features, labels, batch_size=32, test_size=0.2):
    """Prepara DataLoaders para treino e validação"""
    X_train, X_val, y_train, y_val = train_test_split(
        features, labels, test_size=test_size, random_state=42, stratify=labels
    )
    
    train_dataset = torch.utils.data.TensorDataset(
        torch.FloatTensor(X_train), torch.LongTensor(y_train))
    val_dataset = torch.utils.data.TensorDataset(
        torch.FloatTensor(X_val), torch.LongTensor(y_val))
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    return train_loader, val_loader