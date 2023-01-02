import re
import pyautogui
from conversation import robot_say, person_request
import movies


def volume_pattern(volume_str):
    for i in range(5):
        pyautogui.press(volume_str)


def down():
    volume_pattern("volumedown")


def up():
    volume_pattern("volumeup")


def mute():
    pyautogui.press("volumemute")


def set_vol():
    movie_command = str(movies.movie_mode)
    volume_level = [int(s) for s in re.findall(r'\b\d+\b', person_request+movie_command)]
    try:
        times_to_repeat = volume_level[0] / 2
        print(int(times_to_repeat))
        for i in range(50):
            pyautogui.press("volumedown")
        for i in range(int(times_to_repeat)):
            pyautogui.press("volumeup")
        robot_say("The volume level is now " + str(volume_level[0]))
    except:
        for i in range(50):
            pyautogui.press("volumeup")
        robot_say("Volume is on the highest level")
