# app.py
# from models.usuario import Usuario
from sqlalchemy import text
from models.tbl_bb_bots_controle import TblBbBotsControle
from models.tbl_bb_bot_registros_primeira_sentenca import TblBbBotRegistros1Sentenca
from models.tbl_bb_bots_controle_logs import TblBbBotsControleLogs
from models.tarefas_table import TarefasTable

from datetime import datetime

import sys
sys.path.append('../')
sys.path.append('../../')
import usuario as user
from funcoesbb import FuncoesBB
from Emails import Enviar
from funcoes_nit import Nit


import pandas as pd
import psycopg2
import re
from time import sleep
from anticaptchaofficial.recaptchav2proxyless import *

from selenium.webdriver.common.by import By

from datetime import datetime, timedelta, timezone
# Define o fuso horário -3 (em horas)
tz_minus3 = timezone(timedelta(hours=-3))




   
def consulta_autojur(bot_id): 
    
    sql = text("""
                SELECT DISTINCT(a.pasta_id), a.id as cod_tarefa, b.localizador, a.evento as nome_evento, a.tag_controle as tag_tarefa, b.tag_controle as tag_pasta
                FROM autokit.tarefas_table AS a
                INNER JOIN autokit.pastas_table AS b ON (b.pasta_id = a.pasta_id)
                WHERE a.evento = 'REGISTRAR PRIMEIRA SENTENCA'
                AND a.situacao IN ('AGUARDANDO','EM ANDAMENTO','NOVA');
                """)

    resultados = TarefasTable.rawSql(sql, db_key='autokit')

    registros = []
    for index, row in enumerate(resultados):
        # Supondo que row seja uma tupla e que o valor de npj seja o segundo item (row[1])
        d = {
            "bot_controle_id": bot_id,  # bot_id deve estar definido, por exemplo, bot_id = bot_controle['id']
            "pasta_id": row[0],  #
            "cod_tarefa": row[1], 
            "npj": row[2], 
            "nome_evento": row[3], 
            "tag_tarefa": row[4], 
            "tag_pasta": row[5]
        }
        registros.append(d)
        
    if len(registros) == 0:
        print("1-Nenhum registro encontrado no AUTOKIT")
        return None
    else:
        # insere os registros no banco de dados
        dados = TblBbBotRegistros1Sentenca.create(registros)
        

        print(len(dados),"> Registros de tarefas inseridos no robô com sucesso")
        return dados
        

def getUsers() ->  tuple:
    # PEGAR O USUÁRIO NO BANCO DE DADOS
    _connection = bb.connUsers()
    _cursor = _connection.cursor()
    _sql = "select usuario, senha from  bancos.tbl_dmi_painel_notificacoes_usuarios where status = true;"

        # Passe os valores como uma tupla para o método execute
    _cursor.execute(_sql)

    dados = _cursor.fetchone() #fetchall()

    _cursor.close()
    _connection.close()

    _login = dados[0]
    _senha = dados[1]

    return (_login, _senha)


def Autenticacao(first = True,loop = 0) ->  None:
    if first:
        try:
            client.getElement(xpath ='//*[@id="j_id33"]/section/div[2]/p')
            return
        except BaseException as e:
            if loop > 2:
                bb.MensagemErro(bb.Horario()+" Não conseguiu Autenticar!")
                return

            print("\n************************************")
            print(f"Tentanto pela {loop+1}ª vez.")
            print("************************************\n")

            notAutenticated()
    else:
        notAutenticated()
        
        

def notAutenticated():
    try:
        # bb.GravarLogs('- Acessando o sistema do banco')
        # client.getUrl('https://juridico.bb.com.br/paj/juridico/v2?app=processoConsultaApp')
        print('- Fazendo login')
        bb.Login()
        print('- Resolvendo reCaptcha!')
        bb.ResolveCaptcha()
        print('- Entrando com a senha do usuário')
        #EntrarComSenha()
        sleep(1)
        bb.Senha()

        # if(loop == 0):
        #     client.getUrl(urlPainel)
    except BaseException as e:
        Autenticacao(False,loop+1)
        
        
def ExibirErro(mensagem = None, sair = False) ->  None:
    """Exibe a mensagem de erro.
       Params: mensagem, String, sair Boolean
       
       Quando 'sair' receber True, o sistema finaliza a execução."""
       
    print(">>> ERRO!", mensagem)
    
    if sair:
        quit()




