from transformers import BertTokenizer, BertModel
import torch
import logging

class Tokenizer:
    """Tokenizer class to initialize BERT tokenizer and tokenize text."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tokenizer_initialized = False
        self.tokenizer = None
        self.bert_model = None

    def initialize_tokenizer(self):
        """Initialize BERT tokenizer and model."""
        while not self.tokenizer_initialized:
            try:
                self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                self.bert_model = BertModel.from_pretrained('bert-base-uncased').cuda()
                self.logger.info('BERT tokenizer and model initialized on CUDA')
                self.tokenizer_initialized = True
            except Exception as e:
                self.logger.error(f'Error initializing BERT tokenizer and model on CUDA: {e}')
                self.logger.info('Trying to initialize BERT tokenizer and model on CPU')
                try:
                    self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                    self.bert_model = BertModel.from_pretrained('bert-base-uncased')
                    self.logger.info('BERT tokenizer and model initialized on CPU')
                    self.tokenizer_initialized = True
                except Exception as e:
                    self.logger.error(f'Error initializing BERT tokenizer and model on CPU: {e}')
                    self.logger.info('Retrying to initialize BERT tokenizer and model on CUDA')
                    return

    def tokenize_text(self, text):
        """Tokenize text and return embeddings."""
        if not self.tokenizer_initialized:
            self.logger.info('Tokenizer not initialized, initializing...')
            self.initialize_tokenizer()
        try:
            tokens = self.tokenizer.tokenize(text)
            total_tokens = len(tokens)
            self.logger.info(f'Total tokens: {total_tokens}')
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            if torch.cuda.is_available():
                inputs = {key: val.cuda() for key, val in inputs.items()}
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
            return outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        except Exception as e:
            self.logger.error(f'Error tokenizing text: {e}')
            return None

__all__ = ['Tokenizer']
