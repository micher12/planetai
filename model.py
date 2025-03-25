import torch
from torch import nn
from torch.nn import functional as F

class AtencaoSeletiva(nn.Module):
    """Mecanismo de atenção para focar em partes relevantes do texto"""
    def __init__(self, input_dim):
        super().__init__()
        self.attention = nn.Linear(input_dim, 1)
    
    def forward(self, features, mask=None):
        attention_scores = self.attention(features)
        if mask is not None:
            mask = mask.unsqueeze(2)
            attention_scores = attention_scores.masked_fill(mask == 0, -1e9)
        attention_weights = F.softmax(attention_scores, dim=1)
        context = torch.bmm(features.transpose(1, 2), attention_weights).squeeze(2)
        return context, attention_weights

class ClassificadorNoticiasAvancado(nn.Module):
    def __init__(self, input_dim, hidden_dim=256, n_classes=3, dropout=0.5, use_attention=True):
        super().__init__()
        self.use_attention = use_attention
        
        # Camadas convolucionais
        self.conv1 = nn.Conv1d(input_dim, hidden_dim, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(input_dim, hidden_dim, kernel_size=5, padding=2)
        
        # Mecanismo de atenção
 
        self.atencao = AtencaoSeletiva(input_dim)
        comb_dim = input_dim + hidden_dim * 2
       
        
        # Normalização
        self.layer_norm = nn.LayerNorm(comb_dim)
        
        # Classificador com residual
        self.fc1 = nn.Linear(comb_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim//2)
        self.bn2 = nn.BatchNorm1d(hidden_dim//2)
        self.residual = nn.Linear(comb_dim, hidden_dim//2)
        self.output = nn.Linear(hidden_dim//2, n_classes)
        
        # Regularização
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x, all_tokens=None, attention_mask=None):
        batch_size = x.size(0)
        
        if self.use_attention and all_tokens is not None:
            context, _ = self.atencao(all_tokens, attention_mask)
            all_tokens_t = all_tokens.transpose(1, 2)
            conv1_out = F.relu(self.conv1(all_tokens_t))
            conv2_out = F.relu(self.conv2(all_tokens_t))
            conv1_pooled = F.adaptive_max_pool1d(conv1_out, 1).view(batch_size, -1)
            conv2_pooled = F.adaptive_max_pool1d(conv2_out, 1).view(batch_size, -1)
            combined = torch.cat([context, conv1_pooled, conv2_pooled], dim=1)
        else:
            combined = x
        
        combined = self.layer_norm(combined)
        h1 = self.fc1(combined)
        h1 = self.bn1(h1)
        h1 = F.relu(h1)
        h1 = self.dropout(h1)
        
        h2 = self.fc2(h1)
        h2 = self.bn2(h2)
        res = self.residual(combined)
        h2 = F.relu(h2 + res)
        h2 = self.dropout(h2)
        
        output = self.output(h2)
        return output