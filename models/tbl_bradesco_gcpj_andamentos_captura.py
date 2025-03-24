from sqlalchemy import Column, BIGINT, BOOLEAN, TEXT, VARCHAR
from sqlalchemy.sql import expression
from .db import Base
from .crud import CRUDMixin
SCHEMA = 'bancos'

class TblBradescoGcpjAndamentosCaptura(Base, CRUDMixin):
    __tablename__ = 'tbl_bradesco_gcpj_andamentos_captura'
    __table_args__ = {'schema': SCHEMA}

    id = Column(BIGINT, primary_key=True, nullable=False, server_default=f"nextval('{SCHEMA}.tbl_bradesco_gcpj_andamentos_captura_id_seq'::regclass)")
    gcpj = Column(VARCHAR)
    capturado = Column(BOOLEAN, default=False, server_default=expression.false())
    erro = Column(TEXT)

    fillable = ['gcpj', 'capturado', 'erro']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'capturado': ['boolean'],
    #         'erro': ['string'],
    #     }

