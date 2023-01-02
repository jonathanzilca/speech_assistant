import pyttsx3
import speech_recognition

robot_name = "Jarvis"
person_request = ""


def robot_say(audio_string: str) -> None:
    """

    :param audio_string: string that the robot will say.
    :return: None
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(robot_name+": "+audio_string)
    engine.say(audio_string)
    engine.runAndWait()


def take_command():
    with speech_recognition.Microphone() as mic:
        speech_recognition.Recognizer().adjust_for_ambient_noise(mic, duration=0.2)
        audio = speech_recognition.Recognizer().listen(mic, 7, 7)

        try:
            command = speech_recognition.Recognizer().recognize_google(audio)
            print("You: {}".format(command))
        except speech_recognition.UnknownValueError:
            return "fdgdf"
        except speech_recognition.RequestError:
            robot_say("Sorry, my speech service is down")

        return command.lower()
