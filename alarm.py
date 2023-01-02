import datetime
import json
import re
import threading
import time
from conversation import robot_say, take_command
import requests

weather_url = ["http://api.openweathermap.org/data/2.5/weather?q=", "&appid=a19e10287fb85f419d1aeab1971019b0"]
send_url = "http://api.ipstack.com/check?access_key=24dfaa6dde294f06a6c4c28fe58ca75e"
geo_req = requests.get(send_url)
geo_json = json.loads(geo_req.text)
currentLocation = geo_json['city']
clock = None


def get_hour_minute(request: str):
    # Split the request into a list of words
    words = request.split()

    # Find all the numbers in the request
    numbers = [int(s) for s in re.findall(r'\b\d+\b', request)]

    # Initialize minute to 0
    minute = 0
    hour = 0

    # Check if the request includes a time indicator (e.g. "before", "after", etc.)
    time_indicator = next(
        (word for word in words if word in ("before", "for", "after", "past", "of", "til", "until", "to")), None)

    # Handle requests with time indicators
    if time_indicator:
        hour = numbers[1]
        # If the request includes "after" or "past", the first number is the number of minutes and the second number is the hour
        if time_indicator in ("after", "past"):
            minute = numbers[0]
        # If the request includes "before" or "until", subtract the number of minutes from 60
        elif time_indicator in ("before", "until", "of", "til", "to", "for"):
            minute = 60 - numbers[0]
            hour = hour - 1
    # Handle requests without time indicators
    else:
        # If the request includes two numbers, the first number is the hour and the second number is the minute
        if len(numbers) == 2:
            minute = numbers[1]
            hour = numbers[0]
        elif len(numbers) == 1:
            hour = numbers[0]
        # If the request includes one number, it is the hour
        elif len(numbers) == 0:
            hour = 0

    if "p.m" in request or "PM" in request:
        hour = hour + 12

    # Return the hour and minute as a tuple
    return hour, minute


def check_alarm(alarm_hour: int, alarm_min: int):
    while alarm_min > 59 or alarm_hour > 24:
        robot_say("when Sir?")
        request = take_command()
        get_hour_minute(request)
    return alarm_hour, alarm_min


def calculate_time_til_alarm(approved_alarm_hour: int, approved_alarm_min: int):
    # Get the current time
    now = datetime.datetime.now()

    target_time = now.replace(hour=approved_alarm_hour, minute=approved_alarm_min, second=0, microsecond=0)

    # Add one day to the target time if it is in the past
    if target_time < now:
        target_time += datetime.timedelta(days=1)

    # Calculate the time difference
    time_difference = target_time - now

    # Get the number of seconds until the target time
    seconds_until_target = time_difference.total_seconds()

    return seconds_until_target


def alarm_reminder():
    class AlarmClock:
        def __init__(self):
            self.alarms = []
            self.lock = threading.Lock()

        def set_alarm(self, alarm_time, callback):
            with self.lock:
                self.alarms.append((alarm_time, callback))

        def run(self):
            while True:
                with self.lock:
                    for alarm in self.alarms:
                        alarm_time, callback = alarm
                        if alarm_time <= time.time():
                            self.alarms.remove(alarm)
                            if callable(callback):
                                sound_alarm(approved_alarm_hour, approved_alarm_min, currentLocation)
                time.sleep(1)

    global clock
    if clock is None:
        clock = AlarmClock()

        # Start the alarm clock in a separate thread
        clock_thread = threading.Thread(target=clock.run)
        clock_thread.start()

    # getting the hour and the minute of the alarm
    alarm_hour, alarm_min = get_hour_minute()

    # the hour and the minute after check
    approved_alarm_hour, approved_alarm_min = check_alarm(alarm_hour, alarm_min)

    while True:
        robot_say(f"Did you asked for alarm at {approved_alarm_hour}:{approved_alarm_min}?")
        approve = take_command()
        if "yes" in approve or "right" in approve or "correct" in approve or "good" in approve:
            robot_say(f"Setting alarm for {approved_alarm_hour}:{approved_alarm_min}?")
            target_time = time.time() + calculate_time_til_alarm(approved_alarm_hour, approved_alarm_min)
            clock.set_alarm(target_time, sound_alarm)
            break
        elif "leave" in approve or "exit" in approve or "get out" in approve or "shut" in approve or "zip" in approve or "fuck off" in approve:
            robot_say("It's hard for me to set this alarm. Sorry.")
            break
        elif "fdgdf" in approve:
            robot_say("I can't hear you")
        else:
            robot_say("Oops. Let me try again")
            alarm_reminder()


def sound_alarm(hour: int, minute: int, current_location: str) -> None:
    """

    :param hour: what hour is the alarm set to
    :param minute:
    :param current_location:
    :return:
    """
    url = weather_url[0] + str(current_location) + weather_url[1]
    results = requests.get(url.format())
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

    robot_say("Hello Sir. The hour is " + str(hour) + ":" + str(minute) +
                   ". The weather in " + str(current_location) + " is " + str(temp_celsuis) + " degrees with " +
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