def ResolveCaptcha(vloop=1):
        
        limite_do_loop = 5

        if vloop > limite_do_loop:
            bb.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
            bb.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - task finished with error")
            return


        try:
            # captcha = client.getElement(xpath = '//*[@id="content"]/div/form/fieldset/div[1]')
            # element = WebDriverWait(self.browser, 60).until(
            # EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/form/fieldset/div[1]')))

            # sleep(2)
            chave_captcha_element = client.getElement(xpath = '//*[@id="content"]/div/form/fieldset/div[1]')
            chave_captcha = chave_captcha_element.get_attribute('data-sitekey')
            
            print("ChaveCaptcha", chave_captcha)
        except BaseException as e:
            bb.GravarLogs('[ResolveCaptcha] Não consegui localizar o capthca')
            bb.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - task finished with error")
            return
            
            
        try:
            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key("543f7294cd38f0e295a04eff9f9ce790")
#             solver.set_website_url("https://loginweb.bb.com.br/sso/XUI/?realm=paj#login&goto=https%3A%2F%2Fjuridico.bb.com.br%2Fpaj%2Fjuridico%2Fv2%3Fapp%3DprocessoConsultaApp")
#             solver.set_website_url("https://loginweb.bb.com.br/sso/XUI/?realm=/paj&goto=https://juridico.bb.com.br/paj/juridico/v2?app%3DprocessoConsultaApp#login")
            solver.set_website_url("https://juridico.bb.com.br/paj/juridico/v2?app=processoConsultaApp")
            solver.set_website_key(chave_captcha)
            # solver.set_page_action("home_page")
            solver.set_soft_id(0)


            g_response = solver.solve_and_return_solution()

            if g_response != 0:
                print ("g-response: " + g_response)
                try:
                    
                    # Injetar a resposta do reCAPTCHA diretamente no campo hidden correto
                    client.browser.execute_script(
                        "document.getElementById('g-recaptcha-response').value = arguments[0];", g_response
                    )

                    # Confirmar que a resposta foi inserida corretamente
                    g_response_check = client.browser.execute_script(
                        "return document.getElementById('g-recaptcha-response').value;"
                    )
                    print("ReCaptcha Response Injetado:", g_response_check)

                    # Aguarde um curto período para garantir que a injeção foi reconhecida
                    sleep(2)

                    # Simular o clique no botão de login via JavaScript para forçar o envio
                    client.browser.execute_script("document.querySelector('input[type=submit]').click();")

                except BaseException as e:
                    bb.GravarLogs("*** [ResolveCaptcha] Não Conseguiu Clicar no botão de logar ***",g_response)
                    bb.ResolveCaptcha(vloop+1)

            else:
                print ("task finished with error "+solver.error_code)
    #             print("*** [ResolveCaptcha] Não Conseguiu resolver o CAPTCHA ***")
                if vloop > limite_do_loop:
                    bb.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                    bb.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - task finished with error")
                    return
                
                ResolveCaptcha(vloop+1)

        except BaseException as e:
    #         print("[ResolveCaptcha] Não Carregou o CAPTCHA")
            bb.GravarLogs("[ResolveCaptcha] Não Carregou o CAPTCHA")
            if vloop > 5:
    #             print('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                bb.GravarLogs('[ResolveCaptcha] Não consegui resolver o ReCaptcha')
                bb.MensagemErro(f"[ResolveCaptcha] Tentativa {vloop} - Não consegui resolver o ReCaptcha")
                return

            ResolveCaptcha(vloop+1)
        
    
def Login(_login =  None):
    try:
        print("[Login] Localizando campo Login")
        login = client.getElement(xpath = "idToken1", tipo='ID')
        if login:
            login.clear()
            login.send_keys(_login)
            client.getElement(xpath = '//*[@id="loginButton_0"]', click=True)
    except BaseException as e:
        print(f"[Login] Não encontrei o campo do código do usuário")
        # bb.MensagemErro(f"[Autenticacao] Tentativa {vloop} - task finished with error")
        return

def Senha(_senha = None):   
    try:
        print("[Senha] Localizando campo Senha.")
        senha = client.getElement(xpath = '//*[@id="idToken3"]')
        if senha:
            senha.clear()
            senha.send_keys(_senha)
            sleep(1)
            client.getElement(xpath='//*[@id="loginButton_0"]', click = True)
    except BaseException as e:
        bb.MensagemErro(f"[Senha] Não encontrei co campo da senha")
        return
    

