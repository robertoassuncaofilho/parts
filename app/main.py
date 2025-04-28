from fastapi import FastAPI
from app.api import parts
from app.database import engine, Base
from app.cache import cache
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Parts API",
    description="REST API for managing parts",
    version="0.1.0"
)

# Include routers
app.include_router(parts.router, prefix="/parts", tags=["parts"])

@app.on_event("startup")
def startup():
    """
    Initialize services on startup.
    """
    # Clear cache on startup
    cache.clear() 