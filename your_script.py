from auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
)
from datetime import timedelta

# Test the functions
if __name__ == "__main__":
    # Test password hashing
    password = "password123"
    hashed_password = get_password_hash(password)
    print("Hashed Password:", hashed_password)

    # Test password verification
    is_valid = verify_password(password, hashed_password)
    print("Password Verified:", is_valid)

    # Test JWT token generation
    token = create_access_token({"sub": "pclay"}, expires_delta=timedelta(minutes=30))
    print("Generated Token:", token)

    # Test JWT token decoding
    payload = decode_access_token(token)
    print("Decoded Payload:", payload)
