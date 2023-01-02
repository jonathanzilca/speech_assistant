import difflib
import glob
import random
import re
import subprocess
import time

import nltk
import speech_recognition
import volume
from conversation import robot_say, take_command, person_request


# def movieModeBack():
#     if previous_movie.poll() is None:
#         robot_say("You have to watch a movie first to activate Movie mode.")
#     else:
#         movieMode(chosenRightMoviePath, start_time, hebrew_subtitle_path, english_subtitle_path)

def movie_mode_commands(movie_path, start_time, hebrew_subtitle_path, english_subtitle_path, full_process):
    movie_command = movie_mode()
    save_watched_time = str(time.time() - start_time)
    stop_command = ["pause", "stop", "i am going", "going", "about to go", "leaving", "about to leave"]
    for robot in stop_command:
        if robot in movie_command:
            try:
                full_process.terminate()
                robot_say("Movie paused")
            except:
                robot_say("The movie is already not playing")

    play_command = ["play", "start"]
    for robot in play_command:
        if robot in movie_command:
            try:
                if "Hebrew" in full_process.args[3]:
                    full_process = subprocess.Popen(
                        ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", "--sub-file",
                         hebrew_subtitle_path, "--start-time=" + save_watched_time + "", movie_path],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif "English" in full_process.args[3]:
                    full_process = subprocess.Popen(
                        ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", "--sub-file",
                         english_subtitle_path, "--start-time=" + save_watched_time + "", movie_path],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                else:
                    full_process = subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen",
                                                     "--start-time=" + save_watched_time + "", movie_path],
                                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE)
                robot_say("Playing movie")
            except:
                robot_say("The movie is already playing")

    add_sub_command = ["add", "change"]
    for robot in add_sub_command:
        if robot in movie_command:
            try:
                full_process.terminate()
                if "hebrew" in movie_command:
                    full_process = subprocess.Popen(
                        ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", "--sub-file",
                         hebrew_subtitle_path, "--start-time=" + save_watched_time + "", movie_path],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    robot_say("Hebrew subtitles added")
                else:
                    full_process = subprocess.Popen(
                        ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", "--sub-file",
                         english_subtitle_path, "--start-time=" + save_watched_time + "", movie_path],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    robot_say("English subtitles added")
            except:
                full_process.terminate()
                full_process = subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen",
                                                 "--start-time=" + save_watched_time + "", movie_path],
                                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                robot_say("Something go wrong. No subtitles were added")

    remove_sub_command = ["remove"]
    for robot in remove_sub_command:
        if robot in movie_command:
            try:
                full_process.terminate()
                full_process = subprocess.Popen(["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen",
                                                 "--start-time=" + save_watched_time + "", movie_path],
                                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                robot_say("Subtitles removed")
            except:
                robot_say("Something go wrong.")

    volume_up_command = ["turn volume up", "volume up", "turn up volume ", "increase the volume", "raise the volume"]
    for robot in volume_up_command:
        if robot in movie_command:
            volume.up()

    volume_down_command = ["turn volume down", "volume down", "turn down volume ", "decrease the volume",
                           "lower the volume"]
    for robot in volume_down_command:
        if robot in movie_command:
            volume.down()

    volume_mute_command = ["hush", "silence", "keep it down", "quiet", "mute", "unmute", "bring back volume"]
    for robot in volume_mute_command:
        if robot in movie_command:
            volume.mute()

    set_volume_command = ["set vol", "set the vol", "max"]
    for robot in set_volume_command:
        if robot in movie_command:
            volume.set_vol()

    volume_up_command = ["exit", "get out", "deactivate", "disable", "turn on"]
    for robot in volume_up_command:
        if robot in movie_command:
            robot_say("Movie mode disabled")
            # robot_waiting_for_command() TODO: activate it back


def movie_mode(movie_path, start_time, hebrew_subtitle_path, english_subtitle_path, full_process):
    movie_command = ""
    while True:
        try:
            movie_command = take_command()
            movie_mode_commands(movie_path, start_time, hebrew_subtitle_path, english_subtitle_path, full_process)
        except speech_recognition.UnknownValueError:
            speech_recognition.Recognizer()
        except speech_recognition.WaitTimeoutError:
            speech_recognition.Recognizer()
        return movie_command


def extract_movie_name(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)

    movie_name = []
    for i, (token, pos_tag) in enumerate(pos_tags):
        if pos_tag == 'NNP' or (pos_tag == 'IN' and movie_name):
            movie_name.append(token)
        elif movie_name:
            break

    return " ".join(movie_name)


def watch_movie():
    movies_path = glob.glob("D:\\MOVIES\**\*\*\*\*.mp4", recursive=True) \
                  + glob.glob("D:\\MOVIES\**\*\*\*\*.mkv", recursive=True) \
                  + glob.glob("D:\\MOVIES\**\*\*\*\*.avi", recursive=True)

    requested_movie = extract_movie_name(person_request)
    movie_number = [int(s) for s in re.findall(r'\b\d+\b', person_request)]
    try:
        if len(movie_number) != 0:
            full_movie_name = requested_movie + " " + str(movie_number[0])
        else:
            full_movie_name = requested_movie
    except:
        pass

    # probably the right movie
    print(full_movie_name)
    rightMoviePath = difflib.get_close_matches(full_movie_name, movies_path, len(movies_path), 0)

    i = 0
    start_time = 0
    hebrew_subtitle_path = ""
    english_subtitle_path = ""
    while i < 10:
        try:
            start_time = time.time()
            movie_name = rightMoviePath[i].split("\\")[-1]
            hebrew_subtitle_path = glob.glob(rightMoviePath[i].replace(movie_name, "Hebrew.srt"))[0]
            english_subtitle_path = glob.glob(rightMoviePath[i].replace(movie_name, "English.srt"))[0]
            previous_movie = subprocess.Popen(
                ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", "--sub-file",
                 hebrew_subtitle_path, rightMoviePath[i]], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            previous_movie = subprocess.Popen(
                ["C:\\Users\\yonat\\Downloads\\VLC\\vlc.exe", "--fullscreen", rightMoviePath[i]], stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        robot_say("Is this the right movie sir?")
        approve = take_command()

        if "yes" in approve or "right" in approve or "correct" in approve or "good" in approve:
            robot_say("Enjoy the movie master. Activate Movie mode.")
            movie_mode(rightMoviePath[i], start_time, hebrew_subtitle_path, english_subtitle_path, previous_movie)
            break
        elif "leave" in approve or "exit" in approve or "get out" in approve or "shut" in approve or "zip" in approve or "fuck off" in approve:
            previous_movie.terminate()
            robot_say("It's hard for me to find your movie. Sorry.")
            break
        elif "fdgdf" in approve:
            robot_say("I can't hear you")
            previous_movie.terminate()
            continue
        else:
            previous_movie.terminate()
            robot_say("Oops. Let me try again")
            i += 1


def movie_recommendation():
    if "disney" in person_request:
        movies_path = glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mp4", recursive=True) + \
                      glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.mkv", recursive=True) + \
                      glob.glob("D:\\MOVIES\\Diseny movies\**\*\*.avi", recursive=True)
        movie_category = " Disney"
    elif "marvel" in person_request:
        movies_path = glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mp4", recursive=True) + \
                      glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.mkv", recursive=True) + \
                      glob.glob("D:\\MOVIES\\Marvel  and DC movies\**\*\*.avi", recursive=True)
        movie_category = " Marvel"
    else:
        movies_path = glob.glob("D:\\MOVIES\**\*\*\*.mp4", recursive=True) + \
                      glob.glob("D:\\MOVIES\**\*\*\*.mkv", recursive=True) + \
                      glob.glob("D:\\MOVIES\**\*\*\*.avi", recursive=True)
        movie_category = ""

    moviesName = []
    for me in movies_path:
        moviesName = me.split("\\")[-1].split(".")[0]

    random.shuffle(moviesName)

    robot_say("Here are some recommended" + movie_category + " movies:")
    print("----------------------------------------")
    for i in range(5):
        num = str(i + 1)
        print(num + ") " + moviesName[i])
    print("----------------------------------------")
