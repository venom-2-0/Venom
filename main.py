import pyttsx3
import speech_recognition as sr
import winsound
import subprocess
from openai import OpenAI
import webbrowser
import pywhatkit
import time
import pygame
import threading

apikey = 'put api key here'
TALKING = False
chatstr = ''

class ImageHandler:
    def __init__(self):
        self.pics = dict()

    def loadFromFile(self, filename, id=None):
        if id == None: 
            id = filename
        self.pics[id] = pygame.image.load(filename).convert()

    def loadFromSurface(self, surface, id):
        self.pics[id] = surface.convert_alpha()

    def render(self, surface, id, position=None, clear=False, size=None):
        if clear == True:
            surface.fill((5, 2, 23))

        if position == None:
            picX = int(surface.get_width() / 2 - self.pics[id].get_width() / 2)
            picY = int(surface.get_height() / 2 - self.pics[id].get_height() / 2)
        else:
            picX, picY = position[0], position[1]

        if size == None:
            surface.blit(self.pics[id], (picX, picY))
        else:
            surface.blit(pygame.transform.smoothscale(self.pics[id], size), (picX, picY))

pygame.display.init()
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
handler = ImageHandler()

def display():
    for i in range(1, 151):
        file_path = f"Venom\\face\\{i}.gif"
        handler.loadFromFile(file_path, str(i))
    for i in range(1001, 1151):
        file_path = f"Venom\\face\\{i}.gif"
        handler.loadFromFile(file_path, str(i))

def face():
    A = 150
    B = 0
    x = 700
    y = 550

    COUNT = 1
    global TALKING
    while True:
        if TALKING == False:
            if COUNT > 151:
                COUNT = COUNT - 1000
            # for i in range(1, 151):
            handler.render(screen, str(COUNT), (A, B), True, (x, y))
            pygame.display.update(150, 0, 700, 550)
            time.sleep(0.04)
            COUNT = COUNT+1
            if COUNT == 151:
                COUNT = 1
        elif TALKING == True:
            if COUNT < 1000:
                COUNT = COUNT + 1000
            # for i in range(1001, 1151):
            handler.render(screen, str(COUNT), (A, B), True, (x, y))
            pygame.display.update(150, 0, 700, 550)
            time.sleep(0.04)
            COUNT = COUNT+1
            if COUNT == 1151:
                COUNT = 1001

def Speak(text):
    global TALKING
    rate = 100
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', rate+50)
    TALKING = True
    engine.say(text)
    engine.runAndWait()
    TALKING = False

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("My ears are all yours...")
        winsound.Beep(600,300)
        audio = r.listen(source)
    query = ''
    winsound.Beep(400,300)
    try:
        query = r.recognize_google(audio, language="en-US")
        print(f"Ravi said: {query}")
    except sr.UnknownValueError:
        print("Venom couldn't understand you!")
        Speak("Sorry, I couldn't understand that. Can you please repeat?")
    except sr.RequestError as e:
        print(f"Error: Could not request results from Google Speech Recognition service; {e}")
        Speak("Sorry, there was an issue with the speech recognition service. Please try again later.")
    return query.lower()

def open_application(application):
    try:
        subprocess.Popen([application])
        print(f"Opened {application}")
    except FileNotFoundError:
        print(f"Error: {application} not found.")

def GoogleSearch(term):
    query = term.replace("venom", "")
    Query = str(query)
    pywhatkit.search(Query)
    Speak(f": Result of : {Query} is on this page...")

def YouTubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    webbrowser.open(result)
    Speak("This Is What I Found For Your Search .")
    pywhatkit.playonyt(term)
    Speak("This May Also Help You Sir .")

def convo(query):
    global chatstr
    client = OpenAI(api_key=apikey)
    chatstr += f"Ravi : {query}\n Venom :"

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": chatstr
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    try :
        Speak(response.choices[0].message.content)
        chatstr += f"{response.choices[0].message.content}\n"
        
    except Exception as e:
        print(e)

def Conversation():
    Speak("Greetings to my Overlord")
    while True:
        userSaid = takeCommand()

        if "hello" in userSaid:
            Speak("Hello my lord, What can I do for you?")
        elif 'google search' in userSaid or 'search on google' in userSaid:
            userSaid = userSaid.replace("google search", "")
            userSaid = userSaid.replace("search on google", "")
            GoogleSearch(userSaid)
        elif 'you tube search' in userSaid or 'youtube search' in userSaid or 'search on youtube' in userSaid or 'search on you tube' in userSaid:
            userSaid = userSaid.replace("venom","")
            userSaid = userSaid.replace("youtube search","")
            userSaid = userSaid.replace("you tube search","")
            userSaid = userSaid.replace("search on you tube","")
            userSaid = userSaid.replace("search on youtube","")
            YouTubeSearch(userSaid)
        elif "bye" in userSaid:
            Speak("As you wish my lord, Farewell")
        elif "open my email" in userSaid:
            Speak("This is where I would open your email.")
        elif ("open youtube" in userSaid or "open the youtube" in userSaid ):
            webbrowser.open("https://www.youtube.com")
            Speak("Opening Youtube...")
        elif ("open google" in userSaid or "open the google" in userSaid):
            webbrowser.open("https://www.google.com")
            Speak("Opening Google...")
        elif ("open notes" in userSaid or "open the notes" in userSaid or "open the note" in userSaid or "open note" in userSaid):
            webbrowser.open("https://keep.google.com/")
            Speak("Opening Google Notes...")  
        elif ("open satck overflow" in userSaid or "open the satck overflow" in userSaid):
            webbrowser.open("https://stackoverflow.com/")
            Speak("Opening stackoverflow...")
        elif "open calculator" in userSaid or "open calcu lator" in userSaid:
            open_application('calc')
            Speak("Opening Calculator...")
        elif "open terminal" in userSaid:
            open_application('cmd')
            Speak("Opening Terminal...")
        elif "open notepad" in userSaid:
            open_application('notepad')
            Speak("Opening Notepad...")
        elif "open browser" in userSaid:
            open_application('msedge')
            Speak("Opening Microsoft Edge...")
        elif "open chrome" in userSaid:
            open_application('chrome')
            Speak("Opening Chrome...")
        elif "open file manager" in userSaid:
            open_application('explorer')
            Speak("Opening File Explorer...")
        elif "open word" in userSaid:
            open_application('winword')
            Speak("Opening Microsoft Word...")
        elif "open excel" in userSaid:
            open_application('excel')
            Speak("Opening Microsoft Excel...")
        elif ("open power point" in userSaid or "open powerpoint" in userSaid):
            open_application('powerpnt')
            Speak("Opening Microsoft PowerPoint...")
        elif 'venom close' in userSaid or 'stop venom' in userSaid or 'venom stop' in userSaid:
            print("Are you sure? You want me to go?")
            Speak("Are you sure? You want me to go?")
            input = takeCommand()
            if "yes" in input or "go away" in input:
                print("As you command my lord, I am going.!")
                Speak("As you command my lord, I am going.!")
                # break
                exit()
            elif "no" in input:
                print("Thank you, I am glad you choose to stay with me.")
                Speak("Thank you. I am glad you choose to stay with me...")
        else:
            convo(userSaid)

        time.sleep(2)
        
def main():
    t1 = threading.Thread(target=Conversation)
    t2 = threading.Thread(target=face)

    display()
    t1.start()
    t2.start()

main()