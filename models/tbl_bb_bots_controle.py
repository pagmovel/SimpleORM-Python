from sqlalchemy import Column, BIGINT, BOOLEAN, TIMESTAMP, VARCHAR
from .db import Base
from .crud import CRUDMixin

class TblBbBotsControle(Base, CRUDMixin):
    __tablename__ = 'tbl_bb_bots_controle'
    __table_args__ = {'schema': 'bancos'}

    id = Column(BIGINT, primary_key=True, nullable=False)
    nome_bot = Column(VARCHAR, nullable=False)
    robo_ativo = Column(BOOLEAN, nullable=False)
    iniciado_em = Column(TIMESTAMP)
    encerrado_em = Column(TIMESTAMP)
    apresentou_erro = Column(BOOLEAN, nullable=False)
    iniciar = Column(BOOLEAN)
    user_login = Column(VARCHAR)
    ordem_servico = Column(BIGINT, nullable=False)

    fillable = ['nome_bot', 'robo_ativo', 'iniciado_em', 'encerrado_em', 'apresentou_erro', 'iniciar', 'user_login', 'ordem_servico']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'nome_bot': ['required'],
    #         'robo_ativo': ['required', 'boolean'],
    #         'apresentou_erro': ['required', 'boolean'],
    #         'iniciar': ['boolean'],
    #         'ordem_servico': ['required'],
    #     }

