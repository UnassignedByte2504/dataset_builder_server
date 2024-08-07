import torch
from transformers import BertModel
import logging

class FeatureExtractor:
    """FeatureExtractor class to extract features from text using BERT."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.model = self.initialize_model()
        self.logger.info('BERT model initialized')
        self.tokenizer = None  # Assuming tokenizer is part of the class or passed as an argument

    def initialize_model(self) -> BertModel:
        """Initialize BERT model."""
        try:
            model = BertModel.from_pretrained('bert-base-uncased').cuda()
            return model
        except Exception as e:
            self.logger.error(f'Error initializing BERT model on CUDA: {e}')
            self.logger.info('Trying to initialize BERT model on CPU')
            try:
                model = BertModel.from_pretrained('bert-base-uncased')
                return model
            except Exception as e:
                self.logger.error(f'Error initializing BERT model on CPU: {e}')
                self.logger.info('Retrying to initialize BERT model on CUDA')
                return None

    def extract_features(self, tokenized_text: str):
        """Extract features from text using BERT."""
        try:
            inputs = self.to_tensor(tokenized_text)
            with torch.no_grad():
                outputs = self.model(**inputs)
            return self.to_numpy(outputs.last_hidden_state.mean(dim=1))
        except Exception as e:
            self.logger.error(f'Error extracting features: {e}')
            return None

    def to_tensor(self, tokenized_text):
        """Convert tokenized text to tensor."""
        inputs = self.tokenizer(tokenized_text, return_tensors='pt', truncation=True, padding=True)
        if torch.cuda.is_available():
            inputs = {key: val.cuda() for key, val in inputs.items()}
        return inputs

    def to_numpy(self, tensor):
        """Convert tensor to numpy array."""
        return tensor.cpu().numpy()

__all__ = ['FeatureExtractor']
