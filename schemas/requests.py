from pydantic import BaseModel, constr

class TextRequest(BaseModel):
    text: constr(min_length=1, max_length=5000)