def carregar_dados(bot_id):
    # Carrega os dados relacionados ao robô da tabela TblBbBotRegistros1Sentenca
    try:
        print("-> Carrega os dados relacionados ao robô da tabela TblBbBotRegistros1Sentenca")
        dados = TblBbBotRegistros1Sentenca.all().where('bot_controle_id', bot_id).emptyOrNull('updated_at').toDict()
        
        # se não tiver dados, procure no Autokit
        if len(dados) == 0:
            print("-> Nenhum registro encontrado")
            print("-> Vamos gerar novamente os dados consultando no banco do Autojur")
            
            dados = consulta_autojur(bot_id)
            
            # Se retornar vazio, sair do robô
            if dados is None:
                # atualizar a tabela de controle
                update_controle = {
                    'apresentou_erro': True,
                    'robo_ativo': False
                }
                if not TblBbBotsControle.findById(bot_id).update(data = update_controle):
                    print("--> Erro ao atualizar controle")
                    
                # inserir log da atividade na tabela
                if not TblBbBotsControleLogs.create([{
                                                'bb_bots_controle_id': bot_id, 
                                                'descricao': 'Erro ao consultar no Autojur',
                                                'user_login': bot_user_login
                                                }]):
                    print("--> Erro ao inserir log")
                    
                exit("--> EXECUÇÃO ENCERRADA COM ERRO")
                
        # retorna os dados
        return dados
    except BaseException as e:
        print("Erro ao carregar dados")
        print(e)
        
        # Atualiza a tabela de controle
        update_controle = {
                'robo_ativo': False,
                'apresentou_erro': True
        }
        if not TblBbBotsControle.findById(bot_id).update(update_controle):
            print("--> Erro ao atualizar controle")
        
        # inserir log da atividade na tabela
        if TblBbBotsControleLogs.create({
                                        'bb_bots_controle_id': bot_id, 
                                        'descricao': str(e),
                                        'user_login': bot_user_login
                                        }):
            print("--> Erro ao inserir log")
        
        exit("--> EXECUÇÃO ENCERRADA COM ERRO")





