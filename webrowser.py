import json
import webbrowser
import wikipedia
from conversation import robot_say, take_command, person_request

import requests

send_url = "http://api.ipstack.com/check?access_key=24dfaa6dde294f06a6c4c28fe58ca75e"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
currentLocation = geo_json['city']


def google_search():
    what_to_search = person_request.split("google")[1]
    url = 'https://www.google.com/search?q='
    search_url = url + what_to_search
    webbrowser.open(search_url)


def youtube_search():
    what_to_search = person_request.split("youtube")[1]
    url = 'https://www.youtube.com/results?search_query='
    search_url = url + what_to_search
    webbrowser.open(search_url)


def location():
    try:
        robot_say("You are in " + str(currentLocation) + ".")
    except:
        robot_say("I don't know. My location service is down.")


def weather_search():
    what_to_search = person_request.split("in ")[1]
    city_name = what_to_search
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
        city_name) + "&appid=a19e10287fb85f419d1aeab1971019b0"
    results = requests.get(url.format(city_name))
    info = results.json()
    try:
        temp_kelvin = info['main']['temp']
        temp_celsuis = int(round(temp_kelvin - 273))
        weather = info['weather'][0]['description']
        pre_feels_like = info['main']['feels_like']
        feels_like = int(round(pre_feels_like - 273))
        pre_temp_min = info['main']['temp_min']
        temp_min = int(round(pre_temp_min - 273))
        pre_temp_max = info['main']['temp_max']
        temp_max = int(round(pre_temp_max - 273))
        humidity = info['main']['humidity']
    except:
        robot_say("I didn't get the city. please repeat the city name.")
        city_name = take_command()
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + str(
            city_name) + "&appid=a19e10287fb85f419d1aeab1971019b0"
        results = requests.get(url.format(city_name))
        info = results.json()
        temp_kelvin = info['main']['temp']
        temp_celsuis = int(round(temp_kelvin - 273))
        weather = info['weather'][0]['description']
        pre_feels_like = info['main']['feels_like']
        feels_like = int(round(pre_feels_like - 273))
        pre_temp_min = info['main']['temp_min']
        temp_min = int(round(pre_temp_min - 273))
        pre_temp_max = info['main']['temp_max']
        temp_max = int(round(pre_temp_max - 273))
        humidity = info['main']['humidity']

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


def wikipedia_search():
    try:
        search_subject = person_request.split("wikipedia")[1]
        robot_say("Searching in Wikipedia...")
        results = wikipedia.summary(search_subject, sentences=3)
        robot_say(results)
    except:
        robot_say("There in no information about this person on the internet")


def open_browser():
    get_website = person_request.split("open ")[1]
    website_name_path = get_website.replace(" ", "")
    url = website_name_path + ".com"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    print("Opening " + get_website + "...")
    webbrowser.get(chrome_path).open(url)


def open_gmail():
    url = "https://mail.google.com/mail/u/0/?tab=rm#inbox"
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    robot_say("Opening Email...")
    webbrowser.get(chrome_path).open(url)
