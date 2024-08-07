from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import ner_pipeline
from utils.text_processing import correct_sentence_spacing, chunk_text
from transformers import AutoTokenizer
from collections import defaultdict

router = APIRouter(prefix="/entities", tags=["Named Entity Recognition"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def entities(request: TextRequest):
    """
    Perform named entity recognition on the given text. Returns entities sorted by their frequency in descending order.
    """
    corrected_text = correct_sentence_spacing(request.text)

    # Chunk the text using a sliding window approach
    tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
    chunks = chunk_text(corrected_text, tokenizer, max_length=512, overlap=50)
    entity_frequency = defaultdict(int)

    # Process each chunk and gather entities
    for chunk in chunks:
        chunk_entities = ner_pipeline(chunk)
        for entity in chunk_entities:
            # Ensure all expected keys are present and calculate frequency
            entity_type = entity.get("entity_group") or entity.get("entity", "")
            word = entity.get("word", "")
            
            # Increase the frequency count for each entity
            entity_frequency[(entity_type, word)] += 1

    # Convert frequency dictionary to a list and sort by frequency
    sorted_entities = sorted(
        [{"entity": et[0], "word": et[1], "frequency": freq} for et, freq in entity_frequency.items()],
        key=lambda x: x["frequency"],
        reverse=True
    )

    return {"entities": sorted_entities}
