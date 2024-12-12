import torch
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect, LangDetectException
import logging

class Translator:
    """
    A robust translation class with GPU support and comprehensive error handling.
    """
    MODELS = {
        "en-fr": "Helsinki-NLP/opus-mt-en-fr",
        "en-hi": "Helsinki-NLP/opus-mt-en-hi",
        "en-es": "Helsinki-NLP/opus-mt-en-es",
        "en-ru": "Helsinki-NLP/opus-mt-en-ru",
        "en-de": "Helsinki-NLP/opus-mt-en-de",
    }

    def __init__(self, text, tgt_lang=None):
        """
        Initialize the Translator with robust error checking.

        Parameters:
        text (str): The text to be translated.
        tgt_lang (str, optional): The target language code. 
                                  If None, raises a ValueError.
        """
        # Validate input
        if not isinstance(text, str):
            raise ValueError("Input text must be a string")
        
        if not text.strip():
            raise ValueError("Input text cannot be empty")

        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        self.text = text
        self.tgt_lang = tgt_lang
        self.src_lang = "en"
        
        # Detect source language with fallback
        try:
            self.src_lang = self.detect_src_lang()
        except Exception as e:
            self.logger.warning(f"Language detection failed: {e}")
            self.src_lang = "en"  # Default to English

    def detect_src_lang(self):
        """
        Detect the source language with robust error handling.

        Returns:
        str: The detected source language code.
        """
        try:
            # Use language detection with a timeout
            return detect(self.text)
        except LangDetectException as e:
            self.logger.error(f"Language detection error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error in language detection: {e}")
            return "en"  # Default to English

    def load_model(self, model_name):
        """
        Load the translation model and tokenizer with GPU support and error handling.

        Parameters:
        model_name (str): The Hugging Face model name.

        Returns:
        tuple: A tuple containing the tokenizer and model.
        """
        try:
            # Determine the best available device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.logger.info(f"Using device: {self.device}")

            # Load tokenizer and move to device
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            
            # Load model with error handling
            model = MarianMTModel.from_pretrained(model_name)
            model.to(self.device)
            
            # Set model to evaluation mode
            model.eval()
            
            return tokenizer, model

        except Exception as e:
            self.logger.error(f"Error loading model {model_name}: {e}")
            raise

    def translate_text(self):
        """
        Translate text with comprehensive error handling.

        Returns:
        str: The translated text.
        
        Raises:
        ValueError: If translation is not supported or input is invalid.
        """
        # Validate target language
        if not self.tgt_lang:
            raise ValueError("Target language must be specified")

        # Construct model key (handle bidirectional translations)
        possible_model_keys = [
            f"{self.src_lang}-{self.tgt_lang}"
        ]

        # Find a valid model
        model_name = None
        for key in possible_model_keys:
            if key in self.MODELS:
                model_name = self.MODELS[key]
                break

        if not model_name:
            error_msg = f"Translation from {self.src_lang} to {self.tgt_lang} is not supported."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            # Load model
            tokenizer, model = self.load_model(model_name)
            print("Translation model loaded successfully!")


            # Prepare input
            inputs = tokenizer(
                self.text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True
            ).to(self.device)

            # Generate translation
            with torch.no_grad():
                outputs = model.generate(**inputs)

            # Decode translation
            translated_text = tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True
            )

            self.logger.info(f"Successfully translated text to {self.tgt_lang}")
            return translated_text

        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            raise