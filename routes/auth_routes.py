from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from utils.auth_utils import create_access_token, verify_password

# Simulated user database with hashed passwords
fake_users_db = {
    "pclay": {
        "username": "pclay",
        "password": "$2b$12$ICBgw0VHiercIpdo72HUF.hBUppmqw7EfTD5LGfDkOdhUy7cXzQIi"  # bcrypt-hashed 'password123'
    }
}

auth_routes = APIRouter()

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        print(f"User '{username}' not found in fake_users_db.")  # Debug
        return None
    if not verify_password(password, user["password"]):
        print(f"Password verification failed for user '{username}'.")  # Debug
        return None
    print(f"User '{username}' authenticated successfully.")  # Debug
    return user

@auth_routes.post("/token", summary="Login and get access token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Received username: {form_data.username}")
    print(f"Received password: {form_data.password}")
    
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        print("Authentication failed.")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
