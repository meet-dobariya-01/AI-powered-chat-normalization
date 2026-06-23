from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    It automatically reads environment variables from a .env file
    in the current working directory.
    """
    # MongoDB connection URL (required)
    MONGODB_URL: str
    
    # Target database name (default: fluentchat)
    DATABASE_NAME: str = "fluentchat"
    
    # Application name
    APP_NAME: str = "FluentChat"
    
    # Debug mode flag
    DEBUG: bool = True

    # Pydantic configuration to load values from the environment file
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # Gracefully ignore other OS environment variables
    )

# Instantiate the settings object to be imported across the application
settings = Settings()
