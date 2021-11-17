from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY
# Algorithm
# Expriation time

# secret key dibuat pake linux run code : "openssl rand -hex 32"
SECRET_KEY = "3b56f6aa9c1c0462298fc8bafa0e88092790750cb00de73d02d15eaac5a6809a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def crate_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
        token_data = schemas.tokenData(id=id)

    except JWTError:
        raise credential_exception


    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"could not Validate credential",
                                         headers={"www-Authenticate": "Bearer"})

    return verify_access_token(token, credential_exception)
