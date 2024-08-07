from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader

# Define API key for authentication
API_KEY = "your-secure-api-key"  # Replace with your actual API key
api_key_header = APIKeyHeader(name="Authorization")

# Dependency for API key authentication
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
