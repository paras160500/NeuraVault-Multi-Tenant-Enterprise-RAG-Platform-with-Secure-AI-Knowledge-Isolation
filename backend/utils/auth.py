#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.config import settings
from backend.models.db_models import User 


#--------------------------------------------------------------------------------
#                                 Password Hashing
#--------------------------------------------------------------------------------

# bcrypt only accept 72 bytes so for the long password it will create error so the flow is below
# Original password -> SHA256 -> short fixed-size value -> bcrypt -> final hash

pwd_context = CryptContext(
    schemes=['bcrypt_sha256'],
    deprecated = "auto"
)

bearer_scheme = HTTPBearer()        # for like look inside the auth header and extract token after word Bearer


def hash_password(plain : str) -> str:
    """
        Hash user password safely first SHA256 and then bcrypt on password
        Args:
            plain(str) : user original password
        Returns:
            str : Hashed password string
    """
    return pwd_context.hash(plain)


def verify_password(plain : str , hashed : str) -> bool:
    """
        check the password is correct or not
        Args:
            plain(str) : original user entered password
            hashed(str) : hashed password from db
        Returns:
            return True is both plain and hashed are same otherwise return False
    """
    return pwd_context.verify(plain,hashed)


#--------------------------------------------------------------------------------
#                                 JWT Token Creation
#--------------------------------------------------------------------------------

def _create_token(data : dict , expires_delta : timedelta) -> str:
    """
        Generate JWT tokens from dict and expiretime
        Args:
            data(dict) : The data which need to convert into the JWT
            expires_delta(timedelta) : Time where the token will expire
    """
    payload = data.copy()
    payload.update({
        "exp" : datetime.utcnow() + expires_delta,
        "iat" : datetime.utcnow()
    })
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def create_Access_token(user_id : str , username : str) -> str:
    """
        Create a short-lived access token.
        Args:
            user_id(str) : id of user 
            username(str) : username 
        Returns:
            returns a string having the jwt access token
    """
    return _create_token(
        {
            "sub" : user_id,
            "username" : username,
            "type" : "access"
        },
        timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )


def create_refresh_token(user_id : str) -> str:
    """
        Create long-lived refresh token
        Args:
            user_id(str) : id of user 
            username(str) : username 
        Returns:
            returns a string having the jwt access token
    """
    return _create_token(
        {
            "sub" : user_id,                               # I am putting user_id only in refresh token because
            "type" : "refresh"                             # tomorrow username can change but not the userid 
        },                                                 # that is what my logic is
        timedelta(
            days=settings.jwt_refresh_token_expire_days
        )
    )


#--------------------------------------------------------------------------------
#                                  Token Verification
#--------------------------------------------------------------------------------

def decode_token(token : str) -> dict:
    """
        Decode and validate the JWT Token
        Args:
            token(str) : jwt token 
        Returns:
            dict : payload will return from here
    """
    try:
        payload = jwt.decode(
            token ,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate" : "Bearer"}          # Just telling the client that this api need bearer token
        )


#--------------------------------------------------------------------------------
#                                Current user Dependency
#--------------------------------------------------------------------------------

async def get_current_user(credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme))-> User:
    """
    
    """

    payload = decode_token(credentials.credentials)

    # Ensure the access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an access token"
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = await User.find_one(
        User.user_id == user_id
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "User inactive"
        )

    return user 