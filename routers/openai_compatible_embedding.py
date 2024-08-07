# routers/openai_compatible_embedding.py
from fastapi import APIRouter, HTTPException, Header, Depends
from schemas.requests import EmbeddingRequest
from models.nlp_models import get_model
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/v1/embeddings", tags=["OpenAI-Compatible Embeddings"])

@router.post("/")
async def openai_compatible_embedding(
    request: EmbeddingRequest
):
    """
    Generate embeddings in an OpenAI API-compatible format.
    """

    # Correct the input text
    corrected_text = correct_sentence_spacing(request.input)

    # Retrieve model from request or use default from config
    model_name = request.model if request.model else "all-MiniLM-L6-v2"
    try:
        embedding_model = get_model("embedding", model_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Generate embedding
    embedding = embedding_model.encode(corrected_text).tolist()

    # Simulate OpenAI's embedding API response format
    response = {
        "object": "list",
        "data": [
            {
                "object": "embedding",
                "index": 0,
                "embedding": embedding,
            }
        ],
        "model": model_name,
        "usage": {
            "prompt_tokens": len(corrected_text.split()),  # Rough approximation
            "total_tokens": len(corrected_text.split()),
        }
    }

    return response
