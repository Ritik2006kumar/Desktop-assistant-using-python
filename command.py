
import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text): 
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[2].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        
        
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            if "open" in query:
                from backend.feature import openCommand
                openCommand(query)
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
            else:
                from backend.feature import chatBot
                chatBot(query)
        else:
            speak("No command was given.")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
    
    eel.ShowHood()
'''
import speech_recognition as sr # install this icetension
import webbrowser
import pyttsx3    #pip install pyttsx3 
import musicLibrary
import requests
from openai import OpenAI
# pip install speechrecognition pyaudio
#pip install setuptools
#install audio




recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api="48c96c603ae9442da2b36fca7e86d249"
# convert the text into voice


def speak(text):
    engine.say(text)

    engine.runAndWait ()



def aiprocess(command):
    client = OpenAI(
    api_key="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"
    )
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages =[
        {"role" :"stystem" ,"content":"you are a virtual assistant named jarvis skilling in gernal tasks like alexa ,google could"} ,
        {"role":"user","contant": command}  
     ]
    )
    return completion.choices[0].message.content


def processCommand(c):    
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com") 
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")   
    elif c.lower().startswith("play"): 
        song=c.lower().split(" ")[1]
        link= musicLibrary.music[song]  
        webbrowser.open(link) 
    elif "what is the weather" in c.lower():
        webbrowser.open("https://weather.com")   
    elif "open chatGPT" in c.lower():
        webbrowser.open("https://chatGPT.com")
    elif "open code with harry" in c.lower():
        webbrowser.open("https://www.codewithharry.com/") 
    elif " the news" in c.lower():
        r=requests.get(f"https://api.sambanova.ai/v1={news_api}")
        if r.status_code == 200:
            #parse the json response
            data =r.json

            #extract the article
            articles =data.get('articles' , [])

            for article in articles:
                speak(article['title'])
            # speak a news 
    else:
         output = aiprocess(command)
         speak(output)     




if __name__ == "__main__":
    speak("initializing jarvis......")
    while True:
        #listen for the wake word "jarvis"
        #obtain audio form the microphone 
        r = sr.Recognizer()
        print("recognizing....")
            #recorgnize speech using sphinx


        try:
            with sr.Microphone() as sourse:
               print("listing...... ")
               audio =r.listen(sourse , timeout=2, phrase_time_limit=1)

            word = r.recognize_google(audio)
            if(word.lower()=="jarvis"):
              speak("ya")
              #listen for command

            

            with sr.Microphone() as sourse:
               print("jarvis active")
               audio =r.listen(sourse)
               command =r.recognize_google(audio)

               processCommand(command)


  
        except sr.UnknownValueError:
            print("jarvis active ...")

        except Exception as e:
            print(" error; {0}" .format(e))
           '''           