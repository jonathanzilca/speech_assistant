from neuralintents import GenericAssistant
import difflib
import glob
import json
import speech_recognition  # for the voice recognition
import pywhatkit as k  # in order to send a whatsapp message
import pyttsx3  # for robot voice
import wikipedia  # to use wikipedia through robot
import webbrowser  # to open web browsers
import time  # for time.sleep()
import subprocess  # to open files on the computer
import random
import cv2
import numpy as np
import face_recognition
import os
import requests
import re
import datetime
import functions
from re import match

#########################################static information and small databases#########################################

jokes = [["Why shouldn't you write with a broken pencil?", "Because it's pointless."],
         ["What's the best thing about Switzerland?", "I don't know, but there flag is a big plus"],
         ["How do you call a man without a body and a nose?", "Nobody nose."],
         ["How do you call an American bee?", "a USB."],
         ["Why did the picture go to jail?", "because it was framed."],
         ["Did you sit on the F5 key?", "Because your ass is refreshing!"],
         ["I wish the corona virus started in Las Vegas", "Because what happens in Vegas stays in Vegas"],
         ["I told my wife she was drawing her eyebrows too high", "She looked surprised"]]

random.shuffle(jokes)
jokes_counter = 0

send_url = "http://api.ipstack.com/check?access_key=2a0a4487b2bdee553fa34672568b5935"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
currentLocation = geo_json['city'] + ", " + geo_json['country_name']

robot_name = "jarvis"


#########################################static information and small databases######################################

