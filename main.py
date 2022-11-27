import speech_recognition as sr  # for the voice recognition
import pywhatkit as k  # in order to send a whatsapp message
from time import ctime  # for the exact time
# import playsound  # for friday (for now it is not in use)
import pyttsx3  # for jarvis voice
# from gtts import gTTS  # for friday (for now it is not in use)
import wikipedia  # to use wikipedia through JARVIS
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
from multiprocessing import Process

r = sr.Recognizer()


def record_audio():
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
            robots_name_system("Sorry, my speech service is down")

        return user_text.lower()


# def friday_system(audio_string):
#     tts = gTTS(text=audio_string, lang="en")
#     audio_file = "audio-99999.mp3"
#     tts.save(audio_file)
#     playsound.playsound(audio_file)
#     print(audio_string)
#     os.remove(audio_file)


def robots_name_system(audio_string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        robots_name_system("Good Morning Sir. Nice to see you again.")

    elif 12 <= hour < 18:
        robots_name_system("Good Afternoon Sir. Nice to see you again.")

    else:
        robots_name_system("Good Evening Sir. Nice to see you again.")

    robots_name_system("I am at your service. How can I help you?")


def helper():
    robots_name_system("Can I do anything else for you Sir?")
    helping = record_audio()
    if "no" in helping:
        robots_name_system(goodbye[0])
        exit()
    elif "yes" in helping:
        robots_name_system("How can I help you?")
        user_voice_text = record_audio()
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
                robots_name_system("when Sir?")
                body_time = record_audio()
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

            city_name = str("Giv'at Shmuel")
            url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
                city_name) + "&appid=a19e10287fb85f419d1aeab1971019b0"
            results = requests.get(url.format())
            json = results.json()
            # city = json['name']
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

            robots_name_system("Hello Sir. The hour is " + str(alarm_hour) + ":" + str(alarm_min) +
                               ".The weather in Giv'at Shmuel is " + str(temp_celsuis) + " degrees with " +
                               str(weather) + ".")
            if temp_min == temp_max:
                robots_name_system("The humidity today is " + str(humidity) +
                                   "% and it feels like " + str(feels_like) + ".")
            else:
                robots_name_system(
                    "The humidity today is " + str(humidity) + "% and the weather will be between "
                    + str(temp_min) + " and " + str(temp_max) + " degrees.")
            if feels_like < 20:
                robots_name_system("I recommend you to take a coat with you today Sir. "
                                   "It feels like " + str(feels_like) + " degrees outside.")
            elif feels_like > 25:
                robots_name_system("I recommend you to take your sunglasses today Sir. "
                                   "It is a sunny day and feels like " + str(feels_like) + " degrees outside.")
            else:
                robots_name_system("Have a nice day")


def movieSuggestions():
    if "recommend a movie" in user_voice_text or "command a movie" in user_voice_text or \
            "recommend movies" in user_voice_text or "command movies" in user_voice_text:
        robots_name_system("In which category sir?")
        robots_name_system("Try to say: recommend a Disney movie or recommend a Marvel movie")

    robots_name_ending = ["i want to watch a movie", "i want to see a movie", "what movie should i watch",
                          "which movie should i watch", "i don't know what to watch",
                          "i don't know which movie should i watch", "recommend me a movie"]
    for robot_name in robots_name_ending:
        if robot_name in user_voice_text:
            robots_name_system("If you want, you can ask me to recommend a movie.")
            robots_name_system("Try to say: recommend a Disney movie or recommend a Marvel movie")

    diseny_suggestions = ["6 Big Heroes", "101 Dalmatians", "101 Dalmatians 2 - London Adventure", "A Goofy Movie",
                          "Aladdin", "Life Action Aladdin", "Alice In Wonderland", "Life Action Alice In Wonderland 1",
                          "Life Action Alice In Wonderland 2: Through The Looking Glass", "Anastasia",
                          "Atlantis: The Lost Empire", "Bambi", "Bolt", "Brave", "Brother Bear 1", "Brother Bear 2",
                          "Cars 1", "Cars 2", "Cars 3", "Cinderella", "Coco", "Despicable Me 1", "Despicable Me 2",
                          "Despicable Me 3", "Dumbo", "Life Action Dumbo", "Frozen 1", "Frozen 2", "Hercules",
                          "How to Train Your Dragon 1", "How to Train Your Dragon 2",
                          "How to Train Your Dragon 3: The Hidden World", "Ice Age 1", "Ice Age 2: The Meltdown",
                          "Ice Age 3: Dawn of the Dinosaurs", "Ice Age 4: Continental Drift",
                          "Ice Age 5: Collision Course", "Inside Out", "Kung Fu Panda 1", "Kung Fu Panda 2",
                          "Kung Fu Panda 3", "Lady and the Tramp", "Lilo and Stitch 1",
                          "Lilo And Stitch 2: Stitch Has a Glitch", "Madagascar 1", "Madagascar 2: Escape to Africa",
                          "Madagascar 3: Europe's Most Wanted", "Mary Poppins", "Moana", "Monsters Inc",
                          "Monsters University", "Mulan 1", "Mulan 2", "Life Action Mulan", "Over the Hedge",
                          "Peter Pan 1", "Peter Pan 2: Return To Neverland", "Pinocchio (1940)", "Pocahontas 1",
                          "Pocahontas 2: Journey to a New World", "Puss In Boots", "Ratatouille", "Rio 1", "Rio 2",
                          "Rise of the Guardians", "Robin Hood", "Life Action Robin Hood", "Shark Tale", "shrek 1",
                          "shrek 2", "shrek 3", "shrek 4", "Sinbad: Legend of the Seven Seas", "Sing", "Up",
                          "Sleeping Beauty", "Snow White and the Seven Dwarfs", "Space Jam", "Tangled", "Tarzan",
                          "Spirit Stallion of the Cimarron", "The Aristocats", "The Beauty And The Beast", "Zootopia",
                          "The Boss Baby", "The Cat in the Hat", "The Hunchback Of Notre Dame", "The Incredibles 1",
                          "The Incredibles 2", "The Jungle Book 1", "The Jungle Book 2", "Life Action Jungle Book",
                          "The Lion King 1", "The Lion King 2", "The Lion King 3", "Life Action Lion King",
                          "The Little Mermaid", "The Little Mermaid 2: Return to the Sea", "The Sword in the Stone",
                          "The Little Mermaid 3: Ariel's Beginning", "The Princess And The Frog", "Toy Story 1",
                          "The Road to El Dorado", "Treasure Planet", "Wreck-It Ralph 2: Ralph Breaks the Internet",
                          "Wreck-It Ralph 1", "Toy Story 2", "Toy Story 3", "Toy Story 4"]
    random.shuffle(diseny_suggestions)
    robots_name_watch_disney = ["recommend a disney movie", "command a disney movie", "command disney movies",
                                "recommend disney movies", "command some disney movies", "recommend some disney movies"]
    for robot_name in robots_name_watch_disney:
        if robot_name in user_voice_text:
            print("----------------------------------------")
            robots_name_system("Here are some recommended Disney movies:")
            print(diseny_suggestions[0])
            print(diseny_suggestions[1])
            print(diseny_suggestions[2])
            print(diseny_suggestions[3])
            print(diseny_suggestions[4])
            print("----------------------------------------")
            time.sleep(4)
            print("If you want to watch a movie just say: Open _______")
            robots_name_system("Which movie would you like to watch?")

    marvel_suggestions = ["Ant-Man 1", "Ant-Man 2: Ant-Man And The Wasp", "Aquaman", "Avengers Age of Ultron",
                          "Avengers Endgame", "Avengers Infinity War", "The Avengers 1", "Black Panther",
                          "Captain America 1: The First Avenger", "Captain America 2: The Winter Soldier", "Iron Man 3",
                          "Captain America 3: Civil War", "Captain Marvel", "Deadpool 1", "Deadpool 2", "Iron Man 1",
                          "Doctor Strange", "Guardians of the Galaxy 1", "Guardians of the Galaxy Vol. 2", "Iron Man 2",
                          "Spider-Man 2: Far from Home", "Spider-Man 1: Homecoming", "The Incredible Hulk", "Thor 1",
                          "Thor 2: The Dark World", "Thor 3: Ragnarok", "Venom"]
    random.shuffle(marvel_suggestions)
    jarvis_watch_marvel = ["recommend a marvel movie", "command a marvel movie", "command marvel movies",
                           "recommend marvel movies", "command some marvel movies", "recommend some marvel movies",
                           "recommend a melvin movie", "recommend me a marvel movie", "command me a marvel movie"]
    for robot_name in jarvis_watch_marvel:
        if robot_name in user_voice_text:
            print("----------------------------------------")
            robots_name_system("Here are some recommended Marvel movies:")
            print(marvel_suggestions[0])
            print(marvel_suggestions[1])
            print(marvel_suggestions[2])
            print(marvel_suggestions[3])
            print(marvel_suggestions[4])
            print("----------------------------------------")
            time.sleep(4)
            print("If you want to watch a movie just say: Open _______")
            robots_name_system("Which movie would you like to watch?")


