from sqlalchemy import Column, BIGINT, BOOLEAN, VARCHAR
from sqlalchemy.sql import expression
from .db import Base
from .crud import CRUDMixin
SCHEMA = 'bancos'

class TblBradescoGcpjAndamentosEnvio(Base, CRUDMixin):
    __tablename__ = 'tbl_bradesco_gcpj_andamentos_envio'
    __table_args__ = {'schema': SCHEMA}

    id = Column(BIGINT, primary_key=True, nullable=False, server_default=f"nextval('{SCHEMA}.tbl_bradesco_gcpj_andamentos_envio_id_seq'::regclass)")
    ordem_servico = Column(BIGINT)
    planilha = Column(VARCHAR)
    gravado = Column(BOOLEAN, default=False, server_default=expression.false())
    porcentagem = Column(VARCHAR)
    session_id = Column(VARCHAR)

    fillable = ['ordem_servico', 'planilha', 'gravado', 'porcentagem', 'session_id']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'gravado': ['boolean'],
    #     }

