import streamlit as st
import time
import textGenModel
import re
from PIL import Image
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import time
import cv2
import pyautogui
import numpy as np
import requests
from bs4 import BeautifulSoup                                                   #web Srapping
from requests import get
import psutil                                                                   #battery
#from googlesearch import search
from gnews import GNews
import pywhatkit


#wish
#date and time
#day
#note
#open facebook
#open twitter
#git hub
#stackoverflow
#voice command
#wikipedia
#youtube
#google
#amazon
#open command
#open code
#power left
#who are you,who made you
#location
#temperature
#screenshot
#shutdown and restart
#whatsapp
#question
#camera
#set alarm
#calculation
#joke
#switch window
#minimize or close
#other location
# what is "expert ans"
# play YT videos
# news
# search 
#exit


val = 0
sound = False
begin = False
brk = False
go = False
toggle = False

def speak2(wrd):
    st.write(wrd)
    if taskVoice:
        speak(wrd)

def takeCommand():
    # it will take voice commands input from the microphone

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.5  # when mic is listening our voice that time 1s gap can be okay
        r.energy_threshold = 10
        audio = r.listen(source)

        try:
            with st.spinner("Recognizing..."):
                query = r.recognize_google(audio,language='en-in')
                st.markdown(f"""<h2>User said:</h2><br><p>{query}</p>""", unsafe_allow_html=True)

        except:
            # print(e)
            st.error("Say That Again Please")
            return "none"
        query = query.lower()
        return query


def taskExecute(query):
    
    if taskEnable:  
        if "news" in query:
            google_news = GNews()
            speak2("please tell me place:")
            place = takeCommand()
            news = google_news.get_news(f"{place}")
            for i in range(1,4):
                speak2(f"{news[i]}")

        elif "where is" in query:
            try:
                query = query.replace("jarvis","")
                query = query.replace("where is","")
                location = query
                reply_location = "Locating",location, " in google maps"
                speak2(reply_location)
                webbrowser.open("http://www.google.com/maps/place/"+location)
            except:
                st.error("unable to locate this place")
        
        elif "note" in query:
            speak2("What Should I write, Sir")
            try:
                note = takeCommand()
                file = open('jarvis.txt', 'w')
                time_reply = " Should i include date and time"
                speak2(time_reply)
                snfm = takeCommand().lower()
                if 'yes' in snfm or 'sure' in snfm:
                    try:
                        strTime = datetime.datetime.now().strftime("% H:% M:% S")
                        file.write(strTime)
                        file.write(" :- ")
                        file.write(note)
                    except:
                        st.error("Sorry but note has been written without time")
                        file.write(note)
                else:
                    file.write(note)
            except:
                   st.error("Unable To Write note")

        elif "show notes" in query:
                file = open("jarvis.txt", "r")
                speak2(file.read())

        elif 'open youtube' in query:     
            webbrowser.open_new_tab("youtube.com")
            time.sleep(5)

        elif 'open facebook' in query:
                
            webbrowser.open_new_tab("facebook.com")
            time.sleep(5)

        elif 'open twitter' in query:
                
            webbrowser.open_new_tab("twitter.com")
            time.sleep(5)

        elif 'overflow' in query:
                
            webbrowser.open_new_tab("https://stackoverflow.com/")
            time.sleep(5)
            
        elif 'w3school' in query:
                
            webbrowser.open_new_tab("https://www.w3schools.com/")
            time.sleep(5)

        elif 'hub' in query:
                
            webbrowser.open_new_tab("https://github.com/")
            time.sleep(5)

        elif 'open google' in query:
                
            webbrowser.open_new_tab("google.com")
            time.sleep(5)

       # elif "shut down" in query:
            
           # os.system("shutdown /s /t 5")

       # elif "restart" in query:
            
            #os.system("shutdown /r /t 5")

        elif "date" in query or "year" in query :
            date = datetime.datetime.now()
            speak2(f"today's date is {date}")
            

        elif "day" in query :

            day = time.strftime("%A")
            speak2(f"today's day is {day}")

        elif "switch" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        #elif 'minimise' in query or 'background' or 'maximise' in query:
            #pyautogui.hotkey("win","w")

        #elif 'close' in query:
            #pyautogui.hotkey("ctrl","w")
            
        elif "power left" in query or "battery" in query:
            
            battery = psutil.sensors_battery()
            percentage = battery.percent
            speak2(f"sir our system have {percentage}% battery")

        elif "who are you" in query or "your name" in query or "yourself" in query:
            speak2("i am a virtual desktop assistant. myself jarvis.i am here to ease your computer related task")
            
        elif "who developed you" in query or "who made you" in query:
            speak2("i am invented by a student as a mini project. his name is Ritesh Pandit.")
             
        elif "where i am" in query or "where we are" in query or "location" in query:
            speak2("wait sir, let me check")
                    
            try:

                ipAdd = requests.get('https://api.ipify.org').text
                speak2(ipAdd)
                url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak2(f"sir i am not sure, but i think we are in {city} city of {country} country")
               
            except Exception as e:
                st.error("sorry sir , Due to network issue i am not able to find our location")
    
                
        elif "screenshot" in query:
            speak2("sir, please tell me the name for this screenshot file")
            name = takeCommand().lower()
            speak2("please sir hold the screen for few seconds, i am taking screenshot")
            time.sleep(3)
            img = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
            cv2.imwrite(f"{name}.png",img)
            speak2("i am done sir, the screenshot is saved in our main folder")


        elif "temperature" in query:
            speak2("at which location:")
            x = takeCommand().lower()
            search = f"temperature in {x}"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_="BNeawe").text
            speak2(f"current {search} is {temp}")
            
                
        elif 'open amazon' in query:
                
            webbrowser.open("amazon.in")
            
        elif 'open flipkart' in query:
            
            webbrowser.open("flipkart.com")
            time.sleep(5)
            
        elif 'time' in query:

            strTime = datetime.datetime.now().strftime("%H:%M:%S %p")
            speak2(f"the time is {strTime}")

        elif 'open code' in query:
            codepath = "C:\\Users\\momin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)
            time.sleep(10)
            
        elif 'exit' in query or 'quit' in query or 'bye' in query:
            speak2("Okay bye sir I am deactivating ")
            exit()

        elif 'whatsapp' in query:
            webbrowser.open("https://web.whatsapp.com/")
            time.sleep(5)
            
        elif 'play' in query:
            try:    
                query = query.replace("play","")
                pywhatkit.playonyt(query)
            except:
                pass

        elif "don't listen" in query or "wait" in query:
            speak2("tell me time for don't listening mode")
            try:
                o = takeCommand().lower()
                time.sleep(int(o))
            except:
                pass

        elif 'open command' in query:
            os.system("start cmd")
            time.sleep(2)
            
        elif 'open camera' in query:
            cap= cv2.VideoCapture(0)
            while True:
                ret,img=cap.read()
                cv2.imshow('webcam',img)
                k=cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        else:
            st.error("I am not able to understand")
            time.sleep(1)
            st.empty()
            
