from jose import JWTError, jwt
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def decode_access_token(token: str):
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Token decoded:", payload)
        return payload
    except JWTError as e:
        print("JWT decoding error:", e)
        raise

