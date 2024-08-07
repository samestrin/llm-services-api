import re
import spacy

# Load spaCy model for sentence splitting
nlp = spacy.load("en_core_web_sm")

def correct_sentence_spacing(text: str) -> str:
    """
    Correct common spacing issues in text.
    """
    # Use spaCy to split text into sentences
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    # Join sentences with a single space between them
    corrected_text = " ".join(sentences)

    # Use regular expressions to fix common punctuation issues
    corrected_text = re.sub(r",(\S)", r", \1", corrected_text)  # Space after commas
    corrected_text = re.sub(r"(\.\s*)([A-Za-z])", r". \2", corrected_text)  # Space after periods
    corrected_text = re.sub(r"([!?,;:])(\S)", r"\1 \2", corrected_text)  # Space after punctuation
    corrected_text = re.sub(r"\s{2,}", " ", corrected_text)  # Remove multiple spaces
    corrected_text = corrected_text.strip()  # Trim leading and trailing spaces

    # Define common abbreviations
    abbreviations = [
        "U\\.", "I\\.", "P\\.", "R\\.", "B\\.", "O\\.", "S\\.", "J\\.", "A\\."
    ]

    # Create a regex pattern for all abbreviations
    abbrev_pattern = "|".join(abbreviations)

    # Handle common abbreviation spacing issues
    corrected_text = re.sub(rf"\b({abbrev_pattern})\b", lambda m: m.group(0).replace(" ", ""), corrected_text)
    corrected_text = re.sub(rf"(\b{abbrev_pattern})\s+(\b{abbrev_pattern})", r"\1\2", corrected_text)
    corrected_text = re.sub(rf"\s({abbrev_pattern})", r" \1", corrected_text)

    return corrected_text

def chunk_text(text, tokenizer, max_length=512, overlap=50):
    """
    Chunk text into manageable pieces using a sliding window approach.
    """
    tokens = tokenizer.encode(text, truncation=False)
    total_tokens = len(tokens)
    chunks = []

    # Create overlapping chunks
    for i in range(0, total_tokens, max_length - overlap):
        # Get tokens for the current chunk, ensure we don't exceed total token length
        chunk_tokens = tokens[i:i + max_length]

        # Decode tokens back to text
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks

def count_tokens(text: str, model_name: str) -> int:
    """
    Count the number of tokens in a text string.
    """
    # This function uses a simple word split as a proxy for token count
    # Adjust this method if using a tokenizer specific to your models
    tokens = text.split()
    return len(tokens)
