# #!/usr/bin/env python
# # coding: utf-8

import lxml
import locale
import xlsxwriter
import requests
import base64
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import psycopg2
import psycopg2.extras as extras
import datetime
import logging
import sys
import os
from time import sleep
from datetime import date, timedelta, timezone
from pytz import timezone
from typing import Any
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from sqlalchemy import create_engine
import sqlalchemy.types as sqltypes
from sqlalchemy.exc import SQLAlchemyError
import glob
import skimpy
from skimpy import clean_columns



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from anticaptchaofficial.recaptchav2proxyless import *
# from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.select import Select

# sys.path.append('../')
import usuario as user
import Emails

import fasteners



class FuncoesBB:
    
    def __init__(self, browser = None, robo = 'painel'):
        self.browser = browser
        self.robo = robo
        
#         self._login = user._login
#         self._senha = user._senha

        # Garantir que a pasta 'temp' exista
        self.temp_dir = "temp"
        os.makedirs(self.temp_dir, exist_ok=True)

         # Caminho do arquivo de estado
        self.status_file = os.path.join(self.temp_dir, self.robo.replace(" ", "_") + ".json")
        
        # Trava para não executar simultaneamente
        self.lock_file = os.path.join(self.temp_dir, self.robo.replace(" ", "_") + ".lock")
        self.lock = fasteners.InterProcessLock(self.lock_file)



        
        # # Caminho do arquivo de estado
        # self.status_file = "temp/"+robo.replace(" ", "_")+".json"
        
        # # Trava para não executar simultaneamente
        # self.lock_file = "temp/"+robo.replace(" ", "_")+".lock"
        # self.lock = fasteners.InterProcessLock(self.lock_file)
               
        
        
        fuso_horario = timezone('America/Recife')
        
        # Unidades
        self.civel_key = '6da94d19-f607-11ea-'
        self.trabalhista_key = '6da951c3-f607-11ea-'
        
        
        # if user.v_local == 'dev':
        if user.autojurProd == False:
            self.url = 'https://homologacao/rest/importador/informacao' # HOMOLOGAÇÃO
            self.url_ged =  'https://homologacao/rest/ged'  # GED HOMOLOGAÇÃO
            self.ChaveApi = '732c1cd8-f53d-11e9' 
            self.ChaviApi_Trabalhista = '732c1cd8-f53d-11e9'
            self.v_closeBrowser = False
            
        elif user.autojurProd == True:
            self.url = 'https://producao/rest/importador/informacao' # PRODUÇÃO
            self.url_ged = 'https://producao/rest/ged' # GED PRODUÇÃO
            self.ChaveApi = '732bb159-f53d-11e9'
            self.ChaviApi_Trabalhista = '732b8b72-f53d-11e9'
            self.v_closeBrowser = True


        if user.dbprod: # PRODUÇÃO
            self.user="postgres"
            self.password="nem_a_pau" 
            self.host="192.168.1.26"
            self.port="5433"
            self.database="nem_a_pau"
        else:  # HOMOLOGAÇÃO
            self.user="postgres"
            self.password="nem_a_pau" 
            self.host="192.168.1.21"
            self.port="54320"
            self.database="nem_a_pau"
            
            
        # PEGAR O USUÁRIO NO BANCO DE DADOS
        _connection = self.connUsers()
        _cursor = _connection.cursor()
        _sql = "select usuario, senha from  bancos.tbl_notificacoes_usuarios where status = true;"

         # Passe os valores como uma tupla para o método execute
        _cursor.execute(_sql)

        dados = _cursor.fetchone() #fetchall()

        _cursor.close()
        _connection.close()

        self._login = dados[0]
        self._senha = dados[1]

        print(f"USUARIO: {self._login} ")

        # ChaveApi = '732c6311-f53d-11e9' #'CARLA JANE'
        # ChaveApi = '9bbf98f9-3a3c-11eb-9de7-000c29d92768' #'TON MARCELINO'
    

    # #CONEXAO COM BANCO DE DADOS PGSQL 
    def connUsers(self):
        global v_local
        
        try:
            connection = psycopg2.connect(user="postgres",
                                      password="nem_a_pau" ,
                                      host="192.168.1.26",
                                      port="5433",
                                      database="nem_a_pau",
                                      application_name=self.robo)

            return connection
        except Exception as e1:
            _logging(msg='[conn] Erro ao Se conectar ao Banco de usuários : {}'.format(e1.args))
            self.GravarLogs('[conn] Erro ao Se conectar ao Banco de usuários: {}'.format(e1.args))
            exit(0)
    
    
    # #CONEXAO COM BANCO DE DADOS PGSQL 
    def conn(self):
        global v_local
        
        try:
            connection = psycopg2.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      database=self.database,
                                      application_name=self.robo)

            return connection
        except Exception as e1:
            _logging(msg='[conn] Erro ao Se conectar ao Banco : {}'.format(e1.args))
            self.GravarLogs('[conn] Erro ao Se conectar ao Banco : {}'.format(e1.args))
            exit(0)

            
            
            
    def Horario(self):
        fuso_horario = timezone('America/Fortaleza')
        return str(datetime.now().astimezone(fuso_horario))
    
    
    
    def MensagemErro(self,erro):
        global v_closeBrowser
        if self.v_closeBrowser:
    #         send_message(token, chat_id, msg)
            self.browser.close()
        
        print(str(self.Horario()))
        self.GravarLogs(erro)
        self.GravarLogs('*** SISTEMA ABORTADO! ***')
        
        Emails.Enviar(robo=self.robo, descricao=erro, destinatario='monitoria@nem_a_pau.com')
        
        if (self.robo == 'acompanhamento prazos'):
            # salvar flag informando erro
                # """Salva o status atual da execução."""
                status_file = "/app/temp/execution_status.json"
                with open(status_file, "w") as f:
                    json.dump({"error": True}, f)
                    
        self.lock.release()           
        sys.exit()




    def GravarLogs(self,mensagem):
        global tipo_texto, subtipo, classificacao