def disneyOpener():
    jarvis_6_big_heroes = ["open 6 big heroes", "watch 6 big heroes", "see 6 big heroes", "play 6 big heroes",
                           "open six big heroes", "watch six big heroes", "see six big heroes", "play six big heroes",
                           "open 6 big hills", "watch 6 big hills", "see 6 big hills", "play 6 big hills",
                           "open six big hills", "watch six big hills", "see six big hills", "play six big hills"]
    for jarvis in jarvis_6_big_heroes:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\6 Big Heros (2014)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_101_dalmatians = ["open 101 dalmatians", "watch 101 dalmatians", "see 101 dalmatians",
                             "open one hundred and one dalmatians", "watch one hundred and one dalmatians",
                             "see one hundred and one dalmatians"]
    for jarvis in jarvis_101_dalmatians:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            choosing_movie = {
                "1": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "one": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "first": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "the first": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "2": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "two": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "too": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "the second": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
                "second": "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\One Hundred and One Dalmatians (1961)",
            }
            number_movie = choosing_movie.get(which_movie)
            while number_movie is None:
                robots_name_system("Please say again.")
                which_movie = record_audio()
                number_movie = choosing_movie.get(which_movie)
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              number_movie])
            robots_name_system("Enjoy the movie sir")
            exit()

            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\101 Dalmatians Movies\\101 Dalmatians 2 - London Adventure (2003)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_goofy_movie = ["open goofy movie", "watch goofy movie", "see goofy movie"]
    for jarvis in jarvis_goofy_movie:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\A Goofy Movie (1995)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_aladdin = ["open aladdin", "watch aladdin", "see aladdin", "open aladin", "watch aladin", "see aladin"]
    for jarvis in jarvis_aladdin:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            choosing_movie = {
                "original": "D:\\MOVIES\\Diseny movies\\Aladdin- animated and unanimated\\Aladdin (1992)",
                "life action": "D:\\MOVIES\\Diseny movies\\Aladdin- animated and unanimated\\Aladdin (2019)",
                "the original": "D:\\MOVIES\\Diseny movies\\Aladdin- animated and unanimated\\Aladdin (1992)",
                "the life action": "D:\\MOVIES\\Diseny movies\\Aladdin- animated and unanimated\\Aladdin (2019)"
            }
            number_movie = choosing_movie.get(which_movie)
            while number_movie is None:
                robots_name_system("Please say again.")
                which_movie = record_audio()
                number_movie = choosing_movie.get(which_movie)
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              number_movie])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_alice_in_wonderland = ["open alice in wonderland", "watch alice in wonderland", "see alice in wonderland"]
    for jarvis in jarvis_alice_in_wonderland:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "original" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Alice In Wonderland movies - animated and "
                                  "unanimated\\Alice in Wonderland (1951)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "life action" in which_movie:
                robots_name_system("1 or 2?")
                which_movie_1 = record_audio()
                if "1" in which_movie_1 or "one" in which_movie_1 or "first" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\Alice In Wonderland movies - animated and unanimated"
                                      "\\Alice In Wonderland movies (1+2) - unanimated\\Alice In Wonderland (1)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "2" in which_movie_1 or "two" in which_movie_1 or "too" in which_movie_1 \
                        or "second" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\Alice In Wonderland movies - animated and "
                                      "unanimated\\Alice In Wonderland movies (1+2) - unanimated\\Alice "
                                      "Trought The Looking glass(2)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()

    jarvis_anastasia = ["open anastasia", "watch anastasia", "see anastasia",
                        "open stassia", "watch stassia", "see stassia",
                        "open anesthesia", "watch anesthesia", "see anesthesia"]
    for jarvis in jarvis_anastasia:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Anastasia (1997)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_atlantis = ["open atlantis", "watch atlantis", "see atlantis"]
    for jarvis in jarvis_atlantis:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Atlantis The Lost Empire (2001)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_bambi = ["open bambi", "watch bambi", "see bambi"]
    for jarvis in jarvis_bambi:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Bambi (1942)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_bolt = ["open bolt", "watch bolt", "see bolt"]
    for jarvis in jarvis_bolt:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Bolt (2008)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_brave = ["open brave", "watch brave", "see brave"]
    for jarvis in jarvis_brave:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Brave (2012)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_brother_bear = ["open brother bear", "watch brother bear", "see brother bear"]
    for jarvis in jarvis_brother_bear:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Brother Bear Movies\\Brother Bear (2003)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Brother Bear Movies\\Brother Bear 2 (2006)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_cars = ["open cars", "watch cars", "see cars"]
    for jarvis in jarvis_cars:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Cars Movies\\Cars (2006)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Cars Movies\\Cars 2 (2011)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Cars Movies\\Cars 3 (2017)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_cinderella = ["open cinderella", "watch cinderella", "see cinderella"]
    for jarvis in jarvis_cinderella:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Cinderella (1950)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_coco = ["open coco", "watch coco", "see coco"]
    for jarvis in jarvis_coco:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Coco (2017)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_despicable_me = ["open despicable me", "watch despicable me", "see despicable me",
                            "open bubble me", "watch bubble me", "see bubble me"]
    for jarvis in jarvis_despicable_me:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Despicable Me Movies\\Despicable Me (2010)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Despicable Me Movies\\Despicable Me 2 (2013)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Despicable Me Movies\\Despicable Me 3 (2017)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_dumbo = ["open dumbo", "watch dumbo", "see dumbo"]
    for jarvis in jarvis_dumbo:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "original" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Dumbo movies - animated and unanimated\\Dumbo (1941)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "life action" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Dumbo movies - animated and unanimated\\Dumbo (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_frozen = ["open frozen", "watch frozen", "see frozen"]
    for jarvis in jarvis_frozen:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Frozen Movies\\Frozen (2013)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Frozen Movies\\Frozen II (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_hercules = ["open hercules", "watch hercules", "see hercules",
                       "open oculus", "watch oculus", "see oculus",
                       "open herculis", "watch herculis", "see herculis"]
    for jarvis in jarvis_hercules:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Hercules (1997)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_how_to_train_your_dragon = ["open how to train your dragon", "watch how to train your dragon",
                                       "see how to train your dragon"]
    for jarvis in jarvis_how_to_train_your_dragon:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\How to Train Your Dragon Movies\\"
                                  "How to Train Your Dragon (2010)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\How to Train Your Dragon Movies\\"
                                  "how to train your dragon 2  (2014)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\How to Train Your Dragon Movies\\"
                                  "how to train your dragon 3 - the hidden world (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_ice_age = ["open ice age", "watch ice age", "see ice age"]
    for jarvis in jarvis_ice_age:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2, 3, 4 or 5?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age (2002)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age 2 - The Meltdown (2006)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\"
                                  "Ice Age 3 - Dawn of the Dinosaurs (2009)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "4" in which_movie or "four" in which_movie or "for" in which_movie or "fourth" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age 4 -Continental Drift (2012)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "5" in which_movie or "five" in which_movie or "fifth" in which_movie or "v" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age 5 - Collision Course (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_inside_out = ["open inside out", "watch inside out", "see inside out"]
    for jarvis in jarvis_inside_out:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Inside Out (2015)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_kung_fu_panda = ["open kung fu panda", "watch kung fu panda", "see kung fu panda"]
    for jarvis in jarvis_kung_fu_panda:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Kung Fu Panda Movie\\Kung Fu Panda (2008)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Kung Fu Panda Movie\\Kung Fu Panda 2 (2011)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Kung Fu Panda Movie\\Kung Fu Panda 3 (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_lady_and_the_tramp = ["open lady and the tramp", "watch lady and the tramp", "see lady and the tramp"]
    for jarvis in jarvis_lady_and_the_tramp:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Lady and the Tramp (1955)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_lilo_and_stitch = ["open lilo & stitch", "watch lilo & stitch", "see lilo & stitch",
                              "open lilo and stitch", "watch lilo and stitch", "see lilo and stitch"]
    for jarvis in jarvis_lilo_and_stitch:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Lilo and Stitch Movies\\Lilo and Stitch (2002)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Lilo and Stitch Movies\\Lilo And Stitch 2 - "
                                  "Stitch Has a Glitch (2005)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_madagascar = ["open madagascar", "watch madagascar", "see madagascar"]
    for jarvis in jarvis_madagascar:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Madagascar Movies\\Madagascar (2005)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Madagascar Movies\\Madagascar 2 Escape 2 Africa (2008)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Madagascar Movies\\Madagascar 3 - "
                                  "Europe's Most Wanted (2012)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_mary_poppins = ["open mary poppins", "watch mary poppins", "see mary poppins"]
    for jarvis in jarvis_mary_poppins:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Mary Poppins (1964)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_moana = ["open moana", "watch moana", "see moana"]
    for jarvis in jarvis_moana:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\moana (2016)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_monsters_inc = ["open monsters inc", "watch monsters inc", "see monsters inc"]
    for jarvis in jarvis_monsters_inc:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? original or Monsters University?")
            which_movie = record_audio()
            if "original" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Monsters Inc Movies\\Monsters Inc (2001)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "monsters university" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Monsters Inc Movies\\Monsters University (2013)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_mulan = ["open mulan", "watch mulan", "see mulan"]
    for jarvis in jarvis_mulan:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "original" in which_movie:
                robots_name_system("1 or 2?")
                which_movie_1 = record_audio()
                if "1" in which_movie_1 or "one" in which_movie_1 or "first" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\Mulan Movies\\Mulan (1998)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "2" in which_movie_1 or "two" in which_movie_1 or "too" in which_movie_1 \
                        or "second" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\Mulan Movies\\Mulan 2 (2004)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
            if "life action" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Mulan Movies\\Mulan (2020)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_over_the_hedge = ["open over the hedge", "watch over the hedge", "see over the hedge"]
    for jarvis in jarvis_over_the_hedge:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Over the Hedge (2006)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_peter_pan = ["open peter pan", "watch peter pan", "see peter pan"]
    for jarvis in jarvis_peter_pan:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Peter Pan Movies\\Peter Pan (1953)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Peter Pan Movies\\Peter Pan"
                                  " II Return To Neverland (2002)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_pinocchio = ["open pinocchio", "watch pinocchio", "see pinocchio"]
    for jarvis in jarvis_pinocchio:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Pinocchio (1940)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_pocahontas = ["open pocahontas", "watch pocahontas", "see pocahontas"]
    for jarvis in jarvis_pocahontas:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Pocahontas Movies\\Pocahontas (1995)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Pocahontas Movies\\Pocahontas 2 - "
                                  "Journey to a New World (1998)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_puss_in_boots = ["open puss in boots", "watch puss in boots", "see puss in boots"]
    for jarvis in jarvis_puss_in_boots:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Puss In Boots (2011)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_ratatouille = ["open ratatouille", "watch ratatouille", "see ratatouille"]
    for jarvis in jarvis_ratatouille:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Ratatouille (2007)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_rio = ["open rio", "watch rio", "see rio",
                  "open leo", "watch leo", "see leo",
                  "open reel", "watch reel", "see reel"]
    for jarvis in jarvis_rio:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Rio Movies\\Rio (2011)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Rio Movies\\Rio 2 (2014)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_rise_of_the_guardians = ["open rise of the guardians", "watch rise of the guardians",
                                    "see rise of the guardians"]
    for jarvis in jarvis_rise_of_the_guardians:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Rise of the Guardians (2012)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_robin_hood = ["open robin hood", "watch robin hood", "see robin hood"]
    for jarvis in jarvis_robin_hood:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "original" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Robin Hood movies\\Robin Hood (1973)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "life action" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Robin Hood movies\\Robin Hood (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_shark_tale = ["open shark tail", "watch shark tail", "see shark tail",
                         "open shark tale", "watch shark tale", "see shark tale"]
    for jarvis in jarvis_shark_tale:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Shark Tale (2004)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_shrek = ["open shrek", "watch shrek", "see shrek"]
    for jarvis in jarvis_shrek:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2, 3 or 4?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Shrek Movies\\Shrek (2001)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Shrek Movies\\Shrek 2 (2004)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Shrek Movies\\Shrek 3 (2007)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "4" in which_movie or "four" in which_movie or "for" in which_movie or "fourth" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Shrek Movies\\Shrek 4 (2010)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_sinbad = ["open sinbad", "watch sinbad", "see sinbad"]
    for jarvis in jarvis_sinbad:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Sinbad Legend of the Seven Seas (2003)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_sing = ["open sing", "watch sing", "see sing"]
    for jarvis in jarvis_sing:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\sing (2016)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_sleeping_beauty = ["open sleeping beauty", "watch sleeping beauty", "see sleeping beauty"]
    for jarvis in jarvis_sleeping_beauty:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Sleeping Beauty (1959)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_snow_white = ["open snow white", "watch snow white", "see snow white"]
    for jarvis in jarvis_snow_white:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Snow White and the Seven Dwarfs (1937)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_space_jam = ["open space jam", "watch space jam", "see space jam",
                        "open space jim", "watch space jim", "see space jim",
                        "open space gym", "watch space gym", "see space gym"]
    for jarvis in jarvis_space_jam:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Space Jam (1996)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_spirit = ["open spirit", "watch spirit", "see spirit"]
    for jarvis in jarvis_spirit:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Spirit Stallion of the Cimarron (2002)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_tangled = ["open plonter", "watch plonter", "see plonter",
                      "open planter", "watch planter", "see planter",
                      "open rapunzel", "watch rapunzel", "see rapunzel",
                      "open tangled", "watch tangled", "see tangled",
                      "open blonde tail", "watch blonde tail", "see blonde tail",
                      "open a punzel", "watch a punzel", "see a punzel"]
    for jarvis in jarvis_tangled:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Tangled (2010)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_tarzan = ["open tarzan", "watch tarzan", "see tarzan"]
    for jarvis in jarvis_tarzan:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Tarzan (1999)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_aristocats = ["open aristocats", "watch aristocats", "see aristocats"]
    for jarvis in jarvis_aristocats:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The AristoCats (1970)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_beauty_and_the_beast = ["open the beauty and the beast", "watch the beauty and the beast",
                                       "see the beauty and the beast", "open beauty and the beast",
                                       "watch beauty and the beast", "see beauty and the beast"]
    for jarvis in jarvis_the_beauty_and_the_beast:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Beauty And The Beast (1991)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_boss_baby = ["open boss baby", "watch boss baby", "see boss baby",
                        "open baby boss", "watch baby boss", "see baby boss"]
    for jarvis in jarvis_boss_baby:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Boss Baby (2017)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_cat_in_the_hat = ["open the cat in the hat", "watch the cat in the hat", "see the cat in the hat",
                                 "open cat in the hat", "watch cat in the hat", "see cat in the hat"]
    for jarvis in jarvis_the_cat_in_the_hat:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Cat in the Hat (2003)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_hunchback_of_notre_dame = ["open the hunchback of notre dame", "watch the hunchback of notre dame",
                                          "see the hunchback of notre dame", "open hunchback of notre dame",
                                          "watch hunchback of notre dame", "see hunchback of notre dame"]
    for jarvis in jarvis_the_hunchback_of_notre_dame:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Hunchback Of Notre Dame (1996)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_incredibles = ["open incredibles", "watch incredibles", "see incredibles",
                              "open the incredibles", "watch the incredibles", "see the incredibles"]
    for jarvis in jarvis_the_incredibles:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Incredibles movies\\The Incredibles (2004)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Incredibles movies\\The Incredibles 2 (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_the_jungle_book = ["open jungle book", "watch jungle book", "see jungle book",
                              "open the jungle book", "watch the jungle book", "see the jungle book"]
    for jarvis in jarvis_the_jungle_book:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "life action" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Jungle Book Movies - animated and unanimated\\"
                                  "The Jungle Book (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "original" in which_movie:
                robots_name_system("1 or 2?")
                which_movie_1 = record_audio()
                if "1" in which_movie_1 or "one" in which_movie_1 or "first" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\The Jungle Book Movies - animated and unanimated\\"
                                      "The Jungle Book (1967)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "2" in which_movie_1 or "two" in which_movie_1 or "too" in which_movie_1 \
                        or "second" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\The Jungle Book Movies - animated and unanimated\\"
                                      "The Jungle Book 2 (2003)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()

    jarvis_the_lion_king = ["open lion king", "watch lion king", "see lion king",
                            "open the lion king", "watch the lion king", "see the lion king"]
    for jarvis in jarvis_the_lion_king:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? The original or the life action?")
            which_movie = record_audio()
            if "life action" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Lion King movies - animated and unanimated\\"
                                  "The Lion King (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "original" in which_movie:
                robots_name_system("1, 2 or 3?")
                which_movie_1 = record_audio()
                if "1" in which_movie_1 or "one" in which_movie_1 or "first" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\The Lion King movies - animated and unanimated\\"
                                      "The Lion King (1994)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "2" in which_movie_1 or "two" in which_movie_1 or "too" in which_movie_1 \
                        or "second" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\The Lion King movies - animated and unanimated\\"
                                      "The Lion King 2 - Simba's Pride (1998)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "3" in which_movie_1 or "three" in which_movie_1 or "tree" in which_movie_1 \
                        or "third" in which_movie_1:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Diseny movies\\The Lion King movies - animated and unanimated\\"
                                      "The Lion King 1½ (2004)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()

    jarvis_the_little_mermaid = ["open little mermaid", "watch little mermaid", "see little mermaid",
                                 "open the little mermaid", "watch the little mermaid", "see the little mermaid"]
    for jarvis in jarvis_the_little_mermaid:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Little Mermad Movies\\The Little Mermad (1989)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Little Mermad Movies\\The Little Mermaid 2 -"
                                  " Return to the Sea (2000)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\The Little Mermad Movies\\The Little Mermaid 3 -"
                                  " Ariels Beginning (2008)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_the_princess_and_the_frog = ["open princess and the frog", "watch princess and the frog",
                                        "see princess and the frog", "open the princess and the frog",
                                        "watch the princess and the frog", "see the princess and the frog",
                                        "open frog and the princess", "watch frog and the princess",
                                        "see frog and the princess", "open the frog and the princess",
                                        "watch the frog and the princess", "see the frog and the princess"]
    for jarvis in jarvis_the_princess_and_the_frog:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\the princess and the frog (2009)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_road_to_el_dorado = ["open road to el dorado", "watch road to el dorado", "see road to el dorado",
                                    "open the road to el dorado", "watch the road to el dorado",
                                    "see the road to el dorado"]
    for jarvis in jarvis_the_road_to_el_dorado:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Road to El Dorado (2000)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_sword_in_the_stone = ["open sword in the stone", "watch sword in the stone", "see sword in the stone",
                                     "open the sword in the stone", "watch the sword in the stone",
                                     "see the sword in the stone"]
    for jarvis in jarvis_the_sword_in_the_stone:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\The Sword in the Stone (1963)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_toy_story = ["open toy story", "watch toy story", "see toy story"]
    for jarvis in jarvis_toy_story:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2, 3 or 4?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\toy story movies\\Toy Story (1995)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\toy story movies\\Toy Story 2 (1999)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\toy story movies\\toy story 3 (2010)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "4" in which_movie or "four" in which_movie or "for" in which_movie or "third" in which_movie \
                    or "fourth" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\toy story movies\\Toy Story 4 (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_treasure_planet = ["open treasure planet", "watch treasure planet", "see treasure planet"]
    for jarvis in jarvis_treasure_planet:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Treasure Planet (2002)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_up = ["open up", "watch up", "see up"]
    for jarvis in jarvis_up:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Up (2009)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_wreck_it_ralph = ["open wreck-it ralph", "watch wreck-it ralph", "see wreck-it ralph"]
    for jarvis in jarvis_wreck_it_ralph:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Wreck-It Ralph Movies\\Wreck It Ralph (2012)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Wreck-It Ralph Movies\\Ralph Breaks the Internet (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_zootopia = ["open zootopia", "watch zootopia", "see zootopia"]
    for jarvis in jarvis_zootopia:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Diseny movies\\Zootopia (2016)"])
            robots_name_system("Enjoy the movie sir")
            exit()


def marvelOpener():
    jarvis_ant_man = ["open ant-man", "watch ant-man", "see ant-man"]
    for jarvis in jarvis_ant_man:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Ant-Man movies\\Ant-Man (2015)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Ant-Man movies\\Ant-Man And The Wasp (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_aquaman = ["open aquaman", "watch aquaman", "see aquaman"]
    for jarvis in jarvis_aquaman:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\Aquaman (2018)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_the_avengers = ["open avengers", "watch avengers", "see avengers",
                           "open the avengers", "watch the avengers", "see the avengers", ]
    for jarvis in jarvis_the_avengers:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 - The Avengers, 2 - Age of Ultron, 3 - Infinity War or 4 - Endgame?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "the avengers" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Avengers movies\\The Avengers (2012 )"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "age of ultron" in which_movie or "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Avengers movies\\Avengers Age of Ultron (2015)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "infinity war" in which_movie or "3" in which_movie or "three" in which_movie or "tree" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Avengers movies\\Avengers Infinity War (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "endgame" in which_movie or "game" in which_movie or "end game" in which_movie or "4" in which_movie \
                    or "four" in which_movie or "for" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Avengers movies\\Avengers Endgame (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_black_panther = ["open black panther", "watch black panther", "see black panther",
                            "open the black panther", "watch the black panther", "see the black panther"]
    for jarvis in jarvis_black_panther:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\Black Panther (2018)"])
            robots_name_system("Enjoy the movie sir")
            robot_sleep()

    jarvis_captain_america = ["open captain america", "watch captain america", "see captain america"]
    for jarvis in jarvis_captain_america:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 - The First Avenger, 2 - The Winter Soldier or 3 - Civil War?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Captain America movies\\"
                                  "Captain America The First Avenger (2011)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Captain America movies\\"
                                  "Captain America The Winter Soldier (2014)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Captain America movies\\"
                                  "Captain America Civil War (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_captain_marvel = ["open captain marvel", "watch captain marvel", "see captain marvel"]
    for jarvis in jarvis_captain_marvel:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\Captain Marvel (2019)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_deadpool = ["open deadpool", "watch deadpool", "see deadpool",
                       "open dead pool", "watch dead pool", "see dead pool"]
    for jarvis in jarvis_deadpool:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Deadpool Movies\\Deadpool (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Deadpool Movies\\Deadpool 2 (2018)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_doctor_strange = ["open doctor strange", "watch doctor strange", "see doctor strange"]
    for jarvis in jarvis_doctor_strange:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\Doctor Strange (2016)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_guardians_of_the_galaxy = ["open guardians of the galaxy", "watch guardians of the galaxy",
                                      "see guardians of the galaxy", "open the guardians of the galaxy",
                                      "watch the guardians of the galaxy", "see the guardians of the galaxy"]
    for jarvis in jarvis_guardians_of_the_galaxy:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 or 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Guardians of the Galaxy movies\\"
                                  "Guardians of the Galaxy (2014)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Guardians of the Galaxy movies\\"
                                  "Guardians of the Galaxy Vol. 2 (2017)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_iron_man = ["open iron man", "watch iron man", "see iron man",
                       "open island man", "watch island man", "see island man",
                       "open bibleman", "watch bibleman", "see bibleman",
                       "open ottoman", "watch ottoman", "see ottoman",
                       "open islandman", "watch islandman", "see islandman"]
    for jarvis in jarvis_iron_man:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2 or 3?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Iron Man movies\\Iron Man (2008)"])
                robots_name_system("Great choice sir. Love you 3000")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Iron Man movies\\Iron man 2 (2010)"])
                robots_name_system("Great choice sir. Love you 3000")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Iron Man movies\\Iron Man 3 (2013)"])
                robots_name_system("Great choice sir. Love you 3000")
                exit()

    jarvis_spider_man = ["open spider-man", "watch spider-man", "see spider-man",
                         "open spiderman", "watch spiderman", "see spiderman"]
    for jarvis in jarvis_spider_man:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1 - Homecoming or 2 - Far From Home?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "homecoming" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Spider - Man movies\\"
                                  "Spider-Man Homecoming (2017)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "far from home" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Marvel  and DC movies\\Spider - Man movies\\Spider-Man "
                                  "Far from Home (2019)"])
                robots_name_system("Enjoy the movie sir")
                exit()

    jarvis_incredible_hulk = ["open incredible hulk", "watch incredible hulk", "see incredible hulk"]
    for jarvis in jarvis_incredible_hulk:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\The Incredible Hulk (2008)"])
            robots_name_system("Enjoy the movie sir")
            exit()

        jarvis_thor = ["open thor", "watch thor", "see thor",
                       "open toe", "watch toe", "see toe",
                       "open touhou", "watch touhou", "see touhou"]
        for robot_name in jarvis_thor:
            if robot_name in user_voice_text:
                robots_name_system("Which movie? 1, 2 - The Dark World or 3 - Ragnarok?")
                which_movie = record_audio()
                if "1" in which_movie or "one" in which_movie:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Marvel  and DC movies\\Thor movies\\Thor (2011)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "2" in which_movie or "two" in which_movie or "too" in which_movie or "the dark world" in which_movie \
                        or "the dark word" in which_movie:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Marvel  and DC movies\\Thor movies\\Thor The Dark World (2013)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()
                if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "ragnarok" in which_movie:
                    subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                      "D:\\MOVIES\\Marvel  and DC movies\\Thor movies\\Thor Ragnarok (2017)"])
                    robots_name_system("Enjoy the movie sir")
                    exit()

    jarvis_venom = ["open venom", "watch venom", "see venom"]
    for jarvis in jarvis_venom:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Marvel  and DC movies\\Venom (2018)"])
            robots_name_system("Enjoy the movie sir")
            exit()


def scienceFictionOpener():
    jarvis_avatar = ["open avatar", "watch avatar", "see avatar"]
    for jarvis in jarvis_avatar:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Sience fiction movies\\Avatar (2009)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_dark_shadows = ["open dark shadows", "watch dark shadows", "see dark shadows"]
    for jarvis in jarvis_dark_shadows:
        if jarvis in user_voice_text:
            subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                              "D:\\MOVIES\\Sience fiction movies\\Dark Shadows (2012)"])
            robots_name_system("Enjoy the movie sir")
            exit()

    jarvis_harry_potter = ["open harry potter", "watch harry potter", "see harry potter"]
    for jarvis in jarvis_harry_potter:
        if jarvis in user_voice_text:
            robots_name_system("Which movie? 1, 2, 3, 4, 5, 6, 7 part 1 or 7 part 2?")
            which_movie = record_audio()
            if "1" in which_movie or "one" in which_movie or "first" in which_movie or "first" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Sience fiction movies\\Harry Potter movies\\"
                                  "Harry Potter and the Philosopher's Stone (2001)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "2" in which_movie or "two" in which_movie or "too" in which_movie or "second" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Sience fiction movies\\Harry Potter movies\\"
                                  "Harry Potter and the Chamber of Secrets (2002)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "3" in which_movie or "three" in which_movie or "tree" in which_movie or "third" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\"
                                  "Ice Age 3 - Dawn of the Dinosaurs (2009)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "4" in which_movie or "four" in which_movie or "for" in which_movie or "fourth" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age 4 -Continental Drift (2012)"])
                robots_name_system("Enjoy the movie sir")
                exit()
            if "5" in which_movie or "five" in which_movie:
                subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe",
                                  "D:\\MOVIES\\Diseny movies\\Ice Age Movies\\Ice Age 5 - Collision Course (2016)"])
                robots_name_system("Enjoy the movie sir")
                exit()