def setChoice(voice_choice):
    if voice_choice == "Male":
        return 0
    else:
        return 1

def speak(audio):
    #print(f"Speaking: {audio}")  
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[val].id)
    engine.say(audio)
    engine.runAndWait()

def playTime(text):
    st.write(text)
    speak(text)

def wishMe():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    time_text = ""
    if hour >= 0 and hour < 12:   
        time_text = f"good morning sir, its {tt}"

    elif hour >= 12 and hour < 18:
        time_text = f"good Afternoon sir, its {tt}"

    else:
        time_text = f"good Evening sir, its {tt}"

    time_text += "  I am Jarvis Please tell me how may I help you?"
    return time_text

def stream_data(data, delay: float = 0.02):

        placeholder = st.empty()   
        words = re.split(r'[ *]', data)
        streamed_text = ""  
        count = 0
        temp = ""
        for word in words:
            streamed_text += word + " "
            temp += word + " "
            if brk:
                break
            placeholder.write(temp)
            count +=1
            if count == 30 and sound:
                speak(streamed_text)
                count = 0
                streamed_text = ""
            time.sleep(delay) 

def process(prompt):
    if go:
        response = textGenModel.chatResponse(prompt)
        stream_data(response.text, delay=0.02)

st.title("AI Desktop Assistant")
st.divider()
if st.button("Start"):
    begin = True
st.divider()
#st.image("jarvis5.gif",width=200)
sidebar = st.sidebar
sidebar.title("Menu")
file = sidebar.file_uploader("Choose a Image file")


home, voice, task, about = st.tabs(["Home", "voice","Task", "About"])

