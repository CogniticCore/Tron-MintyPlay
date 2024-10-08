# python -m venv tron-backend-env
# tron-backend-env/Scripts/activate
# pip install -r requirements.txt
# uvicorn app.main:app --reload

import logging
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import v1
from .core.database import client

# Load environment variables from .env file securely
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Mintyplay API",
    description="This is an APIs for MintyPlay by CogniticCore made for Tron Season 7 Hackathon Project",
    version="1.0.0",
    contact={
        "name": "",
    },
    license_info={}
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "https://mintyplay.vercel.app",
    "https://vercel.app",
    "https://vercel.com",
]

# Include the API router for version 1
app.include_router(v1.router)


@asynccontextmanager
async def startup_event():
    """
    Event triggered on application startup. Use this for initializing resources like
    database connections, logging systems, or checking service health status.
    """
    try:
        # Example: Checking MongoDB connection at startup
        await client.admin.command("ping")
        logger.info("Successfully connected to the database.")
    except Exception as e:
        logger.error(f"Error connecting to the database: {str(e)}")
        raise RuntimeError("Failed to connect to the database.")

@app.get("/", summary="Root Endpoint", tags=["Root"])
def root():
    """
    Root endpoint of the API. Use this to check if the API is up and running.
    
    Returns:
        dict: A message confirming the API is running.
    """
    return {"details": "This is the root. Check /docs for interactive documentation."}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

