'''
pip install SpeechRecognition       => reconhecimento da voz
pip install pyaudio                 => reconhecimento da voz
pip install gTTS                    => API com o google text to speech
pip install playsound==1.2.2        => reproduz a file mp3

REF.: https://letscode.com.br/blog/speech-recognition-com-python
'''

import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os
import time

class Alicia:
    def __init__(self):
        self.quit_keywords = ['sai', 'fecha', 'encerra']
        self.quit = False
        self.retorno = []
        
        self.loop()
    
    def loop(self, txt=''):
        txt = txt + ' ' + self.ouvir_microfone()
        if any(word in txt for word in self.quit_keywords):
            self.quit = True

         # Escolhendo o pedido
        escolha = ''
        if 'big mac' in txt.lower():
            escolha = 'Big Mac'
            self.retorno = 1
        elif 'cachorro quente' in txt.lower():
            self.retorno = 2
            escolha = 'Cachorro Quente'
        elif 'açaí' in txt.lower():
            self.retorno = 3
            escolha = 'Açai'
        else:
            print("Nao entendi nada")
            return self.ouvir_microfone()
        
        self.reproduzir_audio(f"Excelente escolha. Vamos fazer um pedido de {escolha}", "alternative_command.mp3")

        
    def ouvir_microfone():
        pass
    
    def reproduzir_audio():
        pass