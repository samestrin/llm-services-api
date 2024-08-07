from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import get_model
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/paraphrase", tags=["Paraphrasing"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def paraphrase(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)
    # Get paraphrasing model
    paraphraser = get_model("paraphrase", "Vamsi/T5_Paraphrase_Paws")
    # Paraphrase text
    paraphrased = paraphraser(
        f"paraphrase: {corrected_text}", 
        max_length=150, 
        num_return_sequences=1, 
        do_sample=True, 
        temperature=0.9
    )
    return {"paraphrased_text": paraphrased[0]["generated_text"]}
