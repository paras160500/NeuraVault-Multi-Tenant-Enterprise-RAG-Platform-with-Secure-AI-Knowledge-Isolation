#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

from datetime import datetime 
from typing import Optional,List,Annotated
from pydantic import BaseModel, EmailStr, Field 
import uuid 
from beanie import Document, Indexed

#---------------------------------------------------------------------------------
#                                   User Class Defination
#---------------------------------------------------------------------------------

class User(Document):
    user_id : str = Field(default_factory=lambda : str(uuid.uuid4()))
    email : Annotated[EmailStr , Indexed(unique = True)]                    # Make it unique and index for fast search
    username : Annotated[str , Indexed(unique = True)]                      # Make it unique and index for fast search
    hashed_password : str 
    is_active : bool = True 
    is_verified : bool = False 
    plan : str = "free"
    pinecone_namespace : str = ""                                           # Isolated namespace = user_id
    created_at : datetime = Field(default_factory=datetime.utcnow)
    updated_at : datetime = Field(default_factory=datetime.utcnow)

    class Settings:                                                         # For telling mongodb which collection to use
        name = "users"

    class Config:                                                           # For pydantic Swagger for /docs url
        json_schema_extra = {                                               # to show how the input box look like
            "example" : {
                "email" : "alice@example.come",
                "username" : "alice"
            }
        }