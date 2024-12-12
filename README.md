# Translation API

This repository provides a robust translation service using the MarianMT model from Hugging Face and Flask for serving the API. The service includes features such as language detection, GPU support, and comprehensive error handling.

---

## Features

- **Multi-language Translation**: Supports translation from English to French, Hindi, Spanish, Russian, and German.
- **Language Detection**: Automatically detects the source language.
- **Error Handling**: Comprehensive validation and logging for robust performance.
- **GPU Support**: Automatically uses GPU if available for faster translation.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/harshitasingh4839/translation-api-helsinki_models.git
   cd translation-api
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Ensure GPU support by installing PyTorch with CUDA if supported by your system:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
   ```

---

## Usage

### Running the API
1. Start the Flask server:
   ```bash
   python main.py
   ```

2. The server will run on `http://127.0.0.1:5000` by default.

### API Endpoint
**POST /translate**

#### Request Payload
Send a JSON object with the following fields:
- `text` (string): The text to translate.
- `target_lang` (string): The target language code (e.g., `fr`, `es`, `hi`).

Example:
```json
{
    "text": "Hello, how are you?",
    "target_lang": "fr"
}
```

#### Response
- `translated_text` (string): The translated text.

Example Response:
```json
{
    "translated_text": "Bonjour, comment ça va ?"
}
```

---

## Code Structure

### `translation.py`
This file contains the `Translator` class, which handles:
- Source language detection using `langdetect`.
- Translation using MarianMT models from Hugging Face.
- Error handling and logging for each step.

### `main.py`
This file serves as the entry point for the Flask API. It provides an endpoint (`/translate`) to accept translation requests and return responses.

---

## Supported Languages

The following translations are supported:
- English to French (`en-fr`)
- English to Hindi (`en-hi`)
- English to Spanish (`en-es`)
- English to Russian (`en-ru`)
- English to German (`en-de`)

---

## Logging
Logs are configured using Python's `logging` module. Logs are printed in the following format:
```
[Timestamp] - [Log Level] - [Message]
```

---

## Error Handling
- Invalid input (e.g., empty text or missing target language) raises a `400 Bad Request` error.
- Unexpected errors return a `500 Internal Server Error`.

---

## Deployment

To deploy the application:
1. Use a production-grade WSGI server like `gunicorn`:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```
2. Optionally, containerize the application using Docker:
   - Create a `Dockerfile`:
     ```dockerfile
     FROM python:3.9-slim
     WORKDIR /app
     COPY . .
     RUN pip install --no-cache-dir -r requirements.txt
     CMD ["python", "main.py"]
     ```
   - Build and run the Docker image:
     ```bash
     docker build -t translation-api .
     docker run -p 5000:5000 translation-api
     ```

---

## License
This project is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

## Contact
For questions or support, please contact [your_email@example.com].

