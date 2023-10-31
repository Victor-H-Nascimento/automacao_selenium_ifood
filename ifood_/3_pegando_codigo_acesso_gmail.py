'''
pip install selenium
pip install webdriver-manager
pip install imbox

Selenium - browser automation software
WebDriver - explica o Chrome pro Selenium - ChromeDriver
Chrome - web browser
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from imbox import Imbox
from os import getenv

from datetime import date
import time
import os

from threading import Thread

class Ifood:
    def __init__(self, email):
        self.email = email
        self.senha = open(os.path.join('passwords', 'password_gmail'), 'r').read()
        self.valor_final = 0
        self.retorno = -1

        # inicializando o ifood
        self.initialize_ifood()

    def initialize_ifood(self):
        # inserindo processo de inicialização em uma função para utilizar como thread
        # afinal, se o navegador não estiver aberto, as outras funcs não podem rodar
        def open_ifood(self):
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            # chrome_options.add_argument("--headless") # para abrir o navegador sem UI

            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.driver.get("https://www.ifood.com.br/inicio")
            time.sleep(1)
            assert "iFood" in self.driver.title

             # Logando via email
            while True:
                try:
                    self.driver.find_element(By.XPATH, '//*[contains(text(), "Entrar ou cadastrar")]').click()
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//*[contains(text(), "E-mail")]').click()
                    time.sleep(2)
                    self.driver.find_element(By.NAME, "email").send_keys(self.email + Keys.RETURN)
                    break
                except: pass

             # Verificação do código do email - consumindo do email para inserir no ifood
            try:
                time.sleep(2)  # tempo pro ifood mandar o código
                host = 'imap.gmail.com'

                mail = Imbox(host, username=self.email, password=self.senha)

                # TESTES =====================
                while True:
                    time.sleep(2) # evitar over request
                    msgs_do_ifood = mail.messages(sent_from='naoresponder@login.ifood.com.br', date__gt=date.today())
                    time.sleep(1)
                    msg_list = [msg for uid, msg in msgs_do_ifood]
                    time.sleep(1)
                    if msg_list == None:
                        print("O código de acesso não foi enviado... Tentantiva de reenviar")
                        self.driver.find_element(By.XPATH, '//*[contains(text(), "Não recebi meu código")]').click()
                        self.driver.find_element(By.XPATH, '//*[contains(text(), "Reenviar código")]').click()
                        continue
                    else:
                        title = msg_list[-1].subject
                        if "é o seu código de acesso" in title:
                            for n, code in enumerate(title[:6]):
                                time.sleep(0.2)
                                self.driver.find_element(By.ID, f'otp-input-{n}').send_keys(code)
                        else: continue
                    try:
                        time.sleep(1.5)
                        self.driver.find_element(By.XPATH, '//*[contains(text(), "Código expirado ou inválido")]')
                        for n in range(6): self.driver.find_element(By.ID, f'otp-input-{n}').send_keys(Keys.BACKSPACE)
                    except: break
            except Exception as e: print('\n Exception: ', e)
            # Selecionando a localização
            while True:
                try: self.driver.find_element(By.CSS_SELECTOR, "[aria-label=Casa]").click(); break
                except: time.sleep(5)
        
        self.init_ifood = Thread(target=open_ifood, args=(self,))
        self.init_ifood.start()
        pass


bot = Ifood(getenv('EMAIL'))
