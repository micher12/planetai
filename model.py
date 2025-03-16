from torch import nn

class ClassificadorNoticias(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, n_classes=3, dropout=0.5):
        super().__init__()
        self.classificador = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),  # Adicionado BatchNorm
            nn.ReLU(),  # Trocado para ReLU padrão
            nn.Dropout(dropout),
            
            nn.Linear(hidden_dim, hidden_dim//2),
            nn.BatchNorm1d(hidden_dim//2),  # Adicionado BatchNorm
            nn.ReLU(),
            nn.Dropout(dropout),
            
            nn.Linear(hidden_dim//2, hidden_dim//4),
            nn.BatchNorm1d(hidden_dim//4),  # Adicionado BatchNorm
            nn.ReLU(),
            nn.Dropout(dropout),
            
            nn.Linear(hidden_dim//4, n_classes)
        )
    
    def forward(self, x):
        return self.classificador(x)