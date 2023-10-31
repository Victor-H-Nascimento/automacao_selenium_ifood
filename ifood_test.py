from ifood_class import Ifood
from os import getenv

bot = Ifood(getenv('EMAIL'))

bot.pedido('padrao', 1)

# Classe pra teste apenas do fluxo do selenium, sem voz