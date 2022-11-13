from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse



scheme = OAuth2PasswordBearer(tokenUrl="login")

#Secret key has been created by running "openssl rand -hex 32"
# command on a terminal 

def get_current_user(token: str = Depends(scheme)):
    if token=="12345":
        error =[]
        error.append("Please Log In For this request")
        return RedirectResponse("http://127.0.0.1:8000/books")
    #print("here is the token " + token)
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    #print(token)
    return token

SECRET_KEY = "002b619e2036cf40cc5fd5fa6675fd76d1c8b82b8df8754a620bd1bcb847de0d"
expiretime = 60 
def create_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expiretime)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

    return encoded_jwt

def verify_access_token(token :str , credentials_exception):
    data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    id: str = data.get("user_id")
    if id is None:
        raise credentials_exception 
    return id





