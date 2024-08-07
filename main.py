"""
llm-services-api is a FastAPI-based application that provides a suite of natural language processing services 
using various machine learning models. The application is designed to run in a Docker container, providing 
endpoints for text summarization, sentiment analysis, named entity recognition, paraphrasing, keyword extraction,
and embedding generation.
"""
import argparse
import json
import logging
import sys
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from utils.middleware import add_security_headers
from utils.auth import get_api_key  # Import get_api_key for global dependency
from routers import summarization, sentiment, entities, paraphrase, keywords, embedding, openai_compatible_embedding
from models.nlp_models import load_models

# Initialize the FastAPI app with global API key dependency
app = FastAPI(dependencies=[Depends(get_api_key)])

# CORS configuration to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add security headers middleware
app.middleware("http")(add_security_headers)

# Include routers
app.include_router(summarization.router)
app.include_router(sentiment.router)
app.include_router(entities.router)
app.include_router(paraphrase.router)
app.include_router(keywords.router)
app.include_router(embedding.router)
app.include_router(openai_compatible_embedding.router)

def load_config():
    """
    Load model configuration from a JSON file.
    """
    with open("models_config.json", "r") as file:
        return json.load(file)

def parse_arguments():
    """
    Parse command-line arguments to override model configurations.
    """
    parser = argparse.ArgumentParser(description="Load NLP Models")
    parser.add_argument("--embedding-model", type=str, help="Specify embedding model")
    parser.add_argument("--summarization-model", type=str, help="Specify summarization model")
    parser.add_argument("--sentiment-model", type=str, help="Specify sentiment analysis model")
    parser.add_argument("--ner-model", type=str, help="Specify named entity recognition model")
    parser.add_argument("--paraphrase-model", type=str, help="Specify paraphrasing model")
    parser.add_argument("--keyword-model", type=str, help="Specify keyword extraction model")
    
    # Only parse args if we're not running via Uvicorn
    if 'uvicorn' not in sys.argv[0]:
        args = parser.parse_args()
        return vars(args)
    else:
        return {}

def initialize_models():
    """
    Load models during application startup.
    """
    # Load JSON config and command-line args
    config = load_config()

    # Combine the JSON configuration with any command-line overrides
    args = parse_arguments()
    config.update({k.replace("-", "_"): v for k, v in args.items() if v is not None})

    # Load models based on the configuration
    load_models(config)

# Ensure that models are loaded when the FastAPI app starts
@app.on_event("startup")
async def startup_event():
    print("Initializing models...")
    initialize_models()
    print("Models loaded successfully.")

if __name__ == "__main__":
    initialize_models()  # Load models when running directly
    import uvicorn
    # Run the app with Uvicorn for better performance
    uvicorn.run(app, host="0.0.0.0", port=5000)
