# LLM Services API

[![Star on GitHub](https://img.shields.io/github/stars/samestrin/llm-services-api?style=social)](https://github.com/samestrin/llm-services-api/stargazers)[![Fork on GitHub](https://img.shields.io/github/forks/samestrin/llm-services-api?style=social)](https://github.com/samestrin/llm-services-api/network/members)[![Watch on GitHub](https://img.shields.io/github/watchers/samestrin/llm-services-api?style=social)](https://github.com/samestrin/llm-services-api/watchers)

![Version 0.0.4](https://img.shields.io/badge/Version-0.0.4-blue) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![Built with Python](https://img.shields.io/badge/Built%20with-Python-green)](https://www.python.org/)

LLM Services API is a FastAPI-based application that provides a suite of natural language processing services using various machine learning models from Hugging Face's `transformers` library through a REST API interface. The application is designed to run in a Docker container, providing endpoints for text summarization, sentiment analysis, named entity recognition, paraphrasing, keyword extraction, and embedding generation. The entire API is secured using an API key with `Bearer <token>` format, ensuring that only authorized users can access the endpoints.

The service allows flexibility in model selection through command-line arguments and a configuration file, `models_config.json`, enabling users to specify different Hugging Face models for various NLP tasks. This flexibility allows users to select lightweight models for lower-resource environments or more powerful models for advanced tasks.

## Updates

**0.0.4**

- **Tokenization:** Convert input text into a list of token IDs, allowing you to process and manipulate text at the token level, default model `all-MiniLM-L6-v2`.
- **Detokenization:** Reconstruct original text from a list of token IDs, allowing you to reverse the tokenization process, default model `all-MiniLM-L6-v2`.

**0.0.3**

- **Adaptive Throttling:** Implemented an adaptive throttling mechanism that delays requests using the `Retry-After` header when errors are encountered due to high request frequency or processing failures. The delay is dynamically adjusted based on the client’s request rate and error occurrences.

**0.0.2**

- **OpenAI-Compatible Embeddings:** Provides an endpoint that mimics the OpenAI embedding API, allowing easy integration with existing systems expecting OpenAI-like responses.
- **Configurable Model Loading:** Customize which Hugging Face NLP models are loaded by providing command-line arguments or configuring the `models_config.json` file. This flexibility allows the application to adapt to different resource environments or use cases.

## Features

- **Text Summarization:** Generate concise summaries of long texts, default model `BART`.
- **Sentiment Analysis:** Determine the sentiment of text inputs, default model `DistilBERT`.
- **Named Entity Recognition (NER):** Identify entities within text and sort them by frequency, default model `BERT` (dbmdz/bert-large-cased-finetuned-conll03-english).
- **Paraphrasing:** Rephrase sentences to produce semantically similar outputs, default model `T5`.
- **Keyword Extraction:** Extract important keywords from text, with customizable output count, default model `KeyBERT`.
- **Embedding Generation:** Create vector representations of text, default model `SentenceTransformers` (all-MiniLM-L6-v2).
- - **Caching with LRU:** Frequently used computations, such as generating embeddings and tokenizations, are cached using the Least Recently Used (LRU) strategy. This reduces response times for repeated requests and enhances overall performance.

## Dependencies

- Python 3.7+
- FastAPI
- Uvicorn
- spaCy
- transformers
- sentence-transformers
- keybert
- torch
- python-dotenv (for environment variable management)

## Installation

To get started with the LLM Services API, follow these steps:

1. **Clone the Repository:**

```bash
git clone https://github.com/samestrin/llm-services-api.git
cd llm-services-api
```

2. **Create a Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Install the Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Download SpaCy Model:**

```bash
python -m spacy download en_core_web_sm
```

5. **Run the Application Locally:**

You can run the application locally in two ways:

- **Using Uvicorn:**

This is the recommended method for running in a development or production-like environment.

```bash
uvicorn main:app --reload --port 5000
```

- **Using Python:**

This method allows you to pass command-line arguments for customizing models.

```bash
python main.py --embedding-model all-MiniLM-L6-v2 --summarization-model facebook/bart-large-cnn
```

Replace `--embedding-model` and `--summarization-model` with the models you wish to use. This approach offers flexibility by allowing you to specify different models for various NLP tasks.

### Options

```bash
  -h, --help                                  Show this help message and exit
  --embedding-model EMBEDDING_MODEL           Specify embedding model
  --summarization-model SUMMARIZATION_MODEL   Specify summarization model
  --sentiment-model SENTIMENT_MODEL           Specify sentiment analysis model
  --ner-model NER_MODEL                       Specify named entity recognition model
  --paraphrase-model PARAPHRASE_MODEL         Specify paraphrasing model
  --keyword-model KEYWORD_MODEL               Specify keyword extraction mode
```

## Running with Docker

To run the application in a Docker container, follow these steps:

1. **Build the Docker Image:**

```bash
docker build -t llm-services-api .
```

2. **Run the Docker Container:**

```bash
docker run -p 5000:5000 llm-services-api
```

The application will be accessible at `http://localhost:5000`.

## Usage

The API provides several endpoints for various NLP tasks. Below is a summary of the available endpoints:

### Endpoints

#### 1. Text Summarization

- **Endpoint:** `/summarize`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
  "summary": "The generated summary of the provided text."
}
```

#### 2. Sentiment Analysis

- **Endpoint:** `/sentiment`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
    "sentiment": [
        {
        "label": "POSITIVE", # or "NEGATIVE"
        "score": 0.99
        }
    ]
}
```

#### 3. Named Entity Recognition

- **Endpoint:** `/entities`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
    "entities": [
        {
        "entity": "PERSON",
        "word": "John Doe",
        "frequency": 3
        },
        ...
    ]
}
```

#### 4. Paraphrasing

- **Endpoint:** `/paraphrase`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
  "paraphrased_text": "The paraphrased version of the input text."
}
```

#### 5. Keyword Extraction

- **Endpoint:** `/extract_keywords`
- **Method:** `POST`
- **Query Parameters:**
  - `num_keywords`: Optional, defaults to 5. Specifies the number of keywords to extract.
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
"keywords": [
    {
        "keyword": "important keyword",
        "score": 0.95
        },
        ...
    ]
}
```

#### 6. Embedding Generation

- **Endpoint:** `/embed`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here"
}
```