def welcomeGreetings():
    jarvis_greetings = ["hi jarvis", "days home", "daddy's home", "hey jarvis", "hello jarvis", "hello Jarvis",
                        "good morning", "good evening"]
    for greeting in jarvis_greetings:
        if greeting in user_voice_text:
            wishMe()

    if "i love you" in user_voice_text:
        robots_name_system("And I love you 3000 Sir. How can i help you today?")

    jarvis_greetings = ["black bb", "rock bebe", "zach bb", "black baby"]
    for greeting in jarvis_greetings:
        if greeting in user_voice_text:
            robots_name_system("Fuck Gantz.")

    if "meow" in user_voice_text:
        robots_name_system("I can't hear you clearly Sir. please try again.")

    if "what's up" in user_voice_text:
        robots_name_system("Just doing my thing.")

    jarvis_asked = ["can you hear me", "are you there", "are you working", "are you in there", "are you on"]
    for jarvis in jarvis_asked:
        if jarvis in user_voice_text:
            robots_name_system("At your service Sir.")


def jarvisIdentity():
    # if "change your name" in user_voice_text:
    #     robots_name_system("How would you like to call me?")
    #     new_robots_name = record_audio().replace(str(robots_name), str(new_robots_name))
    #     robots_name_system("Well. My name is " + str(new_robots_name) + ". I am here to make everyone's life easier and "
    #                                                                 "better.")
    #     robots_name_system("How can I help you?")
    if "s your name" in user_voice_text or "who are you" in user_voice_text or "tell me your name" in user_voice_text:
        robots_name_system("My name is JARVIS")

    if "tell me a secret" in user_voice_text:
        robots_name_system("Here's my deepest, darkest secret. I've never taken a shower.")

    if "tell me about yourself" in user_voice_text:
        robots_name_system("I am a virtual assistant named JARVIS which was designed by Jonathan.")

    if "can you do" in user_voice_text:
        robots_name_system("I can do a lot of things. Try to say open Netflix or send a message.")
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
        robots_name_system(answers[answers_counter])
        answers_counter = answers_counter + 1
        if answers_counter is len(answers):
            answers_counter = 0

    jarvis_compliments = ["you are funny", "you're funny", "you are so funny", "you're so funny", "you are awesome",
                          "you're awesome", "you are adorable", "you're adorable", "you are the best"]
    for jarvis in jarvis_compliments:
        if jarvis in user_voice_text:
            robots_name_system("Ha ha ha, thank you. I working on that.")
            robots_name_system("Meanwhile, how can I help you?")


