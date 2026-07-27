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


    #------------------------------------Auth Logic----------------------------------------

    def upload_document(self , file_bytes : bytes , filename : str) -> dict:
        """
            For calling the upload document endpoint and pass the files and headers to them
        """
        # File upload is not having content type as json so we cant override that so we 
        # are passing the "Authorization" key by ourself.
        r = self.session.post(f"{BASE_URL}/documents/upload" , 
                              files = {"file" : (filename , file_bytes)},
                              headers={"Authorization" : f"Bearer {self.access_token}"})
        return r.json() , r.status_code

    def list_documents(self) -> dict:
        """
            For calling the list_document endpoint and pass the headers to them
        """
        r = self.session.get(f"{BASE_URL}/documents/" , headers=self._headers())
        return r.json() , r.status_code

    def delete_document(self , doc_id : str) -> int:
        """
            For calling the deletedocument endpoint and passing the headers to them
        """
        r = self.session.delete(f"{BASE_URL}/documents/{doc_id}" , headers = self._headers())
        return r.status_code

    def get_document(self,doc_id : str) -> dict:
        """
            For calling the get document endpoint on doc_id and passing the headers to them
        """
        r = self.session.get(f"{BASE_URL}/documents/{doc_id}" , headers=self._headers())
        return r.json() , r.status_code()


    #------------------------------------Stats Logic----------------------------------------

    def get_stats(self) -> dict:
        """
            For calling the get_stats endpoint and passing the headers to them
        """
        r = self.session.get(f"{BASE_URL}/stats/" , headers=self._headers())
        return r.json() , r.status_code
    
    def get_namespace_stats(self) -> dict:
        """
            For calling the getnamespace status endpoint and passing the headers to them
        """
        r = self.session.get(f"{BASE_URL}/stats/namespace", headers=self._headers())
        return r.json() , r.status_code