import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings
from app.database import db_manager, get_db

# Configure Python's standard logging library
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("fluentchat.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager that handles startup and shutdown events.
    Using lifespan is the modern, recommended production standard in FastAPI
    (replacing the deprecated startup and shutdown event decorators).
    """
    # ------------------ STARTUP ------------------
    # Establish connection pool to MongoDB Atlas when FastAPI starts
    try:
        await db_manager.connect_to_database()
    except Exception as e:
        logger.error(f"Database connection setup failed during app startup: {e}")
        # In production, failing to connect to the primary database should prevent server startup
        raise e
        
    yield  # Hand over control to FastAPI to start accepting incoming HTTP requests
    
    # ------------------ SHUTDOWN -----------------
    # Cleanly terminate the connection pool to MongoDB Atlas when FastAPI stops
    await db_manager.close_database_connection()

# Initialize the FastAPI App instance
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

@app.get("/")
async def root():
    """
    Root endpoint checking if the API is running.
    """
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "message": f"Welcome to the {settings.APP_NAME} Backend API!"
    }

@app.get("/test-connection")
async def test_connection(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Verification API endpoint that checks connectivity to MongoDB Atlas.
    
    - Uses Depends(get_db) to fetch the active database instance.
    - Sends a 'ping' command to check latency / connection status.
    - Lists active collections inside the 'fluentchat' database.
    """
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not initialized."
        )
    
    try:
        # Run a quick ping command to ensure connection is live
        await db.client.admin.command('ping')
        
        # Get all collection names from the database
        collections = await db.list_collection_names()
        logger.info(f"Retrieved collections: {collections}")
        
        return {
            "status": "connected",
            "message": "Successfully connected to MongoDB Atlas cluster!",
            "database_name": db.name,
            "available_collections": collections,
            "expected_collections": ["users", "rooms", "messages"]
        }
    except Exception as e:
        logger.error(f"MongoDB connection test failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connectivity test failed: {str(e)}"
        )
