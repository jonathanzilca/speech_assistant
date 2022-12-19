# for spotify
import subprocess

import pyttsx3
import requests
import spotipy

username = "Jonathan"
client_id = "f26c9b8e47e0472c929bb1c47826e831"
client_secret = "633a1c6eeeaf462ba7f66e2e1498b6c4"
device_id = "98b72dfb7d1c28362cc7281a11cd9ae6767f21f6"
redirect_uri = "http://localhost:8888/callback"
scope = "user-modify-playback-state playlist-read-private"


def playSpotify():
    try:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        # Get an access token
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", }

        data = {"device_ids": [device_id], "play": True, }

        requests.put("https://api.spotify.com/v1/me/player", headers=headers, json=data)
    except:
        try:
            pass
        except:
            robot_say("Spotify account connection has failed.")

    return token


def pauseSpotify():
    try:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        # Get an access token
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", }

        data = {"device_ids": [device_id], "play": False, }

        requests.put("https://api.spotify.com/v1/me/player", headers=headers, json=data)
    except:
        robot_say("Spotify account connection has failed.")


def playSearchedSong(request):
    token = playSpotify()

    headers = {"Authorization": f"Bearer {token}"}

    # song name
    if "play " in request:
        song_name = request.split("play ")[1]
    elif "to hear" in request:
        song_name = request.split("to hear ")[1]
    elif "watch" in request:
        song_name = request.split("listen to ")[1]

    try:
        # Make a request to the search endpoint
        response = requests.get("https://api.spotify.com/v1/search", params={"q": song_name, "type": "track"},
                                headers=headers)

        # Extract the list of tracks from the response
        tracks = response.json()["tracks"]["items"]
        first_track = tracks[0]

        # Print the track ID and name of the first track
        track_id = first_track["id"]

        # track ID and name var
        song_id = f"{track_id}"
        chosen_song_name = f"{first_track['name']}"

        response = requests.put("https://api.spotify.com/v1/me/player/play",
                                json={"uris": [f"spotify:track:{track_id}"]}, headers=headers)

        # Check the status code of the response to see if the request was successful
        if response.status_code == 204:
            pass
        else:
            robot_say("Spotify account connection has failed.")
    except:
        try:
            # Make a request to the search endpoint
            response = requests.get("https://api.spotify.com/v1/search", params={"q": song_name, "type": "playlist"},
                                    headers=headers)

            # Extract the list of playlists from the response
            playlists = response.json()["playlists"]["items"]
            first_playlist = playlists[0]
            response = requests.put("https://api.spotify.com/v1/me/player/play",
                                    json={"context_uri": first_playlist['uri']}, headers=headers)

            # Check the status code of the response to see if the request was successful
            if response.status_code == 204:
                pass
            else:
                robot_say("Spotify account connection has failed.")
        except:
            # Make a request to the search endpoint
            response = requests.get("https://api.spotify.com/v1/search", params={"q": song_name, "type": "artist"},
                                    headers=headers)

            # Extract the list of artists from the response
            artists = response.json()["artists"]["items"]

            # Get the first artist from the list
            first_artist = artists[0]

            # Extract the artist's URI
            artist_uri = first_artist["uri"]

            # Make a request to the play endpoint
            response = requests.put("https://api.spotify.com/v1/me/player/play", json={"context_uri": artist_uri},
                                    headers=headers)

            # Check the status code of the response to see if the request was successful
            if response.status_code == 204:
                pass
            else:
                robot_say("Spotify account connection has failed.")


def nextSong():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
    try:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        # Use the access token to play the next song
        headers = {"Authorization": "Bearer " + token}
        response = requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    except:
        robot_say("Spotify account connection has failed.")


def previousSong():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
    try:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        # Use the access token to play the next song
        headers = {"Authorization": "Bearer " + token}
        response = requests.post("https://api.spotify.com/v1/me/player/previous", headers=headers)
    except:
        robot_say("Spotify account connection has failed.")


def robot_say(audio_string):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # speech speed
    print(audio_string)
    engine.say(audio_string)
    engine.runAndWait()