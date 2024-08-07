import PyPDF2
import re
import logging

class TextExtractor:
    """TextExtractor class to extract text from PDF files."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.info('TextExtractor initialized')

    def process_pdf(self, file):
        """Process PDF file."""
        file_name = file.filename
        text = self.read_pdf(file)
        self.logger.info(f'Reading PDF: {file_name}')

        cleaned_text = self.clean_text(text)
        self.logger.info(f'Cleaning text: {file_name}')
        return cleaned_text

    def read_pdf(self, file):
        """Read text from PDF file."""
        try:
            pdf = PyPDF2.PdfFileReader(file)
            text = ''
            for page in range(pdf.getNumPages()):
                text += pdf.getPage(page).extract_text()
            return text
        except Exception as e:
            self.logger.error(f'Error reading PDF: {e}')
            return None

    def clean_text(self, text):
        """Clean text by removing non-word characters and multiple spaces."""
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\W+', ' ', text)
        return text

    def __call__(self, file):
        return self.process_pdf(file)

    def __repr__(self):
        return 'TextExtractor'

    def __str__(self):
        return 'TextExtractor'

__all__ = ['TextExtractor']
