from sqlalchemy import Column, BIGINT, TIMESTAMP, VARCHAR
from .db import Base
from .crud import CRUDMixin

class User(Base, CRUDMixin):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'finampe'}

    id = Column(BIGINT, primary_key=True, nullable=False)
    name = Column(VARCHAR, nullable=False)
    email = Column(VARCHAR, nullable=False)
    email_verified_at = Column(TIMESTAMP)
    password = Column(VARCHAR, nullable=False)
    remember_token = Column(VARCHAR)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    fillable = ['name', 'email', 'email_verified_at', 'password', 'remember_token', 'created_at', 'updated_at']

    aliases = {
        'nome': 'name'
    }
    
    @classmethod
    def rules(cls):
        return {
            'name': ['required'],
            'email': ['required'],
            'password': ['required'],
        }