with home:
    left, right = st.columns([2,0.5])
    with left:
        if begin:
            time_text = wishMe()
            playTime(time_text)
            begin = False

        st.subheader("ChatBot")
        prompt = left.text_input("Ask Something...", placeholder="Key of Knowledge...")

        if prompt:
            go = True
            sound = False
            with left.chat_message("user"):
                left.markdown(f"""<h3>You: {prompt}</h3>""", unsafe_allow_html=True)

            with st.spinner("Thinking...."):
                if prompt:
                    go = True     
                    left, right = st.columns(2)
                    with left:
                        if st.button("ResetChat"):
                            go = False 
                    with right:
                        if st.button("RestartChat"):
                            go = True
                    process(prompt)
    # with right:
    #     if st.button("StopChat"):
    #         brk = True 
    #         #go = True          

        elif file:
            go = True
            sound = False
            image = Image.open(file)
            placeholder = sidebar.empty()
            placeholder.success("File Uploaded successfully")
            time.sleep(1)
            placeholder.empty()
            left.image(image, caption='Uploaded Image.', width= 500)
            with st.spinner("Thinking...."):
                process(image)

    with right:
        st.subheader("")

with voice:
    st.subheader("Voice Assistant")
    # text = st.text_input("Enter Text:")
    # if st.button("Speak"):
    #     if text:
    #         speak(text)
    
    sound = False
    left, right = st.columns(2)
    with left:
        enable = st.toggle("Voice")
        if enable:
            sound = True

    with right:
        if enable:
            voice_choice = st.radio("Assistant", ["Male","Female"])
            val = setChoice(voice_choice)

    voicePrompt = voice.text_input("Text Something...", placeholder="Key of Knowledge...")
    if voicePrompt:
        go = True  
        left, right = st.columns(2)
        with left:
            if st.button("Stop"):
                go = False    
        with right:
            if st.button("Restart"):
                go = True
        process(voicePrompt)

with task:
    taskVoice = task.checkbox("Voice")
    taskEnable = task.toggle("Task")
    if taskEnable:
        with st.spinner("Listening..."):
            query = takeCommand()
            taskExecute(query)
            time.sleep(1)
            st.session_state.task_enable = False
    
            

with about:
    
    left, right = st.columns([1,2])
    with left:
        st.markdown("""
        <h5>Name</h5><br>
        <h5>Email</h5><br>
        <h5>Description</h5><br>
        <h5>Other links</h5><br>            
""", unsafe_allow_html=True)
    with right:
        st.markdown("""
        <h6>Ritesh Pandit</h6><br>
        <h6>karanstdio1234@gmail.com</h6><br>
        <h6>AI software automates computer related tasks such as controlling operating System and browsing.
                    It also have capability to talk using voice and answers all questions smartly using ML model</h6><br>
        <h6>https://www.linkedin.com/in/ritesh-pandit-408557269/</h6><br>   
        <h6>https://github.com/</h6>         
""", unsafe_allow_html=True)
    st.divider()
        # Define the tasks and capabilities
    import streamlit as st

    # Define the tasks and capabilities
    tasks = [
        "Wish the user a good time of day (morning, afternoon, evening)",
        "Display today's date and time",
        "Question-Answering",
        "Mathematics and Calculations"
        "Show today's day",
        "Take notes and save them",
        "Open Facebook, Twitter, GitHub, Stack Overflow",
        "Execute voice commands",
        "Search on Wikipedia, YouTube, and Google",
        "Open Amazon and other websites",
        "Open Command Prompt and VS Code",
        "Check remaining battery percentage",
        "Introduce itself and its creator",
        "Retrieve location and weather temperature",
        "Take a screenshot",
        "Shut down and restart the computer",
        "Open WhatsApp web",
        "Answer general questions (e.g., 'expert ans')",
        "Play YouTube videos",
        "Fetch news",
        "Perform searches",
        "Exit the assistant",
        "Open the camera",
        "Set alarms",
        "Perform calculations",
        "Tell jokes",
        "Switch windows",
        "Minimize or close windows",
        "Locate other places",
        "Many More"
    ]

    # Generate the markdown content with improved CSS styling
    about_text = f"""
    <div style="background-color: rgb(40 40 40); padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); font-family: Arial, sans-serif; color: white;">
        <h2 style="font-size: 24px; color: white; margin-bottom: 15px;">About This Virtual Assistant</h2>
        <p>This virtual assistant, built using Streamlit, is capable of performing various tasks to assist you with your daily activities and queries. Below are some of its capabilities:</p>

        <ul style="list-style-type: disc; padding-left: 20px;">
    """

    # Add each task as a list item
    for task in tasks:
        about_text += f'<li style="font-size: 16px; margin-bottom: 8px;">{task}</li>\n'

    about_text += """
        </ul>
    </div>
    """

    # Display the styled markdown in the About tab
    st.markdown(about_text, unsafe_allow_html=True)
