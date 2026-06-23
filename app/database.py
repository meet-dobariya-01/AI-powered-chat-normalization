import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from app.config import settings

# Initialize logging for database operations
logger = logging.getLogger("fluentchat.database")

class DatabaseManager:
    """
    DatabaseManager handles the lifecycle of the MongoDB client connection.
    It encapsulates the Motor client and database references.
    """
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def connect_to_database(self):
        """
        Establishes a connection to the MongoDB Atlas cluster
        and initializes the database and required collections.
        """
        logger.info("Connecting to MongoDB Atlas...")
        try:
            # Initialize the asynchronous Motor client with the loaded connection string
            self.client = AsyncIOMotorClient(settings.MONGODB_URL)
            # Reference the database (creates it on MongoDB Atlas if it doesn't exist)
            self.db = self.client[settings.DATABASE_NAME]
            
            # Send a ping to verify that the client can successfully reach the cluster
            # This triggers DNS resolution and SSL handshake immediately
            await self.client.admin.command('ping')
            logger.info("Successfully connected to MongoDB Atlas!")
            
            # Explicitly create collections if they don't exist
            existing_cols = await self.db.list_collection_names()
            for col_name in ["users", "rooms", "messages"]:
                if col_name not in existing_cols:
                    await self.db.create_collection(col_name)
                    logger.info(f"Explicitly created collection: {col_name}")
            
            # Initialize collection references
            self.users = self.db["users"]
            self.rooms = self.db["rooms"]
            self.messages = self.db["messages"]
            
        except ConnectionFailure as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during database initialization: {e}")
            raise e

    async def close_database_connection(self):
        """
        Closes the connection pool of the Motor client.
        """
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB Atlas connection pool.")

# Global instance of the DatabaseManager
db_manager = DatabaseManager()

# Dependency injection helpers to retrieve database and collection references
async def get_db():
    """
    Dependency helper to retrieve the database instance.
    """
    return db_manager.db

async def get_users_collection():
    """
    Dependency helper to retrieve the 'users' collection.
    """
    return db_manager.db["users"]

async def get_rooms_collection():
    """
    Dependency helper to retrieve the 'rooms' collection.
    """
    return db_manager.db["rooms"]

async def get_messages_collection():
    """
    Dependency helper to retrieve the 'messages' collection.
    """
    return db_manager.db["messages"]
