# create_tables.py
from models.db import engine, Base
# Importe todos os models para registrar as tabelas
from models.tbl_bb_bot_registros_primeira_sentenca import TblBbBotRegistros1Sentenca
from models.tbl_bb_bots_controle import TblBbBotsControle


# Cria todas as tabelas definidas nos models
Base.metadata.create_all(bind=engine)
