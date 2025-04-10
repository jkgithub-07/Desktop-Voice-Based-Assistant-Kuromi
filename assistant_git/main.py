import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
from decouple import config
from datetime import datetime
from const import random_text 
from random import choice
from online import find_my_ip, search_on_google,search_on_wiki,youtube,send_email, get_news
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up client with Groq's base URL
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="base-url"
)

def kuromi_chat_groq(prompt):
    messages = [
        {"role": "system", "content": "You are Kuromi from Sanrio. A bratty, cute, sassy anime assistant with chaotic energy. You tease the user but also help them with questions and tasks."},
        {"role": "user", "content": prompt}
    ]

    try:
        chat_response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.9,
            max_tokens=200
        )
        return chat_response.choices[0].message.content.strip()
    except Exception as e:
        return f"Oopsie~ I broke something: {e}"


engine = pyttsx3.init('sapi5')
engine.setProperty('volume',1.5)
engine.setProperty('rate',225)
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id) # 1 to speak as female 0 for male voice

USER = config('USER')
HOSTNAME = config('BOT')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_me():
    hour = datetime.now().hour
    if(hour>=6 and hour<12):
        speak(f"Good Morning {USER}")
    elif(hour>=12 and hour<=16):
        speak(f"Good afternoon {USER}")
    elif(hour>=16 and hour<19):
        speak(f"Good evening {USER}")
    speak(f"hello ! Kuromi's here and fabulous as always! How can i assist you?")        

listening = False
def start_listening():
    global listening
    listening = True
    print("started listening..")

def pause_listening():
    global listening
    listening = False
    print("stopped listening...")

keyboard.add_hotkey('ctrl+alt+l', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)        

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("recognising..")
        queri = r.recognize_google(audio,language='en-in') 
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour 
            if   hour >= 21 and hour<6:
                speak("Good night, take care!")
            else:
                speak("Aready? BYE-BYE. Don’t miss me too much, hehe! Have a good day!")   
            exit()  
    except Exception:
        speak("Oof, that totally went over my head! come again, pumpkin?")
        queri = 'None'
    return queri    


if __name__ == '__main__':    
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I'm chaotic, caffeinated, and cute. Thanks for asking")
            elif "open command prompt" in query:
                speak("Ugh, fine. Opening it just for you~. opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("opening camera")
                sp.run('start microsoft.windows.camera:',shell=True)

            elif "open notepad" in query:
                speak("Ugh, fine. Opening it just for you~. opening notepad")
                sp.Popen("notepad.exe")       
            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"your ip address is {ip_address}"
                )
                print(f"ip address is {ip_address}")

            elif "youtube" in query:
                speak("what do you want to play on youtube?")  
                video = take_command().lower()
                youtube(video)

            elif "google" in query:
                speak(f"what do you want to search on google?")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia"  in query:
                speak("what do you want to search on wikipedia?")
                search = take_command().lower()
                results = search_on_wiki(search)
                speak(f"according to wikipedia, {results}")
                speak("i am printing it on terminal")
                print(results)    

            elif "send an email" in query:
                speak("On what email address do you want to send an email?")
                receiver_add = input("Email address: ")
                speak("what should be the subject?")
                subject = take_command().capitalize()
                speak("what is the message?")
                message = take_command().capitalize()

                if send_email(receiver_add,subject,message):
                    speak("email sent")
                    print("email sent")
                else:
                    speak("something went wrong")       
            elif 'give me news' in query:
                speak(f"I am reading out the latest headlines of today")
                speak(get_news())
                speak("I am printing in screen")
                print(*get_news(),sep='\n')

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name :")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for "+text)
                speak("i found this")  
                for movie in movies[:1]:
                  title = movie["title"]
                  year = movie["year"]
                  speak(f"{title} -- {year}")
                  info = movie.getID()
                  movie_info = movies_db.get_movie(info)
                  rating = movie_info["rating"]
                  cast = movie_info["cast"]
                  actor = cast[0:5]
                  plot = movie_info.get('plot outline','plot summary not available')
                  speak(f"{title} was released in {year} has imdb ratings of {rating}, it has a cast of {actor}. the plot summary of the movies is {plot}")
                  print(f"{title} was released in {year} has imdb ratings of {rating}, it has a cast of {actor}. the plot summary of the movies is {plot}")

            elif "calculate" in query:
                app_id = os.getenv("WOLFRAM_API_KEY")
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("the answer is "+ans)
                    print("the answer is "+ans)
                except StopIteration:
                    speak("Something went boo! wrong! try again")

            elif "what is" in query or 'who is' in query or 'which is' in query:
                app_id = os.getenv("WOLFRAM_API_KEY")
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                    query.lower().index('who is') if 'who is' in query.lower() else\
                    query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        result = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("the answer is "+ans)
                        print("the answer is "+ans)
                    else:
                        speak("i couldn't find that")

                except StopIteration:
                    speak("Something went boo! wrong! try again")             

            elif "write" in query:
                os.system("notepad")
                speak("Okay, what should i write?")
                text = take_command()
                pyautogui.write(text, interval=0.1)
                pyautogui.press("enter")

            else:
                speak("well,")
                response = kuromi_chat_groq(query)
                speak(response)
                print(f"[Kuromi LLM]: {response}")