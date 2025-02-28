import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import tkinter as tk

# Enabling voices
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[0].id)  # Set to male voice
    else:
        print("No voices found or only one voice available.")
except Exception as e:
    print("Error initializing text-to-speech engine:", e)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to make JARVIS greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am your mini JARVIS. How may I help you today?")  # Intro line

def describe():
    description = """
    I am JARVIS, a virtual assistant, created by Mr. Pradhan, on October 9th, 2024.
    I am capable of performing various tasks:
    - I can search Wikipedia for information.
    - I can open popular websites like YouTube, Google, Spotify, and Wikipedia.
    - I can tell you the current time.
    - You can interact with me using voice commands.
    Currently, I am at my beginning stage, so please don't get angry if I am not able to answer something.
    """
    speak(description)
    print(description)

# Function to capture user commands via voice
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio. Please try again.")
        return "None"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "None"
    except Exception as e:
        print("Error:", e)
        print("Say that again, please...")
        return "None"

    return query

if __name__ == "__main__":

    wishMe()
    while True:
        query = takeCommand().upper()
        if query == "None":
            continue

        if 'EXIT' in query or 'STOP' in query or 'OK BYE JARVIS' in query:
            speak("Goodbye! Have a nice day!")
            print("Goodbye! Have a nice day!")
            break

        elif 'WIKIPEDIA' in query:
            speak("Searching Wikipedia...")
            query = query.replace("WIKIPEDIA", "")
            try:
                results = wikipedia.summary(query, sentences=5)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("There were multiple results for your query. Please be more specific.")
                print(e)
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("There was an issue with Wikipedia. Please try again later.")
                print("HTTPTimeoutError")

        elif 'YOUTUBE' in query:
            webbrowser.open("youtube.com")

        elif 'GOOGLE' in query:
            webbrowser.open("google.com")
        
        elif 'SPOTIFY' in query:
            webbrowser.open("spotify.com")

        elif 'TIME' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)

        elif 'DESCRIBE' in query or 'TELL ME ABOUT YOURSELF' in query:
            describe() 
    