if __name__ == "__main__":
    
    
    # Pega o bot mais antigo que não está ativo e não foi encerrado
    bot_controle = TblBbBotsControle.all() \
                                    .emptyOrNull('encerrado_em') \
                                    .isFalse('robo_ativo') \
                                    .isTrue('iniciar') \
                                    .orderBy('id', 'asc') \
                                    .firstToDict()


    # Se não encontrou nenhum bot
    if bot_controle is None:
        print("Nenhum robô ativo encontrado")
        exit() # finaliza o script
        
    
    # Definindo o navegador padrão como 'chrome'
    v_browser = 'chrome'
    show_browser = True
    nome_robo = 'Registro de 1ª sentença'
    num_robo = 1
    urlPainel = 'https://juridico.bb.com.br/paj/app/paj-central-notificacoes/spas/central-notificacoes/central-notificacoes.app.html'


        
    bot_id = bot_controle['id']  
    bot_user_login = bot_controle['user_login']
    dados_autokit = []
        
    try:
        print("Bot encontrado:",bot_id,'-', bot_controle["nome_bot"], "| Usuário:",bot_user_login)


        if bot_controle['iniciar'] is True:
            
            try:
                
                # atualizar a tabela de controle
                update_controle = {
                    'robo_ativo': True,
                    'apresentou_erro': False
                }
                
                if bot_controle['iniciado_em'] is None:
                    update_controle['iniciado_em'] = datetime.now()
                if not TblBbBotsControle.findById(bot_id).update(update_controle):
                    print("--> Erro ao atualizar controle", update_controle)
                    
                    
                # Se o bot apresentou erro durante a execução anterior, carrega os registros que ainda faltam capturar
                if bot_controle['apresentou_erro'] is True:
                    print("Erro encontrado antyeriormente no bot, tentando novamente")

                # # Carrega os dados relacionados ao robô da tabela TblBbBotRegistros1Sentenca
                dados = carregar_dados(bot_id)
                
                # print("Carrega os dados relacionados ao robô da tabela TblBbBotRegistros1Sentenca")
                # dados = TblBbBotRegistros1Sentenca.all().where('bot_controle_id', bot_controle['id']).emptyOrNull('updated_at').toDict()
            
            except BaseException as e:
                print("Erro ao carregar dados")
                print(e)
                
                # Atualiza a tabela de controle
                update_controle = {
                        'robo_ativo': False,
                        'apresentou_erro': True
                    
                }
                if not TblBbBotsControle.findById(bot_id).update(update_controle):
                    print("--> Erro ao atualizar controle",update_controle)
                
                # inserir log da atividade na tabela
                create_log = {
                            'bb_bots_controle_id': bot_id, 
                            'descricao': str(e),
                            'user_login': bot_user_login
                            }
                if TblBbBotsControleLogs.create(create_log):
                    print("--> Erro ao inserir log",create_log)
                    
                exit("--> EXECUÇÃO ENCERRADA COM ERRO")



            # Instancia a classe Nit no objeto nit
            client = Nit(robo=nome_robo, show_browser=show_browser,v_browser="chrome", port=9520)
            sleep(2)
            bb = FuncoesBB(browser = client, robo = nome_robo)
            
            
            # Autenticação
            try:
                _login, _senha = getUsers()
                
                # Abre o navegador
                client.openBrowser()
                client.getUrl(urlPainel)
                
                # Autenticar(_login, _senha)
                Login(_login)
                    
                ResolveCaptcha()

                sleep(5)

                Senha(_senha) 
                    
                client.getUrl("https://juridico.bb.com.br/paj/juridico/v2?app=centralNotificacoesApp")
            except BaseException as e:
                print(e)
                exit("Erro na Autenticação:",e)


            # try:
            #     dados
            # except NameError:
            #     dados = carregar_dados(bot_id)
            total_dados = len(dados)
            print("TOTAL DE REGISTROS:",total_dados)
            # Procurar pelo NPJ e capturar os dados
            for index, row in enumerate(dados):
                client.MudaFocoParaPrincipal()
                # aguarda a tela de carregamento desaparecer
                # print('*** teste ***')
                bb.AguardarTelaCarregandoDesaparecer()
                # print('*** teste 2 ***')
                print(row)
                dados_capturados = []

                input_npj = client.getElement(xpath = '//*[@id="anoProcesso"]')

                dados_atualisar = []
                if input_npj:
                    input_npj.clear()
                    # npj = '2025/0058147-000'
                    _id = row['id']
                    npj = row['npj']
                    print("-" * 80)
                    print(f"> [{total_dados-index}] >> NPJ: {npj} ")
                    print("-" * 80)
                    # sleep(2)
                    input_npj.send_keys(npj)
                    # sleep(1)
                    
                    
                    
                    btn_buscar = client.getElement(xpath='//*[@id="buscar"]')
                    if btn_buscar:
                        btn_buscar.click()
                    else:
                        ExibirErro("ERRO! Não consegui encontrar o butão BUSCAR para clicar")
                        
                        
                        
                    #  aguarda a tela de carregamento desaparecer
                    bb.AguardarTelaCarregandoDesaparecer()        
                    
                    
                    client.MudaFocoParaIframe()
                    # clicar na ação Detalhes
                    btn_detalhes = client.getElementJavascript(tipo="XPATH",xpath = '//*[@id="processo-consulta-page"]/body/plt-template-base/div/ng-transclude/ng-view/div/div/div/section/article/div/div/div/div/div[1]/ng-include/div[1]/div/div/table/tbody/tr/td[7]/span/i', click = True)
                    if btn_detalhes is False:
                        ExibirErro("Não consegui encontrar o icone de DETALHES para clicar")
                    
                    client.MudaFocoParaPrincipal()            
                    #  aguarda a tela de carregamento desaparecer
                    bb.AguardarTelaCarregandoDesaparecer()
                    
                    sleep(.5)
                    
                    client.MudaFocoParaIframe()
                    
                    sleep(.5)
                    # Captura todos os elementos <classificacao-processo-detail> usando XPath
                    classificacao_processo = client.browser.find_elements(By.XPATH, "//classificacao-processo-detail")
                    print(f"Foram encontrados {len(classificacao_processo)} elementos.")

                    # Itera sobre cada elemento para acessar a tabela interna
                    for elemento in classificacao_processo:
                        try:
                            # Localiza a tabela dentro do elemento
                            tabela = elemento.find_element(By.XPATH, ".//table")
                            
                            try:
                                # Localiza a célula da linha onde a primeira célula (td[1]) tem o texto "CADASTRO"
                                # e captura o conteúdo da segunda célula (td[2])
                                celula_cadastro = tabela.find_element(
                                    By.XPATH, ".//tr[td[1][normalize-space()='CADASTRO']]/td[2]"
                                )
                                
                                cadastro = celula_cadastro.text
                                # Verifica se o texto está vazio
                                if not cadastro:
                                    cadastro = 'SEM INFORMAÇÃO EM ' + datetime.now(tz_minus3).strftime('%d/%m/%Y %H:%M:%S')
                            except BaseException as e:
                                cadastro = 'SEM INFORMAÇÃO EM ' + datetime.now(tz_minus3).strftime('%d/%m/%Y %H:%M:%S')

                            
                            menui_analise_risco = client.getElementByText(text="Análise de Risco", attribute="li")
                            menui_analise_risco.click()
                            
                            client.MudaFocoParaPrincipal()            
                            #  aguarda a tela de carregamento desaparecer
                            bb.AguardarTelaCarregandoDesaparecer()
                            client.MudaFocoParaIframe()
                            
                            # capturar as TAGs de nalise de riscos se houverem
                            try:
                                # Encontra todos os elementos com a classe 'alert--warn'
                                elementos = client.browser.find_elements(By.CLASS_NAME, "alert--warn")
                                # Extrai o texto de cada elemento
                                textos = [elemento.text for elemento in elementos]
                                
                                # Remove a substring 'Mensagem de alerta.\n' de cada texto
                                textos_sem_alerta = [texto.replace("Mensagem de alerta.\n", "") for texto in textos]
                                
                                # Junta os textos com o separador ';'
                                tags_analise_riscos = '; '.join(textos_sem_alerta)
                                
                                print(tags_analise_riscos)
                            except BaseException as e:
                                print("Não tem tags de analises de riscos", e)
                                tags_analise_riscos = None
                            
                            print('-' *20)
                            print("ID:", _id)
                            print("CADASTRO:", cadastro)
                            print("TAGS_ANALISE_RISCOS:", tags_analise_riscos)
                            
                            
                            # Salvar no banco de dados
                            try:
                                # Salvar no banco de dados
                                data_update = {
                                    "cadastro":cadastro,
                                    "tags_analise_riscos":tags_analise_riscos,
                                    "updated_at":datetime.now()
                                }
                                result = TblBbBotRegistros1Sentenca.findById(_id).update(data = data_update)
                                print("Dados atualizados com sucesso!", data_update)         
                                
                            except BaseException as e:
                                print("Erro ao atualizar a captura do NPJ/ID:",npj,"/",_id, e)
                                
                            print('-' *20)
                            
                        except BaseException as e:
                            print("Não foi possível localizar a linha com 'CADASTRO':", e)
                    
            # Marca o registro do robô como finalizado
            data_update = {
                "robo_ativo": False,
                "encerrado_em": datetime.now(),
                "apresentou_erro": False,
                "iniciar": False,
                "updated_at": datetime.now()
            }
            if not TblBbBotsControle.findById(bot_id).update(data = data_update):
                print("Erro ao atualizar controle:",data_update)
            else:
                print("Robô finalizado com sucesso!")
                print("Enviando e-mail para:")
        
                mensagem = """Prezado!<br>
                Segue planilha processada pelo robô de captura de dados de processos de 1ª instância."""
                
                # pegar dados completos no banco de dados
                dados = TblBbBotRegistros1Sentenca.where('bot_id',bot_id).get()
                df_planilha = pd.DataFrame(dados)
                df_planilha.drop(['id', 'bot_controle_id','created_at', 'updated_at'], inplace=True)
                Enviar(robo='REGISTROS 1ª SENTENÇA', mensagem=mensagem, df=df_planilha, destinatario='nit@rms.adv.br', destinatario_cc='nit@rms.adv.br', tipo=True)
                
    except BaseException as e:
        print("Erro na execução do robô", e)
        
        # Atualiza a tabela de controle
        update_controle = {
                'robo_ativo': False,
                'apresentou_erro': True
        }
        if not TblBbBotsControle.findById(bot_id).update(update_controle):
            print("--> Erro ao atualizar controle:",update_controle)
        
        create_log = [{
                    'bb_bots_controle_id': bot_id, 
                    'descricao': str(e),
                    'user_login': bot_user_login
                    }]
        # inserir log da atividade na tabela
        if not TblBbBotsControleLogs.create(create_log):
            print("--> Erro ao inserir log:",create_log)
        
        exit("--> EXECUÇÃO ENCERRADA COM ERRO")