from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import sentiment_analyzer
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def sentiment(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)

    # Truncate text to the first 512 tokens
    encoded_text = sentiment_analyzer.tokenizer.encode(corrected_text, truncation=True, max_length=512)

    # Decode back to string
    truncated_text = sentiment_analyzer.tokenizer.decode(encoded_text, skip_special_tokens=True)

    # Analyze sentiment
    result = sentiment_analyzer(truncated_text)
    return {"sentiment": result}
