from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils.auth_utils import create_access_token, verify_password
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

auth_routes = APIRouter()

# Simulated user database with hashed passwords
fake_users_db = {
    "pclay": {"username": "pclay", "password": "$2b$12$N9qo8uLOickgx2ZMRZo4i.e9S.t6Lb.CeTg2gR0Y3VhXc8N5zPiPe"}  # bcrypt-hashed 'password123'
}

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        return None
    return user

@auth_routes.post("/token", summary="Login and get access token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
