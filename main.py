from flask import Flask, request, jsonify
from translation import Translator
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/translate', methods=['POST'])
def translate_text():
    """
    API endpoint for text translation.
    
    Expected JSON payload:
    {
        "text": "Text to translate",
        "target_lang": "Target language code (e.g., 'fr', 'es', 'hi')"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        text = data.get('text')
        target_lang = data.get('target_lang')
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        if not target_lang:
            return jsonify({"error": "Target language is required"}), 400
        
        # Create Translator instance
        translator = Translator(text, target_lang)
        
        # Perform translation
        translated_text = translator.translate_text()
        
        # Return translation result
        return jsonify({
            # "original_text": text,
            "translated_text": translated_text,
            # "source_language": translator.src_lang,
            # "target_language": target_lang
        }), 200
    
    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    
    except Exception as e:
        logger.error(f"Translation Error: {e}")
        return jsonify({"error": "An unexpected error occurred during translation"}), 500

if __name__ == '__main__':
    app.run(debug=True)