def robot_say(audio_string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()


def take_command():
    with speech_recognition.Microphone() as mic:
        speech_recognition.Recognizer().adjust_for_ambient_noise(mic, duration=0.2)
        audio = speech_recognition.Recognizer().listen(mic)

        try:
            command = speech_recognition.Recognizer().recognize_google(audio)
            print("You: {}".format(command))
        except speech_recognition.UnknownValueError:
            return "meow"
        except speech_recognition.RequestError:
            functions.robot_say("Sorry, my speech service is down")

        return command.lower()


def personality():
    global robot_name
    robot_say("I am a virtual assistant named " + str(robot_name).upper() + " which was designed by Jonathan.")
    robot_say("I am here to make everyone's life easier and better.")


def tellJokes():
    global jokes_counter
    robot_say(jokes[jokes_counter][0])
    time.sleep(2)
    robot_say(jokes[jokes_counter][1])
    jokes_counter = jokes_counter + 1
    if jokes_counter is len(jokes):
        jokes_counter = 0


def sendingMassage():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    seconds = int(datetime.datetime.now().second)
    if 40 <= seconds < 60:
        minute = minute + 2
    else:
        minute = minute + 1
        robot_say("To who would you like to message?")
        my_contact = {
            # ###########family#################
            # me:
            "to me": '+972503345739',
            "to myself": '+972503345739',
            "me": '+972503345739',
            "myself": '+972503345739',
            "self": '+9725033'
                    '45739',
            # mother:
            "mom": "+972537345739",
            "mother": "+972537345739",
            "emma": "+972537345739",
            "lia": "+972537345739",
            # father:
            "roni": "+972522744248",
            "abba": "+972522744248",
            "papa": "+972522744248",
            # shira:
            "shira": "+972523507576",
            "she-ra": "+972523507576",
            # dani:
            "daniel": '+972523218086',
            "loser": '+972523218086',
            "efes": '+972523218086',
            "dani": '+972523218086',
            "doona": '+972523218086',
            # micheal:
            "mishael": "+972524797269",
            "mishel": "+972524797269",
            "michel": "+972524797269",
            "michael": "+972524797269",
            # magal:
            "magal": "+972526003830",
            "miguel": "+972526003830",
            # ###########family#################

            # ###########friends#################
            # banov:
            "banov": "+972546156775",
            # idan:
            "beta": "+972586245315",
            "idan": "+972586245315",
            # dolev:
            "dolev": "+972506791105",
            # ori:
            "ori": "+972548015343",
            # alon:
            "alon": "+972587312954",
            # zelig:
            "zelig": "+972585667666",
            # lior:
            "lior": "+972542101004",
            # elad:
            "elad": "+972542214882",
            # bremer:
            "bremer": "+972542868238",
            # yahav:
            "yahav": "+972542600073",
            # ilan:
            "ilan": "+972506506033",
            # mati:
            "mati": "+972535223182",
            "matvey": "+972535223182"
        }
        contacts_names = list(my_contact.keys())
        which_person = take_command()

        rightPerson = difflib.get_close_matches(which_person, contacts_names, len(contacts_names), 0)
        rightPhoneNumber = my_contact[rightPerson[0]]

        robot_say("What is the message?")
        body_text = take_command()
        try:
            k.sendwhatmsg(rightPhoneNumber, body_text, hour, minute)
        except:
            robot_say("I was failed to send the message")


def watchMovie():
    which_movie = ""
    movies_path = glob.glob("D:\\MOVIES\**\*\*\*.mp4", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.mkv", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.avi", recursive=True)

    if "play" in request:
        which_movie = request.split("play")[1]
    elif "open" in request:
        which_movie = request.split("open")[1]
    elif "watch" in request:
        which_movie = request.split("watch")[1]
    elif "see" in request:
        which_movie = request.split("see")[1]

    # probably the right movie
    rightMoviePath = difflib.get_close_matches(which_movie, movies_path, len(movies_path), 0)

    i = 0
    while i < 10:
        previous_movie = subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", rightMoviePath[i]])
        robot_say("Is this the right movie sir?")
        approve = take_command()

        if "yes" in approve or "right" in approve or "correct" in approve:
            robot_say("Enjoy the movie master")
            break
        elif "leave" in approve or "exit" in approve or "get out" in approve or "shut" in approve or "zip" in approve or "fuck off" in approve:
            robot_say("It's hard for me to find your movie. Sorry.")
            break
        elif "meow" in approve:
            robot_say("I can't hear you")
            previous_movie.terminate()
            continue
        else:
            previous_movie.terminate()
            robot_say("Oops. Let me try again")
            i += 1


def disneyRecommendation():
    disney_movies_path = glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mp4", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mkv", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.avi", recursive=True)

    disneyMoviesNames = []
    for me in disney_movies_path:
        moviesName = me.split("\\")[-1].split(".")[0]
        disneyMoviesNames.append(moviesName)

    random.shuffle(disneyMoviesNames)

    print("----------------------------------------")
    robot_say("Here are some recommended Disney movies:")
    print(disneyMoviesNames[0])
    print(disneyMoviesNames[1])
    print(disneyMoviesNames[2])
    print(disneyMoviesNames[3])
    print(disneyMoviesNames[4])
    print("----------------------------------------")


def marvelRecommendation():
    marvel_movies_path = glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mp4", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mkv", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.avi", recursive=True)

    marvelMoviesNames = []
    for me in marvel_movies_path:
        onlyName = me.split("\\")[-1].split(".")[0]
        marvelMoviesNames.append(onlyName)

    random.shuffle(marvelMoviesNames)
    print("----------------------------------------")
    robot_say("Here are some recommended Marvel movies:")
    print(marvelMoviesNames[0])
    print(marvelMoviesNames[1])
    print(marvelMoviesNames[2])
    print(marvelMoviesNames[3])
    print(marvelMoviesNames[4])
    print("----------------------------------------")


def Alarm():
    num = [int(s) for s in re.findall(r'\b\d+\b', request)]
    if len(num) == 1:
        alarm_min = 0
    elif len(num) == 0:
        return
    else:
        alarm_min = num[1]
    if "p.m" in request:
        alarm_hour = num[0] + 12
    else:
        alarm_hour = num[0]

    # calculate for how long should the bot sleep
    while alarm_min > 59 or alarm_hour > 24 or len(num) >= 3:
        robot_say("when Sir?")
        body_time = take_command()
        num = [int(s) for s in re.findall(r'\b\d+\b', body_time)]

    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute

    time_to_sleep = 0
    if alarm_hour < hour or (alarm_hour <= hour and alarm_min < minute):
        time_to_sleep = 3600 * 24
    time_to_sleep += (alarm_hour - hour) * 3600 + (alarm_min - minute) * 60 - datetime.datetime.now().second
    # sleep
    time.sleep(time_to_sleep)

    functions.sound_alarm(alarm_hour, alarm_min, currentLocation)


def faceRecognizerCalculator():
    path = "imagesAttendance"
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    # print(classNames)

    def findEncoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncoding(images)
    print("Encoding complete")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    curName = ""
    name = "  "

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
        for encodeFace, faceLocation in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            face_accuracy = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(face_accuracy)

            if matches[matchIndex]:
                name = classNames[matchIndex]
                # x1, y1, x2, y2 = faceLocation
                # x1, y1, x2, y2 = x1 * 4, y1 * 4, x2 * 4, y2 * 4
                # # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2) # to create a square around the face
                # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)  # place to write the name
                # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1) # writing the name
                the_most_right_match = min(face_accuracy)
                if the_most_right_match > 0.55:
                    name = "Unknown"
                    # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                    # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)
                    # cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 1)

            if curName is not name:
                curName = name
            if curName == name:
                return name


def faceRecognition():
    year = int(datetime.datetime.now().year)

    robot_say("Recognizing...")
    recognized_name = faceRecognizerCalculator()

    if "Jonathan" == recognized_name:
        robot_say("hey master")
        robot_say("your name is Jonathan Zilca and are " + str(year - 2002) + " years old.")
        robot_say("These days you work as a soldier.")

    if "Lia" == recognized_name:
        robot_say("Her name is Lia Zilca and she is " + str(year - 1961) + " years old.")
        robot_say("These days she works as a nurse in the Asaf Haroffe hospital.")

    if "Roni" == recognized_name:
        robot_say("His name is Roni Zilca and he is " + str(year - 1962) + " years old.")
        robot_say("These days he works as a lawyer.")

    if "Daniel" == recognized_name:
        robot_say("His name is Daniel Zilca and he is " + str(year - 1992) + " years old.")
        robot_say("These days he works as a programmer.")

    if "Michal" == recognized_name:
        robot_say("Her name is Micheal Zilca and she is " + str(year - 1999) + " years old.")
        robot_say("These days she works as a artist.")

    if "Alon" == recognized_name:
        robot_say("His name is Alon dalach and he is " + str(year - 2002) + " years old.")
        robot_say("These days she works as a soldier.")

    if "Banov" == recognized_name:
        robot_say("His name is Daniel Banovski and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a student in the Technion University.")

    if "Bremer" == recognized_name:
        robot_say("Her name is Adi Bremer and she is " + str(year - 2002) + " years old.")
        robot_say("These days she works as a soldier.")

    if "Dolev" == recognized_name:
        robot_say("His name is Dolev fishman and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Elad" == recognized_name:
        robot_say("His name is Elad Mani and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Idan" == recognized_name:
        robot_say("His name is Idan Pogrevinski and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a soldier-student in the Technion University.")

    if "Ilan" == recognized_name:
        robot_say("His name is Ilan Gimelferb and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Matvey" == recognized_name:
        robot_say("His name is Matvey Oodler and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier")

    if "Lior" == recognized_name:
        robot_say("His name is Lior Raphael and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Maya" == recognized_name:
        robot_say("Her name is Maya Gaver and she is " + str(year - 2002) + " years old.")
        robot_say("These days she learns UI UX.")

    if "Ori" == recognized_name:
        robot_say("His name is Ori Anvar and he is " + str(year - 2002) + " years old.")
        robot_say("These days he is a soldier-student in the Technion University.")

    if "Zelig" == recognized_name:
        robot_say("His name is Daniel Zelig and he is " + str(year - 2002) + " years old.")
        robot_say("These days he works as a soldier.")

    if "Unknown" == recognized_name:
        robot_say("Sorry Sir, but this person does not appear in my database.")


def wikipediaSearch():
    try:
        search_subject = request.split("wikipedia")[1]
        robot_say("Searching in Wikipedia...")
        results = wikipedia.summary(request, sentences=3)
        robot_say(results)
    except:
        robot_say("There in no information about this person on the internet")


def openBrowser():
    get_website = request.split("open ")[1]
    website_name_path = get_website.replace(" ", "")
    url = website_name_path + ".com"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    print("Opening " + get_website + "...")
    webbrowser.get(chrome_path).open(url)


def openGmail():
    url = "https://mail.google.com/mail/u/0/?tab=rm#inbox"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    robot_say("Opening Email...")
    webbrowser.get(chrome_path).open(url)


def whatsApp():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])


def googleSearch():
    what_to_search = request.split("google")[1]
    url = 'https://www.google.com/search?q='
    search_url = url + what_to_search
    webbrowser.open(search_url)


def youtubeSearch():
    what_to_search = request.split("youtube")[1]
    url = 'https://www.youtube.com/results?search_query='
    search_url = url + what_to_search
    webbrowser.open(search_url)


def weatherSearch():
    what_to_search = request.split("in ")[1]
    city_name = what_to_search
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
        city_name) + "&appid=a19e10287fb85f419d1aeab1971019b0"
    results = requests.get(url.format(city_name))
    json = results.json()
    try:
        temp_kelvin = json['main']['temp']
        temp_celsuis = int(round(temp_kelvin - 273))
        weather = json['weather'][0]['description']
        pre_feels_like = json['main']['feels_like']
        feels_like = int(round(pre_feels_like - 273))
        pre_temp_min = json['main']['temp_min']
        temp_min = int(round(pre_temp_min - 273))
        pre_temp_max = json['main']['temp_max']
        temp_max = int(round(pre_temp_max - 273))
        humidity = json['main']['humidity']
    except:
        robot_say("I didn't get the city. please repeat the city name.")
        city_name = take_command()
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
            city_name) + "&appid=a19e10287fb85f419d1aeab1971019b0"
        results = requests.get(url.format(city_name))
        json = results.json()
        temp_kelvin = json['main']['temp']
        temp_celsuis = int(round(temp_kelvin - 273))
        weather = json['weather'][0]['description']
        pre_feels_like = json['main']['feels_like']
        feels_like = int(round(pre_feels_like - 273))
        pre_temp_min = json['main']['temp_min']
        temp_min = int(round(pre_temp_min - 273))
        pre_temp_max = json['main']['temp_max']
        temp_max = int(round(pre_temp_max - 273))
        humidity = json['main']['humidity']

    robot_say("The weather in " + str(city_name) + " is " + str(temp_celsuis) + " degrees with " +
              str(weather) + ".")
    if temp_min == temp_max:
        robot_say("The humidity there today is " + str(humidity) +
                  "% and it feels like " + str(feels_like) + ".")
    else:
        robot_say(
            "The humidity today is " + str(humidity) + "% and the weather will be between "
            + str(temp_min) + " and " + str(temp_max) + " degrees.")
    if feels_like < 20:
        robot_say("I recommend you to take a coat with you today Sir. "
                  "It feels like " + str(feels_like) + " degrees outside.")
    elif feels_like > 25:
        robot_say("I recommend you to take your sunglasses today Sir. "
                  "It is a sunny day and feels like " + str(feels_like) + " degrees outside.")
    else:
        robot_say("Have a nice day")

    url = 'https://www.google.com/search?newwindow=1&sxsrf=ALeKk02IyZcrkKFD0O1cJw7Zj-9ML0h6Wg%3A1605801036107&ei' \
          '=TJS2X_WRBo60gQai1rfYCQ&q=weather+ '
    search_url = url + what_to_search
    robot_say("Here is some more weather data I have found for" + str(city_name))
    webbrowser.open(search_url)


mappings = {"sendingMassage": sendingMassage,
            "watchMovie": watchMovie,
            "faceRecognition": faceRecognition,
            "wikipediaSearch": wikipediaSearch,
            "openBrowser": openBrowser,
            "openGmail": openGmail,
            "whatsApp": whatsApp,
            "googleSearch": googleSearch,
            "youtubeSearch": youtubeSearch,
            "weatherSearch": weatherSearch,
            "disneyRecommendation": disneyRecommendation,
            "marvelRecommendation": marvelRecommendation,
            "Alarm": Alarm,
            "personality": personality,
            "jokes": tellJokes}

assistant = GenericAssistant('new.json', mappings)
assistant.train_model()

while True:
    try:
        # request = take_command()
        request = input("You: ")
        respond = assistant.request(request)
        robot_say(respond)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
