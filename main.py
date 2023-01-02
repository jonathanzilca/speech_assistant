from neuralintents import GenericAssistant
import speech_recognition  # for the voice recognition
import volume
import alarm
import spotify
import robot_face_recognition
import webrowser
import whatsapp
import movies
import personality
import conversation


# TODO: search about tuple/array, list, QUEUE, stack


def robot_conversation():
    try:
        # person_request = take_command()
        person_request = input("You: ")
        respond = assistant.request(person_request)
        if respond is not None:
            conversation.robot_say(respond)
    except speech_recognition.UnknownValueError:
        speech_recognition.Recognizer()
    except speech_recognition.WaitTimeoutError:
        speech_recognition.Recognizer()
    # robot_waiting_for_command()


def robot_waiting_for_command():
    while True:
        try:
            record_waking_command = conversation.take_command()
            for robot in wakeup_robot_commands:
                if robot in record_waking_command:
                    personality.greeting()
                    robot_conversation()
        except speech_recognition.UnknownValueError:
            speech_recognition.Recognizer()
        except speech_recognition.WaitTimeoutError:
            speech_recognition.Recognizer()


mappings = {"robotWaitingForCommand": robot_waiting_for_command,
            "movieMode": movies.movie_mode,
            "volumeDown": volume.down,
            "volumeUp": volume.up,
            "volumeMute": volume.mute,
            "setVolume": volume.set_vol,
            "sendingMassage": whatsapp.send_massage,
            "watchMovie": movies.watch_movie,
            "faceRecognition": robot_face_recognition.faceRecognition,
            "wikipediaSearch": webrowser.wikipedia_search,
            "openBrowser": webrowser.open_browser,
            "openGmail": webrowser.open_gmail,
            "whatsApp": whatsapp.open_whatsapp,
            "googleSearch": webrowser.google_search,
            "youtubeSearch": webrowser.youtube_search,
            "weatherSearch": webrowser.weather_search,
            "movie_recommendation": movies.movie_recommendation,
            "Alarm": alarm.alarm_reminder,
            "personality": personality.introduce_yourself,
            "changeRobotName": personality.changeRobotName,
            "jokes": personality.tellJokes,
            "playSpotify": spotify.play_spotify,
            "pauseSpotify": spotify.pause_spotify,
            "playSearchedSong": spotify.play_searched_song,
            "nextSong": spotify.next_song,
            "previousSong": spotify.previous_song,
            "location": webrowser.location}

assistant = GenericAssistant('new.json', mappings)
# assistant.train_model()
# assistant.save_model()
assistant.load_model()


wakeup_robot_commands = ["hi", "days home", "daddy's home", "hey ", conversation.robot_name, "wake up",
                         "hello", "good morning", "good evening", "I'm back", "what's up"]
while True:
    robot_conversation()
