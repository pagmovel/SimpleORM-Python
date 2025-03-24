from sqlalchemy import Column, BIGINT, TEXT, TIMESTAMP, VARCHAR, ForeignKey
from .db import Base
from .crud import CRUDMixin

class TblBbBotRegistros1Sentenca(Base, CRUDMixin):
    __tablename__ = 'tbl_bb_bot_registros_primeira_sentenca'
    __table_args__ = {'schema': 'bancos'}

    id = Column(BIGINT, primary_key=True, nullable=False)
    bot_controle_id = Column(BIGINT, ForeignKey('bancos.tbl_bb_bots_controle.id'), nullable=False)
    npj = Column(VARCHAR, nullable=False)
    cadastro = Column(VARCHAR)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    tags_analise_riscos = Column(TEXT)
    cod_tarefa = Column(BIGINT)
    nome_evento = Column(VARCHAR)
    tag_tarefa = Column(TEXT)
    tag_pasta = Column(TEXT)
    pasta_id = Column(BIGINT)

    fillable = ['bot_controle_id', 'npj', 'cadastro', 'created_at', 'updated_at', 'tags_analise_riscos', 'cod_tarefa', 'nome_evento', 'tag_tarefa', 'tag_pasta', 'pasta_id']

    # @classmethod
    # def rules(cls):
    #     return {
    #         'bot_controle_id': ['required'],
    #         'npj': ['required'],
    #         'tags_analise_riscos': ['string'],
    #         'tag_tarefa': ['string'],
    #         'tag_pasta': ['string'],
    #     }

