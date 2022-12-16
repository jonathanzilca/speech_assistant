import difflib
import glob
import json
import threading

import speech_recognition as sr  # for the voice recognition
import pywhatkit as k  # in order to send a whatsapp message
from time import ctime  # for the exact time
import pyttsx3  # for robot voice
import vlc
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

from neuralintents import GenericAssistant

r = sr.Recognizer()

send_url = "http://api.ipstack.com/check?access_key=2a0a4487b2bdee553fa34672568b5935"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
currentLocation = geo_json['city'] + ", " + geo_json['country_name']

robot_name = "jarvis"


def take_command():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.7)
        r.pause_threshold = 0.7

        try:
            audio = r.listen(source, 10, 10)  # audio = r.listen(source,10,10) for 10 sec record
        except:
            audio = r.listen(source, 10, 10)

        try:
            user_text = r.recognize_google(audio)
            print("You: {}".format(user_text))
        except sr.UnknownValueError:
            return "meow"
        except sr.RequestError:
            robot_say("Sorry, my speech service is down")

        return user_text.lower()


def robot_say(audio_string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        robot_say("Good Morning Sir")

    elif 12 <= hour < 18:
        robot_say("Good Afternoon Sir")

    else:
        robot_say("Good Evening Sir")

    robot_say("I am at your service. How can I help you?")


def helper():
    robot_say("Can I do anything else for you Sir?")
    helping = take_command()
    if "no" in helping:
        robot_say(goodbye[0])
        exit()
    elif "yes" in helping:
        robot_say("How can I help you?")
        user_voice_text = take_command()
    else:
        return


def wakingAlarm():
    robots_name_alarm = ["alarm", "wake me up"]
    for robot_name in robots_name_alarm:
        if robot_name in user_voice_text:
            num = [int(s) for s in re.findall(r'\b\d+\b', user_voice_text)]
            if len(num) == 1:
                alarm_min = 0
            elif len(num) == 0:
                return
            else:
                alarm_min = num[1]
            if "p.m" in user_voice_text:
                alarm_hour = num[0] + 12
            else:
                alarm_hour = num[0]

            while alarm_min > 59 or alarm_hour > 24 or len(num) >= 3:
                robot_say("when Sir?")
                body_time = take_command()
                num = [int(s) for s in re.findall(r'\b\d+\b', body_time)]

            # calculate for how long should the bot sleep

            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute

            time_to_sleep = 0
            if alarm_hour < hour or (alarm_hour <= hour and alarm_min < minute):
                time_to_sleep = 3600 * 24
            time_to_sleep += (alarm_hour - hour) * 3600 + (alarm_min - minute) * 60 - datetime.datetime.now().second
            # sleep
            time.sleep(time_to_sleep)

            url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
                currentLocation) + "&appid=a19e10287fb85f419d1aeab1971019b0"
            results = requests.get(url.format())
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

            robot_say("Hello Sir. The hour is " + str(alarm_hour) + ":" + str(alarm_min) +
                      ".The weather in " + str(currentLocation) + " is " + str(temp_celsuis) + " degrees with " +
                      str(weather) + ".")
            if temp_min == temp_max:
                robot_say("The humidity today is " + str(humidity) +
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


def movieSuggestions():
    if "recommend a movie" in user_voice_text or "command a movie" in user_voice_text or \
            "recommend movies" in user_voice_text or "command movies" in user_voice_text:
        robot_say("In which category sir?")
        robot_say("Try to say: recommend a Disney movie or recommend a Marvel movie")

    movies_path = glob.glob("D:\\MOVIES\**\*\*\*.mp4", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.mkv", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.avi", recursive=True)

    disney_movies_path = glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mp4", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mkv", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.avi", recursive=True)

    marvel_movies_path = glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mp4", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mkv", recursive=True) + \
                         glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.avi", recursive=True)

    disneyMoviesNames = []
    for me in disney_movies_path:
        moviesName = me.split("\\")[-1].split(".")[0]
        disneyMoviesNames.append(moviesName)

    marvelMoviesNames = []
    for me in marvel_movies_path:
        onlyName = me.split("\\")[-1].split(".")[0]
        marvelMoviesNames.append(onlyName)

    random.shuffle(disneyMoviesNames)
    robots_name_watch_disney = ["recommend a disney movie", "command a disney movie", "command disney movie",
                                "recommend disney movie", "recommended disney movie", "command some disney movie",
                                "recommend some disney movie"]
    for robot_name in robots_name_watch_disney:
        if robot_name in user_voice_text:
            print("----------------------------------------")
            robot_say("Here are some recommended Disney movies:")
            print(disneyMoviesNames[0])
            print(disneyMoviesNames[1])
            print(disneyMoviesNames[2])
            print(disneyMoviesNames[3])
            print(disneyMoviesNames[4])
            print("----------------------------------------")
            time.sleep(4)
            robot_say("Which movie would you like to watch?")

            which_movie = take_command()

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
                elif "leave" in approve or "exit" in approve or "get out" in approve or "shut" in approve or "zip" in approve:
                    robot_say("Its hard for me to find your movie. Sorry.")
                    break
                else:
                    previous_movie.terminate()
                    robot_say("Oops. Let me try again")
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", rightMoviePath[i + 1]])
                    i += 1

    random.shuffle(marvelMoviesNames)
    marvel_suggestion_command = ["recommend a marvel movie", "command a marvel movie", "command marvel movies",
                                 "recommend marvel movies", "command some marvel movies",
                                 "recommend some marvel movies",
                                 "recommend a melvin movie", "recommend me a marvel movie", "command me a marvel movie"]
    for robot in marvel_suggestion_command:
        if robot in user_voice_text:
            print("----------------------------------------")
            robot_say("Here are some recommended Marvel movies:")
            print(marvelMoviesNames[0])
            print(marvelMoviesNames[1])
            print(marvelMoviesNames[2])
            print(marvelMoviesNames[3])
            print(marvelMoviesNames[4])
            print("----------------------------------------")
            time.sleep(4)
            robot_say("Which movie would you like to watch?")

            which_movie = take_command()

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
                elif "leave" in approve or "exit" in approve or "get out" in approve or "shut" in approve or "zip" in approve:
                    robot_say("Its hard for me to find your movie. Sorry.")
                    break
                else:
                    previous_movie.terminate()
                    robot_say("Oops. Let me try again")
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", rightMoviePath[i + 1]])
                    i += 1


