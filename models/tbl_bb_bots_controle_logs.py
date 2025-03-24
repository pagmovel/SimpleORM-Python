from sqlalchemy import Column, BIGINT, TIMESTAMP, VARCHAR
from .db import Base
from .crud import CRUDMixin

class TblBbBotsControleLogs(Base, CRUDMixin):
    __tablename__ = 'tbl_bb_bots_controle_logs'
    __table_args__ = {'schema': 'bancos'}

    id = Column(BIGINT, primary_key=True, nullable=False)
    bb_bots_controle_id = Column(BIGINT, nullable=False)
    descricao = Column(VARCHAR)
    user_login = Column(VARCHAR)
    created_at = Column(TIMESTAMP)

    fillable = ['bb_bots_controle_id', 'descricao', 'user_login', 'created_at']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'bb_bots_controle_id': ['required'],
    #     }

