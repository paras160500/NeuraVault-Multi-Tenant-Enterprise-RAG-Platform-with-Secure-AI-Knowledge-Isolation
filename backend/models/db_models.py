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

#---------------------------------------------------------------------------------
#                                   Usage Stats
#---------------------------------------------------------------------------------

class UsageStat(Document):
    user_id : Annotated[str , Indexed(unique = True)]
    queries_today : int = 0 
    uploads_today : int = 0
    total_queries : int = 0 
    total_uploads : int = 0
    last_reset : datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "usage_stats"

    async def reset_daily(self):
        if self.last_reset.date() < datetime.utcnow().date():
            self.queries_today = 0
            self.uploads_today = 0 
            self.last_reset = datetime.utcnow()
            await self.save()


#---------------------------------------------------------------------------------
#                            Pydantic Req / Resp Schemas
#---------------------------------------------------------------------------------

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password : str 


class UserLogin(BaseModel):
    username : str 
    password : str 


class TokenResponse(BaseModel):
    access_token : str 
    refresh_token : str 
    token_type : str = "bearer"


class UserOut(BaseModel):
    user_id : str 
    email : str 
    username : str 
    plan : str 
    created_at : datetime


