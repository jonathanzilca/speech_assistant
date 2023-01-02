import subprocess
from conversation import robot_say, person_request
import requests
import spotipy

username = "Jonathan"
client_id = "f26c9b8e47e0472c929bb1c47826e831"
client_secret = "633a1c6eeeaf462ba7f66e2e1498b6c4"
device_id = "98b72dfb7d1c28362cc7281a11cd9ae6767f21f6"
redirect_uri = "http://localhost:8888/callback"
scope = "user-modify-playback-state playlist-read-private"


def play_spotify():
    try:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        # Get an access token
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", }

        data = {"device_ids": [device_id], "play": True, }

        requests.put("https://api.spotify.com/v1/me/player", headers=headers, json=data)
    except:
        robot_say("Spotify account connection has failed.")

    return token


def pause_spotify():
    try:
        subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        # Get an access token
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", }

        data = {"device_ids": [device_id], "play": False, }

        requests.put("https://api.spotify.com/v1/me/player", headers=headers, json=data)
    except:
        robot_say("Spotify account connection has failed.")


def play_searched_song():
    token = play_spotify()

    headers = {"Authorization": f"Bearer {token}"}

    # song name
    song_name = ""
    if "play" in person_request:
        song_name = person_request.split("play ")[1]
    elif "to hear" in person_request:
        song_name = person_request.split("to hear ")[1]
    elif "listen to" in person_request:
        song_name = person_request.split("listen to ")[1]

    try:
        # Make a request to the search endpoint
        response = requests.get("https://api.spotify.com/v1/search", params={"q": song_name, "type": "track"},
                                headers=headers)

        # Extract the list of tracks from the response
        tracks = response.json()["tracks"]["items"]
        first_track = tracks[0]

        # Print the track ID and name of the first track
        track_id = first_track["id"]

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
            try:
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
                requests.put("https://api.spotify.com/v1/me/player/play", json={"context_uri": artist_uri},
                                        headers=headers)
            except:
                play_spotify()


def next_song():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
    try:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        # Use the access token to play the next song
        headers = {"Authorization": "Bearer " + token}
        requests.post("https://api.spotify.com/v1/me/player/next", headers=headers)
    except:
        robot_say("Spotify account connection has failed.")


def previous_song():
    subprocess.Popen(["C:\\Users\\yonat\\AppData\\Roaming\\Spotify\\Spotify.exe"])
    try:
        token = spotipy.util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        # Use the access token to play the next song
        headers = {"Authorization": "Bearer " + token}
        requests.post("https://api.spotify.com/v1/me/player/previous", headers=headers)
    except:
        robot_say("Spotify account connection has failed.")