#         if rastreio:
#             mensagem = mensagem + '|'+tipo_texto+'|'+subtipo+'|'+classificacao

        _connection = self.conn()
        _cursor = _connection.cursor()
        _sql = """INSERT INTO bancos.tbl_logs (robo,mensagem) VALUES ('{}', '{}') """.format(self.robo, mensagem)

        #print(_sql)
        _cursor.execute(_sql)
        _connection.commit()
        _connection.close()
        print(mensagem)

    

    # TELA DE CAPTCHA
    def ResolveCaptcha(self,vloop=1):
        
        limite_do_loop = 5

        if vloop > limite_do_loop:
            self.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
            self.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - task finished with error")
            return
            
        print(f"[ResolveCaptcha] Tentativa {vloop} ")


        try:
            element = WebDriverWait(self.browser, 60).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/form/fieldset/div[1]')))

            sleep(2)
            chave_captcha = self.browser.find_element(By.XPATH, '//*[@id="content"]/div/form/fieldset/div[1]').get_attribute('data-sitekey')
            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key("543f7294cd38f0e295a04eff9f9ce790")
            solver.set_website_url("https://nem_a_pau.com/login")
            solver.set_website_key(chave_captcha)
            # solver.set_page_action("home_page")
            solver.set_soft_id(0)


            g_response = solver.solve_and_return_solution()

            if g_response != 0:
                print ("g-response: " + g_response)
                try:
                    element = WebDriverWait(self.browser, 30).until(
                        EC.presence_of_element_located((By.ID, "g-recaptcha-response")))
                
                    self.browser.execute_script(f"document.getElementById('g-recaptcha-response').innerHTML='{g_response}'") 

                    self.browser.execute_script("document.querySelector(\'input[type=submit]\').click()") 
                except TimeoutException:
                    self.GravarLogs("*** [ResolveCaptcha] Não Conseguiu Clicar no botão de logar ***",g_response)
                    self.ResolveCaptcha(vloop+1)

            else:
                print ("task finished with error "+solver.error_code)
    #             print("*** [ResolveCaptcha] Não Conseguiu resolver o CAPTCHA ***")
                if vloop > limite_do_loop:
                    self.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                    self.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - task finished with error")
                    return
                self.ResolveCaptcha(vloop+1)

        except TimeoutException:
    #         print("[ResolveCaptcha] Não Carregou o CAPTCHA")
            self.GravarLogs("[ResolveCaptcha] Não Carregou o CAPTCHA")
            if vloop > 5:
    #             print('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                self.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                self.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - Não consegui resolver o ReCaptcha")
                return

            self.ResolveCaptcha(vloop+1)
            
        # Verifica se o usuário não está autorizado
        try:
            element = WebDriverWait(self.browser, 5).until(
                    EC.visibility_of_element_located((By.XPATH,'//span[contains(text(),"Authentication Failed")]')))
            print('**** USUÁRIO NÃO AUTORIZADO !!!!!!! ****')
        except TimeoutException:
            pass
        


    # CARREGAR CAMPO LOGIN
    def Login(self):
        #global browser, WebDriverWait

        try:
            element = WebDriverWait(self.browser, 60).until(
                EC.visibility_of_element_located((By.ID, "idToken1")))

            self.browser.find_element(By.XPATH,'//*[@id="idToken1"]').send_keys(self._login)
            self.browser.find_element(By.XPATH,'//*[@id="loginButton_0"]').click()

        except TimeoutException:
            self.MensagemErro("*** ERRO: [Login] Não abriu tela de LOGIN")




    # ENTRAR COM SENHA DO USUÁRIO
    def Senha(self):
        try:
