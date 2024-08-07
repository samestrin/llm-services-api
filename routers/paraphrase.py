from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import paraphraser
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/paraphrase", tags=["Paraphrasing"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def paraphrase(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)

    # Paraphrase text using a more appropriate model
    paraphrased = paraphraser(
        f"paraphrase: {corrected_text}", 
        max_length=150, 
        num_return_sequences=1, 
        do_sample=True, 
        temperature=0.9
    )
    
    # Output the paraphrased text without the prefix
    return {"paraphrased_text": paraphrased[0]["generated_text"]}
