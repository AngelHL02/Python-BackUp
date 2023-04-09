#Pls put this python file in the same directory as your script file

# read the file
with open("Script.txt","r") as file:
    lst = file.read()
lst

import pyttsx3
# initialize Text-to-speech engine
engine = pyttsx3.init()

# convert this text to speech
text = lst
engine.setProperty("rate", 190)
engine.say(text)

# We can use file extension as mp3 and wav, both will work
engine.save_to_file(text, 'speech.mp3')

# play the speech
engine.runAndWait()