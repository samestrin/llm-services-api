from pydantic import BaseModel, constr

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
