from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class BertFeatureExtractor:
    def __init__(self, model_name="neuralmind/bert-large-portuguese-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        for param in self.model.parameters():
            param.requires_grad = True
    
    def extract_features(self, texts, max_length=512, batch_size=16):
        all_features = []
        texts = [str(text) for text in texts]
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            
            encoded_input = self.tokenizer(
                batch_texts,
                padding='max_length',
                truncation=True,
                max_length=max_length,
                return_tensors='pt'
            )
            
            input_ids = encoded_input['input_ids'].to(self.device)
            attention_mask = encoded_input['attention_mask'].to(self.device)
            
            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                last_hidden = outputs.last_hidden_state
                mask = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
                masked_hidden = last_hidden * mask
                sum_hidden = torch.sum(masked_hidden, dim=1)
                sum_mask = torch.sum(mask, dim=1) + 1e-8  # Evitar divisão por zero
                features = (sum_hidden / sum_mask).cpu().numpy()
                all_features.append(features)
        
        return np.vstack(all_features)

def combinar_textos(df):
    """Combina título e conteúdo de um DataFrame"""
    return (df['title'] + ' ' + df['content']).tolist()