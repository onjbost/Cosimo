from django.shortcuts import render
from .models import *
# AI Librearies ----------------------------------------
import asyncio
import datetime
import os
import random
import re
import sys
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle



# Variabili Globali -----------------------------------------------------
application_path = os.path.dirname(sys.executable)
r = sr.Recognizer()
mic = sr.Microphone()
rate = 100
ans = ''

def deactive_cosimo(request):
    Check = False
    output = 'Output'
    context = {
        'check':Check,
        'output':output
    }
    return render(request, 'cosimo.html', context)

def active_cosimo(request):
    output = start_recognize()
    Check = True
    context = {
        'check' : Check,
        'output': output,
    }
    return render(request, 'cosimo.html', context)


# AI Functions
async def gpt():
    btn = 0
    while btn <= 1:
        try:
            ans = ascolta()
        except:
            ans = ''
        # if 'youtube' in ans:
        #     try:
        #         ans = ans.replace('youtube', '')
        #         ans = ans.replace('su ', '')
        #         ans = ans.replace('cerca ', '')
        #         ans = ans.replace('metti ', '')
        #     except:
        #         pass
        #     speak(f'Cerco {ans} su youtube')
        #     return f'Cerco {str(ans)} su youtube' 
        #     # isc.youtube_search(ans)
        if 'stop' in ans:
            speak('Va bene, vado a riposare!')
            return ('Va bene, vado a riposare!')
        
        elif 'che ore sono' in ans:
            time = datetime.datetime.now().strftime('%H:%M')
            speak(f'Sono le {time}')
            return f'Sono le {time}'
            
        elif 'stronza' in ans:
            ans = ans.replace('stronza', '')
            ans = ans.replace('una', '')
            ans = ans.replace('è', '')
            speak(f'{ans}, Vaffanculo')
            return f'{ans}, Vaffanculo'
        # elif 'google' in ans:
        #     try:
        #         ans = ans.replace('google', '')
        #         ans = ans.replace('cerca ', '')
        #         ans = ans.replace('su ', '')
        #     except:
        #         pass
        #     speak(f'Cerco {ans} su google')
        #     # result = isc.google_search(ans)
        #     # if result != 0:
        #         # speak(result)
        #     # else:
        #         # speak(f'Non ho trovato niente per {ans} su google')
            
        # elif 'wikipedia' in ans:
        #     try:
        #         ans = ans.replace('wikipedia', '')
        #         ans = ans.replace('cerca ', '')
        #         ans = ans.replace('su ', '')
        #     except:
        #         pass
        #     speak(f'Cerco {ans} su wikipedia')
        #     # result = isc.wikipedia_search(ans)
        #     # if result != 0:
        #         # speak(result)
        #     # else:
        #         # speak('Non ho trovato nulla a riguardo')
        else:
            bot = Chatbot(cookiePath='cookie.json')
            response = await bot.ask(prompt=ans, conversation_style=ConversationStyle.creative)
            bot_response = ''
            for message in response['item']['messages']:
                if message['author']=='bot':
                    bot_response = message['text']
            bot_response = re.sub('\[\^[0-9]+\^\]', '', bot_response)
            bot_response = re.sub('([\:\<]-?[)(|\\/pP3D])(?:(?=\s))', '', bot_response)
            bot_response = bot_response.replace('**', '')
            bot_response = bot_response.replace('Ciao, questo è Bing. ', '')
            bot_response = bot_response.replace('questo è Bing. ', '')
            speak(bot_response)
            await bot.close()
            return str(bot_response)

def speak(text):
    tts = gTTS(text, lang='it')
    tts.save('output.mp3')
    sound = AudioSegment.from_mp3('output.mp3')
    play(sound)

def ascolta():
    with mic as source:
        print('Listening...')
        try:
            audio = r.listen(source, 0, 10 )
            result = r.recognize_google(audio, language='it')
            result = str(result).lower()
        except:
            result = ''
    return result

def start_recognize():
    while True:
        command = ascolta()
        if 'cosimo' in command:
            if 'stop' in command:
                speak('Va bene, Vado a riposare signore')
                return('Va bene, Vado a riposare signore')
            else:
                speak(random.choice(reply()))
                asyncio.run(gpt())
        else:
            speak('Non ho capito')
            return('Non ho capito')


def reply():
    reply_list = ReplyWakeUp.objects.all()
    reply_check = []
    for reply in reply_list:
        text = reply.text.lower()
        reply_check.append(text)
    return reply_check