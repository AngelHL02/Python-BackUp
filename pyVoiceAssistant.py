import webbrowser

import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime #import datetime
import playsound
import pyjokes
import wikipedia
import pyaudio
import webbrowser #buildin function
#import winshell
from pygame import mixer

#get mic_audio
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        #except Exception as e:
            #print("Exception "+str(e))
        except sr.UnknownValueError: #Microphone did not pick up the audio properly
            speak("Sorry, I do not get that.")
        except sr.RequestError:
            speak("Sorry, your request is not available.")
    return said.lower()

def speak(text):
    tts = gTTS(text=text,lang='en')
    filename = "voice.mp3"
    try: #remove file with os module
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)

#Play music
def playmusic(song):
    mixer.init()
    mixer.music.load(song)
    mixer.music.play()

#Stop music
def stopmusic():
    mixer.music.stop()

def repeat(text):
    speak(text)

#-------------------------------------------------------------
#Function to response to request/commands
def respond(text):
    #print("Text from get audio :"+text)
    print("Command:" + text)

    if 'time' in text:
        strTime = datetime.today().strftime("%H:%m %p")
        print(f"Current time: {strTime}")
        speak(f"The time now is {strTime}")

    elif 'repeat' in text:
        repeat(text)

    elif 'joke' in text:
        speak(pyjokes.get_joke())

    elif 'empty recycle bin' in text:
        winshell.recycle_bin().empty(confirm=False,show_progress=True,sound=true)
        speak("Recycle Bin has been emptied")

    elif 'youtube' in text:
        #speak("Opening YouTube")
        #webbrowser.open_new_tab("https://www.youtube.com/")

        speak("YouTube is activated")

        #Search with specific keyword
        speak("What do you want to search for? ")
        keyword = get_audio()
        if keyword != "":
            url = f"https://www.youtube.com/results?search_query={keyword}"
            #webbrowser.get().open(url) #Open in background
            webbrowser.open_new_tab(url)
            speak(f"Here is the result for the corresponding keyword:{keyword}")

    elif 'search' in text: #Search in wiki

        #Search with specific keyword
        speak("What do you want to search for? ")
        query = get_audio()
        if query != " ":
            speak("Searching Wikipedia...")
            #query = text.replace("search","")
            result = wikipedia.summary(query,sentences = 3)
            print("According to wikipedia: ")
            speak("According to wikipedia")
            print(result)
            speak(result)

    #Music control
    elif 'play music' or 'play song' in text:
        speak("Now playing...")
        music_dir = "Music"
        #music_dir = "https://www.youtube.com/watch?v=uw6-n9QEigM&list=PLp2BwhvvACG3kBCn9gFeYZslYWBRwHnsk&index=46"
        songs = os.listdir(music_dir)
        #counter = 0
        print(songs) #List of songs available in your computer
        playmusic(music_dir + "\\" + songs[0])

    elif 'stop music' in text:
        speak("Music is paused.")
        stopmusic()

    #Exit Voice Assistant
    elif 'exit' in text:
        speak("Bye Bye, see you next time")
        exit()

#-------------------------------------------------------------

#Trial 1
#text = get_audio() #returns the text
#speak(text)

while True:
    print("I am listening...")
    speak("Waiting for instruction(s).")
    text = get_audio() #.lower() #for text comparison
    respond(text)

