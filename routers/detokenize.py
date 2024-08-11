from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import DetokenizeRequest
from models.nlp_models import get_model
from utils.auth import get_api_key

router = APIRouter(prefix="/detokenize", tags=["Detokenization"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def detokenize(request: DetokenizeRequest):    
    # Use the provided model or default to the embedding model
    model_name = request.model if request.model else "all-MiniLM-L6-v2"
        
    try:
        tokenizer = get_model("embedding", model_name).tokenizer
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Detokenize the tokens back to text
    decoded_text = tokenizer.decode(request.tokens, skip_special_tokens=True)
    
    return {"text": decoded_text}
