import pyttsx3
import requests

# Threading: Lock(acquire, release), general
# globals
# datetime object
# pep 8
weather_url = ["http://api.openweathermap.org/data/2.5/weather?q=", "&appid=a19e10287fb85f419d1aeab1971019b0"]


def sound_alarm(hour: int, minute: int, currentLocation: str) -> None:
    """

    :param hour: what hour is the alarm set to
    :param minute:
    :param currentLocation:
    :return:
    """
    url = weather_url[0] + str(currentLocation) + weather_url[1]
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

    robot_say("Hello Sir. The hour is " + str(hour) + ":" + str(minute) +
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


def robot_say(audio_string: str) -> None:
    """

    :param audio_string: string that the robot will say.
    :return: None
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()