def familyRecognition():
    if "m roni" in user_voice_text or "m horny" in user_voice_text:
        robots_name_system("Hey Jonathan's father. nice to meet you.")
        robots_name_system("How can I help you?")

    if "m lia" in user_voice_text or "m leah" in user_voice_text:
        robots_name_system("Hey Jonathan's mother. nice to meet you.")
        robots_name_system("How can I help you?")

    if "m daniel" in user_voice_text:
        robots_name_system("Hey Jonathan's brother. nice to meet you.")
        robots_name_system("How can I help you?")

    jarvis_sisters_names = ["m mishael", "m mishel", "m michel", "m michael", "m me carla", "m malala", "m mitchell",
                            "m she-ra", "m serum", "m sheba", "m shira", "m sheila"]
    for jarvis in jarvis_sisters_names:
        if jarvis in user_voice_text:
            robots_name_system("Hey Jonathan's sister. nice to meet you.")
            robots_name_system("How can I help you?")

    if "m magal" in user_voice_text or "m miguel" in user_voice_text:
        robots_name_system("Hey Jonathan's brother in law. nice to meet you.")
        robots_name_system("I wanted to thank you for your code help. I hope you enjoy my service.")
        robots_name_system("How can I help you?")


def openBrowsers():
    if "who is" in user_voice_text or "give me information about" in user_voice_text or \
            "tell me about" in user_voice_text or "what do you know about" in user_voice_text:
        try:
            robots_name_system("Searching in Wikipedia...")
            results = wikipedia.summary(user_voice_text, sentences=2)
            robots_name_system(results)
        except:
            robots_name_system("There in no information about this person on the internet")
        helper()

    if "give me all information you can find about" in user_voice_text or \
            "give me everything you can find about" in user_voice_text:
        try:
            robots_name_system("Searching in Wikipedia...")
            results = wikipedia.summary(user_voice_text, sentences=4)
            robots_name_system(results)
        except:
            robots_name_system("There in no information about this person on the internet")
        helper()

    if "open google" in user_voice_text:
        url = "google.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening google...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open youtube" in user_voice_text:
        url = "youtube.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening YouTube...")
        webbrowser.get(chrome_path).open(url)
        helper()

    jarvis_open_email = ["open gmail", "open email", "open my email", "open my gmail"]
    for greeting in jarvis_open_email:
        if greeting in user_voice_text:
            url = "https://mail.google.com/mail/u/0/?tab=rm#inbox"
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
            robots_name_system("Opening Email...")
            webbrowser.get(chrome_path).open(url)
            helper()

    if "open facebook" in user_voice_text:
        url = "facebook.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening Facebook...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open netflix" in user_voice_text:
        url = "netflix.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening Netflix...")
        webbrowser.get(chrome_path).open(url)
        exit()

    if "open amazon" in user_voice_text:
        url = "amazon.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening Amazon...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open ebay" in user_voice_text:
        url = "ebay.com"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening eBay...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open morfix" in user_voice_text:
        url = "morfix.co.il"
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
        robots_name_system("Opening Morfix...")
        webbrowser.get(chrome_path).open(url)
        helper()

    if "open spotify" in user_voice_text:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        helper()

    jarvis_open_whatsapp = ["open whatsapp", "display messages", "display whatsapp messages", "my messages",
                            "display my whatsapp messages", "display message", "display whatsapp message",
                            "display a message", "display on messages", "show me the messages", "show messages",
                            "play my messages"]
    for jarvis in jarvis_open_whatsapp:
        if jarvis in user_voice_text:
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
    if "search in google" in user_voice_text:
        what_to_search = user_voice_text.replace("search in google", "")
        url = 'https://www.google.com/search?q='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "searching google" in user_voice_text:
        what_to_search = user_voice_text.replace("searching google", "")
        url = 'https://www.google.com/search?q='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "sachin google" in user_voice_text:
        what_to_search = user_voice_text.replace("sachin google", "")
        url = 'https://www.google.com/search?q='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "search in youtube" in user_voice_text:
        what_to_search = user_voice_text.replace("search in youtube", "")
        url = 'https://www.youtube.com/results?search_query='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "searching youtube" in user_voice_text:
        what_to_search = user_voice_text.replace("searching youtube", "")
        url = 'https://www.youtube.com/results?search_query='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "sachin youtube" in user_voice_text:
        what_to_search = user_voice_text.replace("sachin youtube", "")
        url = 'https://www.youtube.com/results?search_query='
        search_url = url + what_to_search
        webbrowser.open(search_url)
        helper()

    if "what is the weather in" in user_voice_text:
        what_to_search = user_voice_text.replace("what is the weather in ", "")
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
            robots_name_system("I didn't get the city. please repeat city name.")
            city_name = record_audio()
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

        robots_name_system("The weather in " + str(city_name) + " is " + str(temp_celsuis) + " degrees with " +
                           str(weather) + ".")
        if temp_min == temp_max:
            robots_name_system("The humidity there today is " + str(humidity) +
                               "% and it feels like " + str(feels_like) + ".")
        else:
            robots_name_system(
                "The humidity today is " + str(humidity) + "% and the weather will be between "
                + str(temp_min) + " and " + str(temp_max) + " degrees.")
        if feels_like < 20:
            robots_name_system("I recommend you to take a coat with you today Sir. "
                               "It feels like " + str(feels_like) + " degrees outside.")
        elif feels_like > 25:
            robots_name_system("I recommend you to take your sunglasses today Sir. "
                               "It is a sunny day and feels like " + str(feels_like) + " degrees outside.")
        else:
            robots_name_system("Have a nice day")

        url = 'https://www.google.com/search?newwindow=1&sxsrf=ALeKk02IyZcrkKFD0O1cJw7Zj-9ML0h6Wg%3A1605801036107&ei' \
              '=TJS2X_WRBo60gQai1rfYCQ&q=weather+ '
        search_url = url + what_to_search
        robots_name_system("Here is some more weather data I have found for" + user_voice_text.replace("what is the "
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
    jarvis_ending = ["send a message", "send a whatsapp message"]
    for jarvis in jarvis_ending:
        if jarvis in user_voice_text:
            robots_name_system("To who would you like to message?")
            which_one = record_audio()
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
                "my mom": "+972537345739",
                "mother": "+972537345739",
                "my mother": "+972537345739",
                "mom": "+972537345739",
                "mama": "+972537345739",
                "fema": "+972537345739",
                "emo": "+972537345739",
                "emma": "+972537345739",
                "lia": "+972537345739",
                "leah": "+972537345739",
                "hema": "+972537345739",
                # father:
                "roni": "+972522744248",
                "abba": "+972522744248",
                "papa": "+972522744248",
                "horny": "+972522744248",
                # shira:
                "shira": "+972523507576",
                "sheba": "+972523507576",
                "sheila": "+972523507576",
                "she-ra": "+972523507576",
                "serum": "+972523507576",
                "dallas": "+972523507576",
                "shottas": "+972523507576",
                "shut us": "+972523507576",
                "shabbos": "+972523507576",
                "chevis": "+972523507576",
                # dani:
                "daniel": '+972523218086',
                "loser": '+972523218086',
                "efes": '+972523218086',
                "fs": '+972523218086',
                "dani": '+972523218086',
                "doona": '+972523218086',
                "luna": '+972523218086',
                # micheal:
                "mishael": "+972524797269",
                "mishel": "+972524797269",
                "michel": "+972524797269",
                "michael": "+972524797269",
                "me carla": "+972524797269",
                "malala": "+972524797269",
                "mitchell": "+972524797269",
                "michaela": "+972524797269",
                "michelle": "+972524797269",
                # magal:
                "magal": "+972526003830",
                "miguel": "+972526003830",
                # ###########family#################

                # ###########friends#################
                # banov:
                "finals": "+972546156775",
                "vinyl": "+972546156775",
                "bono's": "+972546156775",
                "banov": "+972546156775",
                "bono": "+972546156775",
                "banner of": "+972546156775",
                # idan:
                "beta": "+972586245315",
                "pizza": "+972586245315",
                "baytown": "+972586245315",
                "idan": "+972586245315",
                "he done": "+972586245315",
                "edone": "+972586245315",
                # dolev:
                "go live": "+972506791105",
                "dora live": "+972506791105",
                "dolive": "+972506791105",
                "dolev": "+972506791105",
                "dollar": "+972506791105",
                # ori:
                "bowie": "+972548015343",
                "ali": "+972548015343",
                "oggy": "+972548015343",
                "oli": "+972548015343",
                "holy": "+972548015343",
                "ori": "+972548015343",
                # alon:
                "alon": "+972587312954",
                "alone": "+972587312954",
                # zelig:
                "zelig": "+972585667666",
                "vic": "+972585667666",
                "tzedek": "+972585667666",
                "billy boy": "+972585667666",
                "bui bui": "+972585667666",
                "duy bui": "+972585667666",
                "dewey boy": "+972585667666",
                "stewie boy": "+972585667666",
                # lior:
                "lior": "+972542101004",
                "leo": "+972542101004",
                "liahl": "+972542101004",
                "deal": "+972542101004",
                "be all": "+972542101004",
                # elad:
                "elad": "+972542214882",
                "a nod": "+972542214882",
                "and odd": "+972542214882",
                # bremer:
                "bremer": "+972542868238",
                "blackmail": "+972542868238",
                "batman": "+972542868238",
                "savannah": "+972542868238",
                "banana": "+972542868238",
                # yahav:
                "yahav": "+972542600073",
                "do you have": "+972542600073",
                "zahav": "+972542600073",
                "yahoo": "+972542600073",
                # ilan:
                "ilan": "+972506506033",
                "elan": "+972506506033",
                "ellen": "+972506506033",
                # mati:
                "mati": "+972535223182",
                "matty": "+972535223182",
                "matvey": "+972535223182"
            }
            contact = my_contact.get(which_one)
            while contact is None:
                robots_name_system("Please say again.")
                which_one = record_audio()
                contact = my_contact.get(which_one)
            robots_name_system("What is the message?")
            body_text = record_audio()
            k.sendwhatmsg(contact, body_text, hour, minute)


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

    jarvis_face_recogniser = ["give me the name", "recognize", "organize", "organized", "galvanized", "identify",
                              "scan"]
    for jarvis in jarvis_face_recogniser:
        if jarvis in user_voice_text:
            robots_name_system("Recognizing...")
            recognized_name = faceRecognizer()

            if "Jonathan" == recognized_name:
                robots_name_system("hey master")
                robots_name_system("your name is Jonathan Zilca and are " + str(year - 2002) + " years old.")
                robots_name_system("These days you work as a soldier.")

            if "Lia" == recognized_name:
                robots_name_system("Her name is Lia Zilca and she is " + str(year - 1961) + " years old.")
                robots_name_system("These days she works as a nurse in the Asaf Haroffe hospital.")

            if "Roni" == recognized_name:
                robots_name_system("His name is Roni Zilca and he is " + str(year - 1962) + " years old.")
                robots_name_system("These days he works as a lawyer.")

            if "Daniel" == recognized_name:
                robots_name_system("His name is Daniel Zilca and he is " + str(year - 1992) + " years old.")
                robots_name_system("These days he works in the A.L Electronics company.")

            if "Michal" == recognized_name:
                robots_name_system("Her name is Micheal Zilca and she is " + str(year - 1999) + " years old.")
                robots_name_system("These days she works as a waitress in the Ben-Gurion airport.")

            if "Alon" == recognized_name:
                robots_name_system("His name is Alon dalach and he is " + str(year - 2002) + " years old.")
                robots_name_system(
                    "These days he is fucking your mother ha ha ha ha the word wizard did it again beeeeeeaaaachhhh.")

            if "Banov" == recognized_name:
                robots_name_system("His name is Daniel Banovski and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he works as a promoter.")

            if "Bremer" == recognized_name:
                robots_name_system("Her name is Adi Bremer and she is " + str(year - 2002) + " years old.")
                robots_name_system("These days she works as a soldier.")

            if "Dolev" == recognized_name:
                robots_name_system("His name is Dolev fishman and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he works as a soldier.")

            if "Elad" == recognized_name:
                robots_name_system("His name is Elad Mani and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he works as a soldier.")

            if "Idan" == recognized_name:
                robots_name_system("His name is Idan Pogrevinski and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he is a soldier-student in the Technion University.")

            if "Ilan" == recognized_name:
                robots_name_system("His name is Ilan Gimelferb and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he works as a soldier.")

            if "Matvey" == recognized_name:
                robots_name_system("His name is Matvey Oodler and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he works as a soldier")

            if "Lior" == recognized_name:
                robots_name_system("His name is Lior Raphael and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he is a soldier-student in Bar-Ilan University.")

            if "Maya" == recognized_name:
                robots_name_system("Her name is Maya Gaver and she is " + str(year - 2002) + " years old.")
                robots_name_system("These days she works as a soldier.")

            if "Ori" == recognized_name:
                robots_name_system("His name is Ori Anvar and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he is a soldier-student in the Technion University.")

            if "Zelig" == recognized_name:
                robots_name_system("His name is Daniel Zelig and he is " + str(year - 2002) + " years old.")
                robots_name_system("These days he is a soldier-student in Ort Singalovski.")

            if "Unknown" == recognized_name:
                robots_name_system("Sorry Sir, but this person does not appear in my database.")


def respond():
    welcomeGreetings()
    jarvisIdentity()
    familyRecognition()
    movieSuggestions()
    disneyOpener()
    marvelOpener()
    scienceFictionOpener()
    openBrowsers()
    internetSearch()
    sendingMassage()
    peopleInfo()
    wakingAlarm()

    if "what time is it" in user_voice_text or "time" in user_voice_text:
        robots_name_system(ctime())
        helper()

    if "give me bit" in user_voice_text or "give me beat" in user_voice_text \
            or "give me a bit" in user_voice_text or "give me a beat" in user_voice_text:
        robots_name_system("Ged ready to the best bit you have ever heard!")
        robots_name_system("boom boom tack the boom boom tack yeah boom boom tack the boom boom tack yeah")
        robots_name_system("Do you think you can beat me? Ha ha ha")

    # jokes:
    jarvis_ending = ["tell me a joke", "tell a joke", "tell me another", "cheer me up", "give me a joke"]
    for jarvis in jarvis_ending:
        if jarvis in user_voice_text:
            global jokes_counter
            robots_name_system(jokes[jokes_counter][0])
            time.sleep(2)
            robots_name_system(jokes[jokes_counter][1])
            jokes_counter = jokes_counter + 1
            if jokes_counter is len(jokes):
                jokes_counter = 0

    jarvis_ending = ["bye", "goodbye", "nighty night", "that's all for today", "that's awful today", "shut down",
                     "stop", "that's enough", "see you next time", "not now", "i have to go", "buy", "see you soon",
                     "shutdown"]
    for jarvis in jarvis_ending:
        if jarvis in user_voice_text:
            robots_name_system(goodbye[0])
            robot_sleep()


def robot_sleep():
    wake_command = "jarvis"
    while True:
        user_voice_text = record_audio()
        if user_voice_text.count(wake_command) > 0:
            robots_name_system("Ready for your command Sir.")
            while True:
                user_voice_text = record_audio()
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

# robots_name = str("jarvis")
#
# wake_command = str(robots_name)
# while True:
#   user_voice_text = record_audio()
#   if user_voice_text.count(wake_command) > 0:
#       robots_name_system("Ready for your command Sir.")
#     while True:
#          user_voice_text = record_audio()
#          respond()

while True:
    user_voice_text = record_audio()
    respond()
