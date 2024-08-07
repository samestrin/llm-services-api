from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
API_KEY = os.getenv("API_KEY")

# Define the header that will contain the API key
api_key_header = APIKeyHeader(name="Authorization")

# Dependency for API key authentication
async def get_api_key(api_key: str = Depends(api_key_header)):
    """
    Retrieve and verify the API key from the request header in the Bearer <token> format.

    Args:
        api_key (str): The API key provided in the request header.

    Raises:
        HTTPException: If the API key is invalid, raise a 403 Unauthorized exception.

    Returns:
        str: The valid API key.
    """
    # Verify that the API key matches the expected format and value
    expected_api_key = f"Bearer {API_KEY}"
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    return api_key
