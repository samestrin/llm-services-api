from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import get_model
from utils.text_processing import correct_sentence_spacing
from keybert import KeyBERT

router = APIRouter(prefix="/extract_keywords", tags=["Keyword Extraction"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def extract_keywords(request: TextRequest, num_keywords: int = Query(5, gt=0, le=20)):
    """
    Extract keywords from the given text. You can specify the number of keywords to return using `num_keywords`.
    """
    corrected_text = correct_sentence_spacing(request.text)
    # Get the keyword extraction model
    kw_model = get_model("keyword")  # Use the default model for keyword extraction
    keybert = KeyBERT(kw_model)  # Initialize KeyBERT with the loaded model

    # Extract keywords using KeyBERT
    keywords = keybert.extract_keywords(
        corrected_text,
        keyphrase_ngram_range=(1, 2),  # Consider both single and two-word phrases
        stop_words="english",  # Remove common stop words
        top_n=num_keywords  # Return the specified number of keywords
    )
    # Format keywords as a list of strings
    formatted_keywords = [{"keyword": kw, "score": score} for kw, score in keywords]
    return {"keywords": formatted_keywords}