#             print("USUARIO:",self._login)
#             print("SENHA:",self._senha)
            element = WebDriverWait(self.browser, 60).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="idToken3"]')))
            sleep(2)
            self.browser.find_element(By.XPATH,'//*[@id="idToken3"]').send_keys(self._senha)
            self.browser.find_element(By.XPATH,'//*[@id="loginButton_0"]').click()
        except TimeoutException:
            self.MensagemErro("*** ERRO: [EntrarComSenha] Não Carregou o Campo de senha")


        
        
    # checar se div carregando está presente
    def Carregando(self):
        try:
            element = WebDriverWait(self.browser, 60).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loader.is-loading")))
        except TimeoutException:
            print("[Carregando] Mais de 600 segundos esperando desaparecer a tela 'Carregando'")
            return
        
        
    def Mostrar(self, df):
        # if user.v_local == 'dev':
        #     display(df)
        # else:
        #     print(df)
            
        print(df)
        
        
        
    def load_status(self):
        """Carrega o status da última execução."""
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r") as f:
                    content = f.read().strip()  # Remove espaços ou linhas vazias
                    if content:  # Verifica se o arquivo não está vazio
                        return json.loads(content)
            except json.JSONDecodeError:
                print(self.Horario(),"Arquivo de status corrompido. Redefinindo o status.")
        # Retorna um estado padrão caso o arquivo esteja vazio ou inválido
        return {"error": False}

    def save_status(self, error_occurred):
        """Salva o status atual da execução."""
        with open(self.status_file, "w") as f:
            json.dump({"error": error_occurred}, f)
            
            
    def AguardarTelaCarregandoDesaparecer(self):
        """Aguarda a tela de carregamento desaparecer."""
        # Selecionar o elemento da div que queremos monitorar
        loading_selector = 'body > plt-template-base > div > plt-carregando > div > div > span'

        # Variável para controlar a visibilidade
        is_visible = True
        # Contador de tentativas
        attempt_counter = 0
        max_attempts = 60

        # Loop para esperar até que o elemento fique invisível
        while is_visible and attempt_counter < max_attempts:
            print("\t[AguardarTelaCarregandoDesaparecer] Aguardando tela CARREGANDO desparecer, tentativa", attempt_counter + 1)
            try:
                # Verificar se o elemento está visível
                is_visible = WebDriverWait(self.browser, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, loading_selector)))
                # Se estiver visível, esperar um pouco antes de verificar novamente
                time.sleep(1)
            except:
                # Se uma exceção for levantada, o elemento não está visível
                is_visible = False
            
            # Incrementar o contador de tentativas
            attempt_counter += 1
        
        if attempt_counter >= max_attempts:
            print("O elemento ainda está visível após 60 tentativas.")