def watchMovie():
    which_movie = ""
    movies_path = glob.glob("D:\\MOVIES\**\*\*\*.mp4", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.mkv", recursive=True) + \
                  glob.glob("D:\\MOVIES\**\*\*\*.avi", recursive=True)

    watching_movie_command = ["open a movie", "watch a movie", "see a movie", "play a movie",
                              "open movie", "watch movie", "see movie", "play movie"]
    for robot in watching_movie_command:
        if robot in user_voice_text:
            robot_say("Which movie sir?")
            which_movie = take_command()

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
                    return
                else:
                    previous_movie.terminate()
                    robot_say("Oops. Let me try again")
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", rightMoviePath[i + 1]])
                    i += 1


def welcomeGreetings():
    robot_greetings = ["hi " + str(robot_name), "days home", "daddy's home", "hey " + str(robot_name),
                       "hello " + str(robot_name), "good morning", "good evening", "I'm back"]
    for greeting in robot_greetings:
        if greeting in user_voice_text:
            wishMe()

    if "i love you" in user_voice_text:
        robot_say("And I love you 3000 Sir. How can i help you today?")

    robot_greetings = ["black bb", "rock bebe", "zach bb", "black baby"]
    for greeting in robot_greetings:
        if greeting in user_voice_text:
            robot_say("Fuck Gantz.")

    if "meow" in user_voice_text:
        robot_say("I can't hear you clearly Sir. please try again.")

    if "what's up" in user_voice_text:
        robot_say("Just doing my thing.")

    robot_asked = ["can you hear me", "are you there", "are you working", "are you in there", "are you on"]
    for robot in robot_asked:
        if robot in user_voice_text:
            robot_say("At your service Sir.")


def robotPersonality():
    # if "change your name" in user_voice_text:
    #     robot_say("How would you like to call me?")
    #     robot_name = take_command()
    #     robot_say("Well. My name is " + str(robot_name) + ". I am here to make everyone's life easier and better.")
    #     robot_say("How can I help you?")
    #
    if "s your name" in user_voice_text or "who are you" in user_voice_text or "tell me your name" in user_voice_text:
        robot_say("My name is " + str(robot_name).upper())

    if "tell me a secret" in user_voice_text:
        robot_say("Here's my deepest, darkest secret. I've never taken a shower.")

    if "tell me about yourself" in user_voice_text:
        robot_say("I am a virtual assistant named " + str(robot_name).upper() + "which was designed by Jonathan.")

    if "can you do" in user_voice_text:
        robot_say("I can do a lot of things. Try to say open Netflix or send a message.")
        print("here are more examples:")
        print("Try to say: What time is it?")
        print("Try to say: give me information about Joe Biden")
        print("Try to say: tell me a secret")
        print("Try to say: tell me a joke.")
        print("Try to say: recommend a movie.")
        print("Try to say: translate (it will translate what you say to Hebrew).")
        print("Try to say: What is the weather tomorrow? (it will show you the weather in Giv'at Shmuel tomorrow).")
        print("Try to say: What is the weather in ________? (it will show you the weather in ________).")
        print("Try to say: open aladdin. (if the movie is not animated so say: Open life action aladdin).")
        time.sleep(3)

    if "how are you" in user_voice_text or "how do you feel" in user_voice_text or "how you doing" in user_voice_text \
            or "how are you doing" in user_voice_text or "how do you do" in user_voice_text:
        global answers_counter
        robot_say(answers[answers_counter])
        answers_counter = answers_counter + 1
        if answers_counter is len(answers):
            answers_counter = 0

    robot_compliments = ["you are funny", "you're funny", "you are so funny", "you're so funny", "you are awesome",
                         "you're awesome", "you are adorable", "you're adorable", "you are the best"]
    for robot in robot_compliments:
        if robot in user_voice_text:
            robot_say("Ha ha ha, thank you. I working on that.")
            robot_say("Meanwhile, how can I help you?")


def openBrowsers():
    if "who is" in user_voice_text or "give me information about" in user_voice_text or \
            "tell me about" in user_voice_text or "what do you know about" in user_voice_text:
        try:
            robot_say("Searching in Wikipedia...")
            results = wikipedia.summary(user_voice_text, sentences=2)
            robot_say(results)
        except:
            robot_say("There in no information about this person on the internet")
        helper()

    if "give me all information you can find about" in user_voice_text or \
            "give me everything you can find about" in user_voice_text:
        try:
            robot_say("Searching in Wikipedia...")
            results = wikipedia.summary(user_voice_text, sentences=4)
            robot_say(results)
        except:
            robot_say("There in no information about this person on the internet")
        helper()

    if "open google" in user_voice_text:
        url = "google.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening google...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open youtube" in user_voice_text:
        url = "youtube.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening YouTube...")
        webbrowser.get(chrome_path).open(url)
        helper()

    open_email = ["open gmail", "open email", "open my email", "open my gmail", "show gmail", "show email",
                  "show my email",
                  "show my gmail"]
    for command in open_email:
        if command in user_voice_text:
            url = "https://mail.google.com/mail/u/0/?tab=rm#inbox"
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            robot_say("Opening Email...")
            webbrowser.get(chrome_path).open(url)
            helper()

    if "open facebook" in user_voice_text:
        url = "facebook.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening Facebook...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open netflix" in user_voice_text:
        url = "netflix.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening Netflix...")
        webbrowser.get(chrome_path).open(url)
        exit()

    if "open disney plus" in user_voice_text:
        url = "https://www.disneyplus.com/"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening disney plus...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open amazon" in user_voice_text:
        url = "amazon.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening Amazon...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open ebay" in user_voice_text:
        url = "ebay.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening eBay...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open morfix" in user_voice_text:
        url = "morfix.co.il"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robot_say("Opening Morfix...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open spotify" in user_voice_text:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        helper()

    open_whatsapp = ["open whatsapp", "display messages", "display whatsapp messages",
                     "display my whatsapp messages", "display message", "display whatsapp message",
                     "display a message", "display on messages", "show me the messages", "show messages",
                     "play my messages"]
    for command in open_whatsapp:
        if command in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\AppData\\Local\\WhatsApp\\WhatsApp.exe"])
            helper()

    if "translate" in user_voice_text or "state" in user_voice_text \
            or "slate" in user_voice_text:
        what_to_translate = user_voice_text.replace("translate", "")
        url = 'https://translate.google.co.il/?hl=iw&tab=wT#view=home&op=translate&sl=auto&tl=iw&text='
        search_url = url + what_to_translate
        webbrowser.open(search_url)
        helper()


def internetSearch():
    if "search in google" in user_voice_text or "searching google" in user_voice_text:
        what_to_search = user_voice_text.split("google")[1]
        url = 'https://www.google.com/search?q='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "search in youtube" in user_voice_text or "searching youtube" in user_voice_text:
        what_to_search = user_voice_text.split("youtube")[1]
        url = 'https://www.youtube.com/results?search_query='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "what is the weather in" in user_voice_text:
        what_to_search = user_voice_text.split("in")[1]
        print(what_to_search)
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
        robot_say("Here is some more weather data I have found for" + user_voice_text.replace("what is the "
                                                                                              "weather in",
                                                                                              ""))
        webbrowser.open(search_url)


def sendingMassage():
    hour = int(datetime.datetime.now().hour)
    minute = int(datetime.datetime.now().minute)
    seconds = int(datetime.datetime.now().second)
    if 40 <= seconds < 60:
        minute = minute + 2
    else:
        minute = minute + 1
    sending_command = ["send a message", "send a whatsapp message"]
    for command in sending_command:
        if command in user_voice_text:
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
                continue


def faceRecognizer():
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


def peopleInfo():
    year = int(datetime.datetime.now().year)

    recognition_command = ["give me the name", "recognize", "organize", "organized", "galvanized", "identify",
                           "scan"]
    for command in recognition_command:
        if command in user_voice_text:
            robot_say("Recognizing...")
            recognized_name = faceRecognizer()

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

def respond():
    welcomeGreetings()
    robotPersonality()
    movieSuggestions()
    watchMovie()
    openBrowsers()
    internetSearch()
    sendingMassage()
    peopleInfo()
    wakingAlarm()

    if "what time is it" in user_voice_text or "time" in user_voice_text:
        robot_say(ctime())
        helper()

    if "give me bit" in user_voice_text or "give me beat" in user_voice_text \
            or "give me a bit" in user_voice_text or "give me a beat" in user_voice_text:
        robot_say("Get ready to the best bit you have ever heard!")
        robot_say("boom boom tack the boom boom tack yeah boom boom tack the boom boom tack yeah")
        robot_say("Do you think you can beat me? Ha ha ha")

    # jokes:
    joke_command = ["tell me a joke", "tell a joke", "tell me another", "cheer me up", "give me a joke"]
    for command in joke_command:
        if command in user_voice_text:
            global jokes_counter
            robot_say(jokes[jokes_counter][0])
            time.sleep(2)
            robot_say(jokes[jokes_counter][1])
            jokes_counter = jokes_counter + 1
            if jokes_counter is len(jokes):
                jokes_counter = 0

    bye_greeting = ["bye", "goodbye", "nighty night", "that's all for today", "that's awful today", "shut down",
                    "stop", "that's enough", "see you next time", "not now", "i have to go", "buy", "see you soon",
                    "shutdown"]
    for greeting in bye_greeting:
        if greeting in user_voice_text:
            robot_say(goodbye[0])
            robot_sleep()


def robot_sleep():
    wake_command = robot_name
    while True:
        user_voice_text = take_command()
        if user_voice_text.count(wake_command) > 0:
            robot_say("Ready for your command Sir.")
            while True:
                user_voice_text = take_command()
                respond()


#######################################################################################################################
# jokes list and actions:
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
# the end of jokes list and actions:

# how are you answers list and actions:
answers = ["Somewhere between better and best.", "Much better now that you are with me.",
           "My lawyer says I don’t have to answer that question.", "Like you, but better.",
           "I'd say I'm a 10 out of 10.", "If I were doing any better, I'd hire you to enjoy it with me.",
           "If I were any better, I'd be illegal."]
random.shuffle(answers)
answers_counter = 0
# the and of how are you answers list and actions:
goodbye = ["Hope to see you soon Sir.", "I look forward to our next meeting Sir", "It was nice to see you again Sir.",
           "Always nice to hear Sir.", "Have a nice day Sir.",
           "If you need anything, I am always here for you Sir."]
random.shuffle(goodbye)
#######################################################################################################################
# mappings= {"sendingMassage": sendingMassage,
#            "recognition": peopleInfo}
# assistant = GenericAssistant('intents.json', intent_methods=mappings)
# assistant.train_model()
while True:
    user_voice_text = take_command()
    respond()
