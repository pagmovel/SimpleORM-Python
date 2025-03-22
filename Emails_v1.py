#!/usr/bin/env python
# coding: utf-8

# In[13]:


# import locale
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import warnings
from datetime import datetime, timezone, timedelta

# Definindo variáveis de ambiente para suprimir warnings
os.environ['SQLALCHEMY_WARN_20'] = '0'
os.environ['SQLALCHEMY_SILENCE_UBER_WARNING'] = '1'

# Suprimindo warnings específicos do SQLAlchemy
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sqlalchemy")

# locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')

# HOMOLOGAÇÃO
# engine = create_engine('postgresql://postgres:4Ut0juR!@192.168.12.21:54320/smart')
# PRODUÇÃO
engine = create_engine('postgresql://rms_nit:^zDGqGKLoOpayitW@192.168.12.26:5433/smart')

fuso_horario = timezone(timedelta(hours=-3))

# v_local = 'dev'


# In[16]:


def Enviar(robo = '', descricao = '', destinatario = 'nit@rms.adv.br', v_local = 'prod'):
    try:
        servidor_email = smtplib.SMTP('smtp.office365.com', 587)
        servidor_email.starttls()
        servidor_email.login('centralnit@rms.adv.br', 'jkla@2210')
        
        remetente = 'centralnit@rms.adv.br'
        
        if v_local == 'dev':
            destinatario = 'marcossilva@rms.adv.br'
        else:
            destinatario = destinatario
            
        # Endereço para cópia do email
        destinatario_cc = 'nit@rms.adv.br'
            
        hoje = datetime.now().strftime('%d/%m/%Y')
        assunto = f'[ERRO] {robo.upper()} - {hoje}'

        # Texto personalizado a ser adicionado antes da tabela
        texto_personalizado = f"""
        <p>Prezados,</p>
        <p>O robô {robo.upper()} apresentou um erro.</p>
        <p>Favor verificar!</p>
        <p><br></p>"""
        
        if len(descricao)>0:
            texto_personalizado = texto_personalizado + f"""
            <p>DESCRIÇÃO DO ERRO:</p>
            <p>------------------</p>
            <p>{descricao}</p>
        """
        
        # Aplicando formatação de tabela
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
        
        corpo_email = estilo + texto_personalizado #+ df.to_html(index=False)

        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
#         if v_local != 'dev':
#             msg['Cc'] = destinatario_cc
        msg['Subject'] = assunto

        msg.attach(MIMEText(corpo_email, 'html'))

        # Combina os destinatários e os destinatários de cópia
        destinatarios = [destinatario] + [destinatario_cc]

        servidor_email.sendmail(remetente, destinatarios, msg.as_string())
        
        servidor_email.quit()
        
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False


# In[17]:


# Enviar('painel notificações', destinatario="marcossilva@rms.adv.br")


# In[ ]:




