#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------
import os 
import requests
from typing import Optional
from dotenv import load_dotenv
import streamlit as st 

load_dotenv()

BASE_URL = os.getenv("BACKEND_URL")

#---------------------------------------------------------------------------------
#                                   Class Statements
#---------------------------------------------------------------------------------

if not BASE_URL:
    raise ValueError("BACKEND_URL is not configured")

class APIClient:

    # Initializer for client with access token, it will set up token and session
    def __init__(self,access_token : Optional[str] = None):
        self.access_token = access_token
        self.session = requests.Session()

    # function that create headers
    def _headers(self) -> dict:
        """
            For creating headers for the backend to pass the auth tokens
            Returns:
                dict having the Content-Type and Authorization as key
        """
        h = {"Content-Type" : "application/json"}
        if self.access_token:
            h['Authorization'] = f"Bearer {self.access_token}"
        return h 


    #------------------------------------Auth Logic----------------------------------------

    def register(self, email : str , username : str , password : str):
        """
            For registering the user on the database
            Args:
                email(str) : Email of user
                username(str) : Username of user
                password(str) : Password of user
            Returns:
                returns a response and statuscode
        """
        r = self.session.post(                      # We can do request.post but this is reusing of the things
            f"{BASE_URL}/auth/register",
            json={"email" : email , "username" : username , "password" : password} 
        )
        return r.json() , r.status_code

    def login(self , username : str , password : str):
        """
            For Logging in the user on the database
            Args:
                username(str) : Username of user
                password(str) : Password of user
            Returns:
                returns a response and statuscode
        """
        r = self.session.post(
            f"{BASE_URL}/auth/login",
            json={"username" : username , "password" : password}
        )
        return r.json() , r.status_code

    def me(self):
        """
            For getting self information
            Returns:
                it will return a response and status code
        """
        r = self.session.get(f"{BASE_URL}/auth/me" , headers=self._headers())
        return r.json() , r.status_code
    