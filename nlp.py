import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

class BertFeatureExtractor:
    def __init__(self, model_name="neuralmind/bert-large-portuguese-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        for param in self.model.parameters():
            param.requires_grad = True
    
    def extract_features(self, texts, max_length=512, batch_size=16, return_all_tokens=True):
        all_features = []
        all_attention_masks = []
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
                
                if return_all_tokens:
                    # Retornar todas as representações de tokens
                    features = outputs.last_hidden_state.cpu().numpy()
                    all_features.append(features)
                    all_attention_masks.append(attention_mask.cpu().numpy())
                else:
                    # Retornar apenas o token [CLS]
                    features = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                    all_features.append(features)
        
        if return_all_tokens:
            return np.vstack(all_features), np.vstack(all_attention_masks)
        else:
            return np.vstack(all_features)

def combinar_textos(df):
    """Combina título e conteúdo de um DataFrame"""
    return (df['title'] + ' ' + df['content']).tolist()