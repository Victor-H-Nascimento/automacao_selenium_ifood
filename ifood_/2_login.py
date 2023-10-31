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
        
        self.init_ifood = Thread(target=open_ifood, args=(self,))
        self.init_ifood.start()
        pass


bot = Ifood(getenv('EMAIL'))