from pydantic import BaseModel, constr, conlist
from typing import Optional

class TextRequest(BaseModel):
    """
    Schema for simple text requests.
    """
    text: constr(min_length=1, max_length=5000)

class EmbeddingRequest(BaseModel):
    """
    Schema for OpenAI-compatible embedding requests.
    """
    input: constr(min_length=1, max_length=5000)
    model: str

class TokenizeRequest(BaseModel):
    """
    Schema for OpenAI-compatible embedding requests.
    """
    text: constr(min_length=1, max_length=5000)
    model: Optional[str] = None  # Optional, defaults to embedding model
    
class DetokenizeRequest(BaseModel):
    tokens: conlist(int, min_length=1)
    model: Optional[str] = None  # Optional, defaults to embedding model
    