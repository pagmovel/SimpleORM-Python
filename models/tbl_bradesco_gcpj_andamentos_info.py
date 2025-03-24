from sqlalchemy import Column, BIGINT, DATE, TEXT, VARCHAR
from .db import Base
from .crud import CRUDMixin
SCHEMA = 'bancos'

class TblBradescoGcpjAndamentosInfo(Base, CRUDMixin):
    __tablename__ = 'tbl_bradesco_gcpj_andamentos_info'
    __table_args__ = {'schema': SCHEMA}

    id = Column(BIGINT, primary_key=True, nullable=False, server_default=f"nextval('{SCHEMA}.tbl_bradesco_gcpj_andamentos_info_id_seq'::regclass)")
    data = Column(DATE)
    descricao = Column(TEXT)
    gcpj = Column(BIGINT)
    referencia = Column(VARCHAR)

    fillable = ['data', 'descricao', 'gcpj', 'referencia']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'descricao': ['string'],
    #     }

