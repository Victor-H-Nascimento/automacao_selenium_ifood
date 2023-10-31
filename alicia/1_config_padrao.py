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
        pass