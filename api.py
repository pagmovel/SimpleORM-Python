from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import pandas as pd
import datetime

# Importação dos modelos
from models.tbl_bb_bots_controle import TblBbBotsControle
from models.tbl_bb_bot_registros_primeira_sentenca import TblBbBotRegistros1Sentenca
from models.tbl_bb_bots_controle_logs import TblBbBotsControleLogs
from models.tarefas_table import TarefasTable

app = FastAPI()

# Configuração do CORS - ajuste os origins conforme necessário
origins = [
    "*",  # Permite qualquer origem. Em produção, especifique os domínios permitidos.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def gerar_planilha_excel(df: pd.DataFrame) -> BytesIO:
    """
    Gera uma planilha Excel a partir do DataFrame fornecido.
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Dados")
    writer.close()  # Use close() em vez de save() para evitar o FutureWarning
    output.seek(0)
    return output

def gerar_nome_arquivo(data_robo: datetime.datetime) -> str:
    """
    Gera o nome do arquivo usando a data_robo formatada no padrão dd/mm/YYYY HH:MM:SS.
    """
    data_str = data_robo.strftime("%d/%m/%Y %H:%M:%S")
    return f"Registros_de_Primeira_Sentença_{data_str}.xlsx"



@app.api_route("/download", methods=["GET", "POST"])
async def download(request: Request, bot_id: str = None):
    # Se for POST, tenta obter bot_id do corpo da requisição
    if request.method == "POST":
        body = await request.json()
        bot_id = body.get("bot_id", bot_id)
    
    if not bot_id:
        raise HTTPException(status_code=400, detail="bot_id é obrigatório")
    
    # Sequência solicitada: valida o conteúdo e coleta informações do bot
    bot_controle = TblBbBotsControle.findById(bot_id).to_dict()
    bot_data = bot_controle['iniciado_em']
    bot_user_login = bot_controle['user_login']
    
    # Busca os registros referentes ao bot_id e cria o DataFrame
    df_dados = pd.DataFrame(
        TblBbBotRegistros1Sentenca.all().where("bot_controle_id", bot_id).toDict()
    )
    
    df_dados['solocitado_por'] = bot_user_login
    
    # Remoção de colunas extras (adicione outras colunas se necessário)
    colunas_para_remover = ['id', 'bot_controle_id', 'created_at', 'updated_at']
    df_dados = df_dados.drop(columns=colunas_para_remover, errors='ignore')
    
    # Converter os títulos das colunas para maiúsculas
    df_dados.columns = [col.upper() for col in df_dados.columns]
    
    excel_io = gerar_planilha_excel(df_dados)
    nome_arquivo = gerar_nome_arquivo(bot_data)
    headers = {'Content-Disposition': f'attachment; filename="{nome_arquivo}"'}
    
    return StreamingResponse(
        excel_io,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )



