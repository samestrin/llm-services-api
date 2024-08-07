from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.middleware import add_security_headers
from routers import summarization, sentiment, entities, paraphrase, keywords, embedding
import uvicorn
import logging

# Initialize the FastAPI app
app = FastAPI()

# CORS configuration to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Add security headers middleware
app.middleware("http")(add_security_headers)

# Include routers
app.include_router(summarization.router)
app.include_router(sentiment.router)
app.include_router(entities.router)
app.include_router(paraphrase.router)
app.include_router(keywords.router)
app.include_router(embedding.router)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # Run the app with Uvicorn for better performance
    uvicorn.run(app, host="0.0.0.0", port=5000)
