from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from passlib.context import CryptContext
from sqlalchemy.sql.functions import user
from .schemas import Users
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, UserOTP
from .auth import AuthHandler
from fastapi.responses import JSONResponse
import math, random

from datetime import datetime, timedelta


app = FastAPI()
router = InferringRouter() 


auth_handler = AuthHandler()

@cbv(router)

class LawyerLogin:

    session: Session = Depends(get_db)

    def genrate_otp(self):
        digits = "0123456789"
        OTP = ""
        for i in range(4) :
            OTP += digits[math.floor(random.random() * 10)]
    
        return OTP

    @router.get("/login-mail")
    def check_for_mail(self, email: str):
        try: 
            user_obj = self.session.query(User).filter(User.email == email).first()
            if user_obj:
                if user_obj and user_obj.is_lawyer:
                    otp = self.genrate_otp()
                    otp_data = {'user_id':user_obj.id, 'otp': otp, 'created': datetime.now(), 'modified': datetime.now()}
                    user_otp = UserOTP(**otp_data)
                    self.session.add(user_otp)
                    self.session.commit()
                    #send mail with this otp and make check for otp genration time
                    print(otp)
                    return True
                    # return [{'response': True, 'description': 'User with provided mail exists and its is a lawyer', 'timestamp': datetime}]

        except Exception as e:
            print(e)

    @router.get("/login-otp")
    def check_for_otp(self, otp: int, email: str):
        try:
            user_obj = self.session.query(User).filter(User.email == email).first()
            user_otp_obj = self.session.query(UserOTP).filter(UserOTP.user_id == user_obj.id)
            otp_flag = False
            for user_otp in user_otp_obj:
                if user_otp.created.strftime("%m/%d/%Y, %H:%M:%S") > (datetime.now() - timedelta(minutes=10)).strftime("%m/%d/%Y, %H:%M:%S"):
                    if user_otp.otp == otp:
                        otp_flag = True
                    #send mail to this email with this otp
            if otp_flag:
                token = auth_handler.encode_token(user_obj.email)
                return token
            else:
                return False
        except Exception as e:
            print(e)



@app.get('/')
def get_user(id: int, db: Session = Depends(get_db)):
    print(id)
    try:
        return db.query(User).filter(User.id == id).first()
    except Exception as e:
        print(e)

app.include_router(router)