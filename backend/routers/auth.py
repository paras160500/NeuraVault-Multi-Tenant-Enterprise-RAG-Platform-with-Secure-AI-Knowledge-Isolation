#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime 
from backend.models.db_models import (
    User, UserCreate,UserLogin, TokenResponse, UserOut, UsageStat
)
from backend.utils.auth import(
    hash_password,verify_password,
    create_Access_token,create_refresh_token,
    decode_token,get_current_user
)


#---------------------------------------------------------------------------------
#                                   Logic Statements
#---------------------------------------------------------------------------------

router = APIRouter(prefix="/auth" , tags = ["Authentication"])

@router.post("/register" , response_model=UserOut , status_code=201)
async def register(payload : UserCreate):
    """
        For Registering the user in the system
        Args:
            payload(UserCreate) : Check UserCreate model in db_models in models
        Returns:
            UserOut object
    """

    # Check if the username and email already avaibale or not 
    if await User.find_one(User.email == payload.email):
        raise HTTPException(status_code=400 , detail = "Email already registered")
    if await User.find_one(User.username == payload.username):
        raise HTTPException(status_code=400 , detail = "Username already taken")

    # Creating user 
    user = User(
        email = payload.email,
        username=payload.username,
        hashed_password=hash_password(payload.password)
    )
    # Namespace = user_id for Pinecone isolation
    user.pinecone_namespace = user.user_id

    # Insert data to mongo
    await user.insert()

    # Insert UsageStat to mongo
    await UsageStat(user_id=user.user_id).insert()

    # Returning the UserOut object for future usage
    return UserOut(
        user_id = user.user_id,
        email = user.email ,
        username = user.username,
        plan = user.plan,
        created_at=user.created_at
    )


@router.post("/login" , response_model=TokenResponse)
async def login(payload : UserLogin):
    """
        For Login the user in the system
        Args:
            payload(UserLogin) : Check UserLogin model in db_models in models
        Returns:
            TokenResponse object
    """

    # First get the user 
    user = await User.find_one(User.username == payload.username)

    # Check the user is there or not and password is valid or not
    if not user or not verify_password(payload.password , user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check if user is active or not 
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail = "Account Disabled")

    # Return TokenResponse object
    return TokenResponse(
        access_token=create_Access_token(user.user_id , user.username),
        refresh_token=create_refresh_token(user.user_id)
    )


@router.post("/refresh" , response_model=TokenResponse)
async def refresh(refresh_token : str):
    """
    
    """
    # first decode the refresh token
    payload = decode_token(refresh_token)

    # check if the type of the refresh token is refresh or not 
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Not a Refresh Token")

    # Getting the user based on the payload key name sub
    user = await User.find_one(User.user_id == payload['sub'])

    # Check if user is available or not 
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User not found")

    return TokenResponse(
        access_token=create_Access_token(user.user_id , user.username),
        refresh_token=create_refresh_token(user.user_id)
    )


@router.get("/me" , response_model=UserOut)
async def me(current_user : User = Depends(get_current_user)):
    """
        Get current user based on the JWT tokens and then return it 
        Args:
            current_user(User) : This depends on get_current_user which is taking the JWT bearer token and get userid
        Returns:
            UserOut object
    """
    return UserOut(
        user_id = current_user.user_id,
        email = current_user.email ,
        username = current_user.username,
        plan = current_user.plan,
        created_at=current_user.created_at
    )