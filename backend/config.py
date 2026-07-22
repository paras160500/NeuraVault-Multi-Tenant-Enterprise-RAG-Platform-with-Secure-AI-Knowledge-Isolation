"""
    This file replace the old dotenv functionality with the new 
    Centralised settins loaded from .env
"""

#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List 

#---------------------------------------------------------------------------------
#                                   Pydantic Setting Class
#---------------------------------------------------------------------------------

class Settings(BaseSettings):

    # JWT
    jwt_secret_key : str
    jwt_algorithm : str = "HS256"
    jwt_access_token_expire_minutes : int = 60
    jwt_refresh_token_expire_days : int = 7 

    # MongoDB
    mongodb_url : str 
    mongodb_db_name : str = "tenant_rag_saas"

    # Pinecone 
    pinecone_api_key : str 
    pinecone_environment : str = "us-east-1"
    pinecone_index_name : str = "tenant-rag-sass-index"

    # OpenAI
    openai_api_key : str 
    openai_embedding_model : str = "text-embedding-3-small"

    # GROQ
    groq_api_key : str 
    groq_model : str = "llama-3.3-70b-versatile"

    # Rate limiting
    rate_limit_per_minute : int = 20 
    rate_limit_upload_per_day : int = 50

    # CROS
    allowed_origins : str = "http://localhost:8501"

    # App
    app_env : str = "development"
    log_level : str = "INFO"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def origins_list(self) -> List[str]:
        """
            Take the allowed_origins list and then make a list from it 
            by splitting based on the ','
            Returns:
                List[str] -> Return list of all url which passed in the allowed_origins in .env file
        """
        return [o.strip() for o in self.allowed_origins.split(",")]


# LRU_CACHE :- for each file it will have multiple Settings() so instead it will make only one Settings()
#              and use that for all the time means no need to make multiple Settings object
@lru_cache
def get_settings() -> Settings:   
    """
        Returns the Settings object
    """          
    return Settings()

# for outside func
settings = get_settings()