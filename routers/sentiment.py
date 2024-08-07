from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import get_model
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def sentiment(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)
    # Get sentiment analysis model
    sentiment_analyzer = get_model("sentiment", "distilbert-base-uncased-finetuned-sst-2-english")
    # Analyze sentiment
    result = sentiment_analyzer(corrected_text)
    return {"sentiment": result}
