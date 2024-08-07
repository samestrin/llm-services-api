from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch

# Check if a GPU is available and use it if possible
device = 0 if torch.cuda.is_available() else -1

# Dictionary of supported models for various tasks
supported_models = {
    "embedding": {
        "all-MiniLM-L6-v2": "all-MiniLM-L6-v2",
        "all-mpnet-base-v2": "all-mpnet-base-v2",
        "all-distilroberta-v1": "all-distilroberta-v1"
    },
    "summarization": {
        "facebook/bart-large-cnn": "facebook/bart-large-cnn",
        "t5-small": "t5-small",
        "t5-base": "t5-base"
    },
    "sentiment": {
        "distilbert-base-uncased-finetuned-sst-2-english": "distilbert-base-uncased-finetuned-sst-2-english",
        "bert-base-uncased": "nlptown/bert-base-multilingual-uncased-sentiment"
    },
    "ner": {
        "dbmdz/bert-large-cased-finetuned-conll03-english": "dbmdz/bert-large-cased-finetuned-conll03-english",
        "bert-base-cased": "dslim/bert-base-NER"
    },
    "paraphrase": {
        "Vamsi/T5_Paraphrase_Paws": "Vamsi/T5_Paraphrase_Paws",
        "t5-small-paraphrase": "ramsrigouthamg/t5-small-paraphraser"
    },
    "keyword": {
        "all-MiniLM-L6-v2": "all-MiniLM-L6-v2",
        "all-mpnet-base-v2": "all-mpnet-base-v2"
    }
}

# Cache for loaded models
loaded_models = {}

def load_models(config):
    """
    Load models based on the provided configuration.
    """
    # Load each model and log the process
    try:
        # Load embedding model
        embedding_model_name = config["embedding_model"]
        print(f"Loading embedding model: {embedding_model_name}")
        loaded_models["embedding"] = SentenceTransformer(supported_models["embedding"][embedding_model_name])
        print(f"Loaded embedding model: {embedding_model_name}")

        # Load summarization model
        summarization_model_name = config["summarization_model"]
        print(f"Loading summarization model: {summarization_model_name}")
        loaded_models["summarization"] = pipeline("summarization", model=supported_models["summarization"][summarization_model_name], device=device)
        print(f"Loaded summarization model: {summarization_model_name}")

        # Load sentiment analysis model
        sentiment_model_name = config["sentiment_model"]
        print(f"Loading sentiment analysis model: {sentiment_model_name}")
        loaded_models["sentiment"] = pipeline("sentiment-analysis", model=supported_models["sentiment"][sentiment_model_name], device=device)
        print(f"Loaded sentiment analysis model: {sentiment_model_name}")

        # Load named entity recognition model
        ner_model_name = config["ner_model"]
        print(f"Loading NER model: {ner_model_name}")
        loaded_models["ner"] = pipeline("ner", model=supported_models["ner"][ner_model_name], aggregation_strategy="simple", device=device)
        print(f"Loaded NER model: {ner_model_name}")

        # Load paraphrasing model
        paraphrase_model_name = config["paraphrase_model"]
        print(f"Loading paraphrase model: {paraphrase_model_name}")
        loaded_models["paraphrase"] = pipeline("text2text-generation", model=supported_models["paraphrase"][paraphrase_model_name], device=device)
        print(f"Loaded paraphrase model: {paraphrase_model_name}")

        # Load keyword extraction model
        keyword_model_name = config.get("keyword_model", "all-MiniLM-L6-v2")
        print(f"Loading keyword extraction model: {keyword_model_name}")
        loaded_models["keyword"] = SentenceTransformer(supported_models["keyword"][keyword_model_name])
        print(f"Loaded keyword extraction model: {keyword_model_name}")

    except KeyError as e:
        print(f"Error: Model key not found in configuration or supported models. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during model loading: {e}")

def get_model(task, model_name=None):
    """
    Retrieve the model for a specific task. Optionally allows specifying a model name.
    """
    # If a model name is provided, check against the supported models and return the appropriate model.
    if model_name:
        if model_name in supported_models[task]:
            return SentenceTransformer(supported_models[task][model_name])
        else:
            raise ValueError(f"Model {model_name} not supported for task {task}.")
    
    # Otherwise, return the default loaded model for the task.
    if task in loaded_models:
        return loaded_models[task]
    
    raise ValueError(f"Model for task {task} is not loaded.")
