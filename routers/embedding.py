from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import get_model
from utils.text_processing import correct_sentence_spacing
from functools import lru_cache

router = APIRouter(prefix="/embed", tags=["Embedding Generation"])

# Caching mechanism for embeddings
@lru_cache(maxsize=1024)
def get_embedding(text: str):
    model = get_model("embedding")
    return model.encode(text).tolist()

@router.post("/", dependencies=[Depends(get_api_key)])
async def embed(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)
    # Generate the embedding
    embedding = get_embedding(corrected_text)
    return {"embedding": embedding}
