from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch

# Load models at startup
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = SentenceTransformer("all-MiniLM-L6-v2")  # KeyBERT uses the same model

# Check if a GPU is available and use it if possible
device = 0 if torch.cuda.is_available() else -1

# Initialize the pipelines with explicit models
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=device)
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", aggregation_strategy="simple", device=device)
paraphraser = pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws", device=device)
