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
        self.retorno = -1
        
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

    
    def ouvir_microfone(self):
        # Habilita o microfone
        microfone = sr.Recognizer()
        with sr.Microphone() as source: 
            # Chama um algoritmo de reducao de ruidos no som
            microfone.adjust_for_ambient_noise(source)
            
            # Frase para o usuario dizer algo e armazenamento do audio
            playsound(os.path.join('default_audios', 'talk.mp3'))
            audio = microfone.listen(source)
        
        # Passa a variável para o algoritmo reconhecedor de padroes com proteção pra caso de falha relativo ao padrão de reconhecimento
        try: 
            frase = microfone.recognize_google(audio,language='pt-BR')
            print(frase)
        except sr.UnknownValueError: 
            playsound(os.path.join('default_audios', 'error.mp3'))
            os.remove('last_commmand.mp3')
            time.sleep(3)
            return self.ouvir_microfone()

        return frase
    
    def reproduzir_audio(self, txt, file='last_commmand.mp3'): 
        # Objeto Google Text-to-Speech e play no audio
        tts = gTTS(txt, lang='pt-br')
        time.sleep(0.5)
        try:
            tts.save(file)
        except:
            import pdb; pdb.set_trace()
        playsound(file)
