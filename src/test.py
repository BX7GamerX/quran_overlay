import requests
import os
import vlc
import time
import threading

class SurahMedia:
    def __init__(self):
        self.base_url = "https://api.quran.com/api/v4"
        self.media_path = os.path.join("media","surahs")
        self.surah_dict = {}
        self.reciter_dict = {}
        if not os.path.exists("media"):
            os.makedirs("media")
            print("media folder created")
        else:
            print("media folder already exists")
        self.get_surah_list()
        
    def get_surah_list(self):
        chapter_url = f"{self.base_url}/chapters"
        payload={}
        headers = {
            'Accept': 'application/json'
            }
        response = requests.request("GET", chapter_url, headers=headers, data=payload)
        with open (os.path.join("media","surah_list.txt"), "w") as f:
            for chapter in response.json()["chapters"]:
                f.write(f"{chapter["id"]} { chapter["name_simple"]}\n")
                self.surah_dict[chapter["id"]] = chapter["name_simple"]
        print("Surah list saved to media/surah_list.txt")

    def get_reciter_list(self):
        if not os.path.exists(os.path.join("media","reciter_list.txt")):
            reciters_url = f"{self.base_url}/resources/recitations"
            headers = {'Accept': 'application/json'}
            response = requests.get(reciters_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                for reciter in data.get("recitations", []):
                    self.temp_dict = {}
                    rid = reciter.get("id")
                    name = reciter.get("reciter_name")
                    if rid and name:
                        self.reciter_dict[rid] = name
                        #self.reciter_dict.append(self.temp_dict)
                print("Reciter list updated.")
                with open (os.path.join("media","reciter_list.txt"), "w") as f:
                    for reciter in self.reciter_dict:
                        for rid, name in reciter.items():
                            f.write(f"{rid} {name}\n")
                print("Reciter list saved to media/reciter_list.txt")
            else:
                print(f"Request failed: {response.status_code}")
        else:
            with open (os.path.join("media","reciter_list.txt"), "r") as f :
                for line in f:
                    rid, name = line.strip().split(maxsplit=1)
                    self.reciter_dict[rid] = name
                    #self.reciter_dict.append({rid: name})
            pass
    def get_surah_audio(self,chapter_id,recitation_id):
        recitation_url = f"{self.base_url}/chapter_recitations/{recitation_id}/{chapter_id}"
        headers = {"Accept": "application/json"}
        response = requests.get(recitation_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            audio_url = data["audio_file"]["audio_url"]
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                with open(self.get_audio_path(chapter_id,recitation_id), "wb") as f:
                    f.write(audio_response.content)
            else:
                print(f"Failed to download audio file: {audio_response.status_code}")
        else:
            print(f"Request failed: {response.status_code}")
        print(f"Audio file for {self.surah_dict[chapter_id]} downloaded")
    def get_audio_path(self, chapter_id,reciter_id):
        folder_path = os.path.join(self.media_path, str(chapter_id))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_name = f"{chapter_id} - {self.surah_dict[chapter_id]} by {self.reciter_dict[str(reciter_id)]}audio.mp3"
        return os.path.join(folder_path, file_name)

    def play_surah_audio(self,chapter_id):
        if not os.path.exists(self.get_audio_path(chapter_id)):
            print("Audio file not found, downloading...")
            self.get_surah_audio(chapter_id,7)
            print("Audio file downloaded")
        player = vlc.MediaPlayer(self.get_audio_path(chapter_id))
        player.play()
        # Optional wait for the track to finish
        time.sleep(0.5)
        duration = player.get_length() / 1000
        time.sleep(duration)
        print("Audio playback complete")
        pass






test = SurahMedia()
test.get_reciter_list()

#print(test.reciter_dict['2'])#.get('7'))
#print(test.reciter_dict)

threads = []
for i in range(1, 115):
    t = threading.Thread(target=test.get_surah_audio, args=(i, 7))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
test.get_surah_audio(114,7)
#test.play_surah_audio(114)




# chapter_id = 114
# recitation_id = 7
# url = f"https://api.quran.com/api/v4/chapter_recitations/{recitation_id}/{chapter_id}"
# headers = {"Accept": "application/json"}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     data = response.json()
#     audio_url = data["audio_file"]["audio_url"]
#     audio_path = os.path.join(os.path.dirname(__file__), "quran_audio.mp3")

#     audio_response = requests.get(audio_url)
#     if audio_response.status_code == 200:
#         with open(audio_path, "wb") as f:
#             f.write(audio_response.content)

#         player = vlc.MediaPlayer(audio_path)
#         player.play()

#         # Optional wait for the track to finish
#         time.sleep(0.5)
#         duration = player.get_length() / 1000
#         time.sleep(duration)
#     else:
#         print(f"Failed to download audio file: {audio_response.status_code}")
# else:
#     print(f"Request failed: {response.status_code}")
