import datetime
import random
import time
from conversation import robot_say, take_command, robot_name
import conversation

jokes = [["Why shouldn't you write with a broken pencil?", "Because it's pointless."],
         ["What's the best thing about Switzerland?", "I don't know, but there flag is a big plus"],
         ["How do you call a man without a body and a nose?", "Nobody nose."],
         ["How do you call an American bee?", "a USB."],
         ["Why did the picture go to jail?", "because it was framed."],
         ["Did you sit on the F5 key?", "Because your ass is refreshing!"],
         ["I wish the corona virus started in Las Vegas", "Because what happens in Vegas stays in Vegas"],
         ["I told my wife she was drawing her eyebrows too high", "She looked surprised"],
         ["Why does Santa have such a big sack", "because he only comes once a year"]]

random.shuffle(jokes)
jokes_counter = 0


def introduce_yourself():
    robot_say(
        "I am a virtual assistant named " + str(robot_name).upper() + " which was designed by Jonathan.")
    robot_say("I am here to make everyone's life easier and better.")


def changeRobotName():
    robot_say("How would you like to call me?")
    maybe_robot_name = take_command()
    robot_say("Do you want to call me " + str(maybe_robot_name) + "?")
    approve_name = take_command()
    if "yes" in approve_name or "right" in approve_name or "correct" in approve_name:
        conversation.robot_name = maybe_robot_name
        introduce_yourself()
    elif "leave" in approve_name or "exit" in approve_name or "get out" in approve_name or "shut" in approve_name or "zip" in approve_name or "fuck off" in approve_name:
        pass
    elif "fdgdf" in approve_name:
        robot_say("I can't hear you")
        changeRobotName()
        pass
    else:
        robot_say("Oops. Let me try again")
        changeRobotName()


def greeting():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        robot_say("Good Morning Sir")

    elif 12 <= hour < 18:
        robot_say("Good Afternoon Sir")

    else:
        robot_say("Good Evening Sir")
    robot_say("I am at your service. How can I help you?")


def tellJokes():
    global jokes_counter
    robot_say(jokes[jokes_counter][0])
    time.sleep(2)
    robot_say(jokes[jokes_counter][1])
    jokes_counter = jokes_counter + 1
    if jokes_counter is len(jokes):
        jokes_counter = 0
