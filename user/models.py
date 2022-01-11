from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.sql.schema import Column
from .database import Base

class User(Base):
    __tablename__ = 'users_user'

    id = Column(Integer, primary_key = True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, nullable=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    name = Column(String, nullable=True)
    is_staff = Column(Boolean, nullable=True)
    is_active = Column(Boolean, nullable=True)
    last_login = Column(DateTime, nullable=True)
    date_joined = Column(DateTime, nullable=True)



