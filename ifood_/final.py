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

from datetime import date
import time
import os

from threading import Thread

class Ifood:
    def __init__(self, email):
        self.email = email
        self.senha = open(os.path.join('passwords', 'password_gmail'), 'r').read()
        self.valor_final = 0
        self.retorno = []

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

    
    def pedido(self, numero):
        self.init_ifood.join()

        pedidos = {1: 'big mac', 2: 'Cachorro Quente', 3: 'Açai com leite ninho'}
        match numero:
            case 1:
                # 1. Qual o termo especifico de pesquisa?
                pedido = pedidos[numero]
                time.sleep(3)
                search = self.driver.find_element(By.CSS_SELECTOR, "[role='search']")
                time.sleep(0.5)
                search.send_keys([Keys.CONTROL + "a", Keys.BACKSPACE])
                time.sleep(0.5)
                search.send_keys(pedido + Keys.ENTER)
                time.sleep(3)
                
                restaurantes = self.driver.find_elements(By.CLASS_NAME, "merchant-v2__name")

                for rest in restaurantes:
                    if "Mcdonald's".lower() in rest.text.lower():
                        rest.click()
                        break
                    
                while True:
                    try: self.driver.find_element(By.XPATH, '//*[contains(text(), "Sanduíche + Bebida")]').click(); break
                    except: time.sleep(2)
                
                list_options = self.driver.find_elements(By.CLASS_NAME, 'dish-garnishes')
                if len(list_options) != 0:
                    list_options = list_options[0].find_elements(By.CLASS_NAME, 'garnish-choices__list')
                else:
                    self.retorno = ["O restaurante esta fechado! Até a proxima."]

                options = list_options[0].find_elements(By.CLASS_NAME, 'garnish-choices__label')

                # Achando Big Mac
                for opt in options:
                    if "Big Mac" in opt.text:
                        opt.click()
                        time.sleep(0.5)
                        break
                
                options = list_options[1].find_elements(By.CLASS_NAME, 'garnish-choices__label')

                # Achando Coca-Cola Sem Açúcar
                for opt in options:
                    if "Coca-Cola Sem Açúcar" in opt.text:
                        opt.click()
                        time.sleep(0.5)
                        break

                options = list_options[2].find_elements(By.CLASS_NAME, 'marmita-counter')

                elemento = options[0].find_element(By.CSS_SELECTOR, '[aria-label="Aumentar quantidade"]')

                # Achando Sem Batata e Sem Nuggets
                for _ in range(2):
                    elemento.click()
                    time.sleep(0.5)
                
                # Adicionar pedido
                while True:
                    try: self.driver.find_element(By.XPATH, '//*[contains(text(), "Adicionar")]').click(); break
                    except: time.sleep(3)
                try:
                    if recado := self.driver.find_element(By.XPATH, '//*[contains(text(), "Esta loja abre às")]').text:
                        print(f"A loja esta fechada, {recado}")
                        self.driver.quit()
                except: pass

                self.driver.find_element(By.CSS_SELECTOR, '[aria-label="checkout-label"]').click()
                elemento = self.driver.find_element(By.CLASS_NAME, 'restaurant-cart-footer__button-wrapper')
                time.sleep(2)
                elemento.click()
                time.sleep(6)
                
                self.driver.find_element(By.XPATH, '//*[contains(text(), "Pague com Pix")]').click()
                time.sleep(3)

                self.driver.find_element(By.XPATH, '//*[contains(text(), "Fazer pedido")]').click()
                time.sleep(3)

                try:
                    recado = self.driver.find_element(By.XPATH, '//*[contains(text(), "O pedido mínimo para essa loja é de ")]').text
                    print(f"Nao foi possivel realizar o pedido pois {recado}")
                    self.driver.quit()
                except: pass

                valor = self.driver.find_element(By.XPATH, '//span[@data-test-id="total-price"]').text
                self.valor_final = float(valor[3:].replace(',', '.'))
            case 2:
                print("Pedido 2 foi requerido. Cachorro Quente")
            case 3:
                print("Pedido 3 foi requerido. Açai com leite ninho")

# bot = Ifood('nascimento.victor01@gmail.com')
# bot.pedido(1)