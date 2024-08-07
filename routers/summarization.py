from fastapi import APIRouter, HTTPException, Depends
from schemas.requests import TextRequest
from utils.auth import get_api_key
from models.nlp_models import summarizer
from utils.text_processing import correct_sentence_spacing

router = APIRouter(prefix="/summarize", tags=["Summarization"])

@router.post("/", dependencies=[Depends(get_api_key)])
async def summarize(request: TextRequest):
    corrected_text = correct_sentence_spacing(request.text)

    # Generate the summary with adjusted parameters using BART
    summary = summarizer(
        corrected_text,
        max_length=450,  # Adjust maximum length based on the desired summary length
        min_length=150,  # Adjust minimum length to ensure a decent-sized summary
        do_sample=False,  # Use deterministic summarization with BART
        num_beams=4,     # Use beam search for better results
        early_stopping=True,  # Stop when all beams finish
        clean_up_tokenization_spaces=True  # Suppress warning by setting explicitly
    )

    return {"summary": summary[0]["summary_text"]}
