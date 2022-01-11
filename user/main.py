from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from passlib.context import CryptContext
from .schemas import Users
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .auth import AuthHandler

from datetime import datetime, timedelta

app = FastAPI()

# class AuthHandler():
#     security = HTTPBearer()
#     pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#     secret = "123456"


#     def get_password_hash(self, password):
#         return self.pwd_context.hash(password)

#     def verify_password(self, plain_password, hashed_password):
#         return self.pwd_context.verify(plain_password, hashed_password)

#     def encode_token(self, user_name):
#         payload = {
#             'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
#             'iat': datetime.utcnow(),
#             'sub': user_name
#         }

#         return jwt.encode(
#             payload,
#             self.secret,
#             algorithm="HS256"
#         )

#     def decode_token(self, token):
#         try:
#             payload = jwt.decode(token, self.secret, algorithms=["HS256"])
#             return payload['sub']
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail='Signature Has Expired')
#         except jwt.InvalidTokenError as e:
#             raise HTTPException(status_code=401, detail='Invalid Token')

#     def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
#         return self.decode_token(auth.credentials)
auth_handler = AuthHandler()
@app.post('/api-token-auth')
def login(request: Users, db: Session = Depends(get_db)):
    try:
        pas = auth_handler.get_password_hash(request.username)
        print(pas)
        user_obj = db.query(User).filter(User.username == request.username).first()
        print(user_obj)
        iden = auth_handler.identify_hash(user_obj.password)
        print(iden)
        veri = auth_handler.verify_password(request.password, user_obj.password)
        print(veri)
        if veri:
            return auth_handler.encode_token(request.username)
        return request
    except Exception as e:
        print(e)

@app.get('/')
def get_user(id: int, db: Session = Depends(get_db)):
    print(id)
    try:
        return db.query(User).filter(User.id == id).first()
    except Exception as e:
        print(e)