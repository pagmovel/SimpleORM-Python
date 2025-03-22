#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from io import BytesIO
# import os
import warnings
from datetime import datetime, timezone, timedelta
import json
import sys
import traceback

# Suprime warnings desnecessários
warnings.filterwarnings("ignore")

# Evita erro em ambientes que não suportam reconfigure()
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

fuso_horario = timezone(timedelta(hours=-3))

# Carrega configurações do arquivo JSON
with open("config.json", "r") as config_file:
    CONFIG = json.load(config_file)

EMAIL_CONFIG = CONFIG["email"]


# In [ ]
def Enviar(robo='ROBÔ GERENCIADOR DE USUÁRIOS', mensagem='', df=None, 
           destinatario='nit@rms.adv.br', destinatario_cc='nit@rms.adv.br', tipo=True, anexo= False):
    # Verifica se df é um DataFrame; se não for, retorna None
    if not isinstance(df, pd.DataFrame) or df.empty:
        return None

    
    try:
        # Verifica se as configurações de email estão completas
        if not all(key in EMAIL_CONFIG and EMAIL_CONFIG[key] for key in ['host', 'port', 'user', 'password']):
            raise ValueError("Configurações de email incompletas em EMAIL_CONFIG.")
        
        servidor_email = smtplib.SMTP(EMAIL_CONFIG['host'], EMAIL_CONFIG['port'])
        servidor_email.starttls()
        servidor_email.login(EMAIL_CONFIG['user'], EMAIL_CONFIG['password'])
        
        remetente = EMAIL_CONFIG['user']
        hoje = datetime.now().strftime('%d/%m/%Y')
        
        if tipo:
            txt_assunto = 'USUÁRIOS EXECUTADOS COM SUCESSO'
        else:
            txt_assunto = 'EXECUÇÕES DE USUÁRIOS QUE FALHARAM'
            
        assunto = f'[{robo.upper()}] - {hoje} - {txt_assunto}'
        
        # Valida se os cabeçalhos essenciais são strings não vazias
        if not remetente:
            raise ValueError("O remetente está indefinido.")
        if not destinatario:
            raise ValueError("O destinatario está indefinido.")
        if not assunto:
            raise ValueError("O assunto está indefinido.")
        
        # Monta o texto personalizado do email
        texto_personalizado = f"""
        <p>Prezados,</p>
        <p>{mensagem}</p>
        <p><br></p>
        """
       
        
        # Define o estilo da tabela
        estilo = """
        <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """
        
        if not anexo:
            # Converte o DataFrame para HTML
            corpo_email = estilo + texto_personalizado + df.to_html(index=False)
        else:
            corpo_email = estilo + texto_personalizado
        
        # Configura a mensagem de email
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        # Define o cabeçalho Cc somente se destinatario_cc não for None
        if destinatario_cc is not None:
            msg['Cc'] = destinatario_cc
        msg['Subject'] = assunto
        
        msg.attach(MIMEText(corpo_email, 'html'))
        
        # Se o parâmetro "anexo" for True, gera a planilha Excel a partir do DataFrame e anexa ao email.
        if anexo:         
            
            # Gera o nome do arquivo com o conteúdo de "robo" e a data/hora atual
            agora = datetime.now(fuso_horario)
            nome_arquivo = f"{robo.replace(' ', '_')}_{agora.strftime('%d-%m-%Y_%H%M%S')}.xlsx"
            
            # Cria um stream em memória para salvar a planilha
            excel_stream = BytesIO()
            df.to_excel(excel_stream, index=False)
            excel_stream.seek(0)  # Retorna para o início do stream
            
            # Cria o anexo com o conteúdo da planilha
            attachment = MIMEApplication(excel_stream.read(), _subtype="xlsx")
            attachment.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)
            msg.attach(attachment)
            
            
        # Filtra os destinatários para remover None
        destinatarios = [d for d in [destinatario, destinatario_cc] if d is not None]
        
        servidor_email.sendmail(remetente, destinatarios, msg.as_string())
        servidor_email.quit()
        
        return True
    except Exception as e:
        import traceback
        print(f"Erro ao enviar email: {e}")
        print("Erro completo:")
        print(traceback.format_exc())
        return False



