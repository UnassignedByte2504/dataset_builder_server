import os
from src.executors.custom_executor import CustomExecutor
from src.pre_processors.text_extractor import TextExtractor
from src.pre_processors.tokenizer import Tokenizer
from src.pre_processors.feature_extractor import FeatureExtractor
from src.sockets.sio import sio
import logging

class PdfProcessor(CustomExecutor):
    """PdfProcessor class to process PDF files."""

    def __init__(self, max_workers: int = None, executor_type: str = 'thread'):
        super().__init__(max_workers, executor_type)
        self.text_extractor = TextExtractor()
        self.tokenizer = Tokenizer()
        self.feature_extractor = FeatureExtractor()
        self.logger = logging.getLogger(__name__)
        self.logger.info('PdfProcessor initialized')

    def process_pdf(self, file):
        """Process PDF file."""
        output = {
            'text': None,
            'features': None,
            'tokens': None
        }

        try:
            text = self.text_extractor(file)
            output['text'] = text
            self.logger.info(f'Text extracted from PDF: {file.filename}')
        except Exception as e:
            self.logger.error(f'Error extracting text from PDF: {e}')
            return None

        try:
            tokens = self.tokenizer.tokenize_text(text)
            output['tokens'] = tokens
            self.logger.info(f'Text tokenized: {file.filename}')
        except Exception as e:
            self.logger.error(f'Error tokenizing text: {e}')
            return None

        try:
            self.feature_extractor.tokenizer = self.tokenizer.tokenizer  # Pass the tokenizer instance
            features = self.feature_extractor.extract_features(tokens)
            output['features'] = features
            self.logger.info(f'Features extracted: {file.filename}')
        except Exception as e:
            self.logger.error(f'Error extracting features: {e}')
            return None

        return output

    def process_pdfs(self, directory: str):
        """Process PDF files in directory."""
        files = os.listdir(directory)
        results = []
        for file in files:
            file_path = os.path.join(directory, file)
            future = self.submit(self.process_pdf, file_path)
            results.append(future)
        return results
