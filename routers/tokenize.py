from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TokenizeRequest
from models.nlp_models import get_model
from utils.auth import get_api_key 
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/tokenize", tags=["Tokenization"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def tokenize(request: TokenizeRequest):
    corrected_text = correct_sentence_spacing(request.text)
    
    # Use the provided model or default to the embedding model
    model_name = request.model if request.model else "all-MiniLM-L6-v2"
    
    try:
        tokenizer = get_model("embedding", model_name).tokenizer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Tokenize the text
    tokens = tokenizer.encode(corrected_text, return_tensors='pt').tolist()[0]
    
    return {"tokens": tokens}