- **Response:**

```json
{
    "embedding": [0.1, 0.2, 0.3, ...] # Array of float numbers representing the text embedding
}
```

### 7. OpenAI-Compatible Embedding

- **Endpoint:** `/v1/embeddings`
- **Method:** `POST`
- **Request Body:**

```json
{
  "input": "Your text here",
  "model": "all-MiniLM-L6-v2"  # or another supported model
}
```

- **Response:**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [-0.006929283495992422, -0.005336422007530928, ...],  # Embedding array
    }
  ],
  "model": "all-MiniLM-L6-v2",
  "usage": {
    "prompt_tokens": 5,  # Number of tokens in the input
    "total_tokens": 5    # Total number of tokens processed
  }
}
```

#### 8. Tokenization

- **Endpoint:** `/tokenize`
- **Method:** `POST`
- **Request Body:**

```json
{
  "text": "Your text here",
  "model": "all-MiniLM-L6-v2"  # Optional, specify a model for tokenization
}
```

- **Response:**

```json
{
  "tokens": [101, 7592, 999, ...]  # Array of token IDs representing the text
}
```

This endpoint allows you to tokenize input text using a specified or default model. If the model field is not provided, the default embeddings model `all-MiniLM-L6-v2` will be used.

#### 8. Detokenization

- **Endpoint:** `/detokenize`
- **Method:** `POST`
- **Request Body:**

```json
{
  "tokens": [101, 2023, 2003, 2019, 2742, 6251, 2000, 19204, 1012, 102],  # List of token IDs
  "model": "all-MiniLM-L6-v2"  # Optional, specify a model for detokenization
}
```

- **Response:**

```json
{
  "text": "This is an example sentence to tokenize."  # The reconstructed text
}
```

## Contribute

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

## Share

[![Twitter](https://img.shields.io/badge/X-Tweet-blue)](https://twitter.com/intent/tweet?text=Check%20out%20this%20awesome%20project!&url=https://github.com/samestrin/llm-services-api) [![Facebook](https://img.shields.io/badge/Facebook-Share-blue)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/samestrin/llm-services-api) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Share-blue)](https://www.linkedin.com/sharing/share-offsite/?url=https://github.com/samestrin/llm-services-api)
