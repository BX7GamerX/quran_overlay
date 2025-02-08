import requests
import os
import vlc
import time

chapter_id = 114
recitation_id = 7
url = f"https://api.quran.com/api/v4/chapter_recitations/{recitation_id}/{chapter_id}"
headers = {"Accept": "application/json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    audio_url = data["audio_file"]["audio_url"]
    audio_path = os.path.join(os.path.dirname(__file__), "quran_audio.mp3")

    audio_response = requests.get(audio_url)
    if audio_response.status_code == 200:
        with open(audio_path, "wb") as f:
            f.write(audio_response.content)

        player = vlc.MediaPlayer(audio_path)
        player.play()

        # Optional wait for the track to finish
        time.sleep(0.5)
        duration = player.get_length() / 1000
        time.sleep(duration)
    else:
        print(f"Failed to download audio file: {audio_response.status_code}")
else:
    print(f"Request failed: {response.status_code}")


class AudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def play(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def get_time(self):
        # Returns current playback time in seconds.
        return self.player.get_time() / 1000.0

    def get_length(self):
        # Returns total audio duration in seconds.
        return self.player.get_length() / 1000.0
