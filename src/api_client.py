# api_client.py
import requests

# Base URL for the Quran.com API v4
API_BASE = "https://api.quran.com/api/v4"

def get_surah_list(language="en"):
    """
    Retrieves the list of surahs with translated names.
    """
    url = f"{API_BASE}/chapters?language={language}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Expecting a key "chapters" that contains the list
        return data.get("chapters", [])
    else:
        raise Exception(f"API error: {response.status_code}")

def get_surah_text(surah_id, edition="quran-uthmani"):
    """
    Retrieves the Arabic text of the specified surah.
    """
    url = f"{API_BASE}/surah/{surah_id}/{edition}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Assume the response contains a key "surah" with verse data
        return data.get("surah", {})
    else:
        raise Exception(f"API error: {response.status_code}")

def get_surah_translation(surah_id, edition="en.asad"):
    """
    Retrieves the English translation of the specified surah.
    """
    url = f"{API_BASE}/surah/{surah_id}/{edition}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("surah", {})
    else:
        raise Exception(f"API error: {response.status_code}")

def get_audio_url(surah_id, reciter="ar.alafasy"):
    """
    Retrieves the audio URL for the given surah and reciter.
    (For demonstration purposes, we return a dummy URL.)
    """
    # In a real implementation, you would call an endpoint that returns audio URLs.
    # Here, we simulate by returning a sample audio URL.
    # (Adjust the URL pattern as per actual API documentation.)
    return "http://cdn.alquran.cloud/media/audio/ayah/ar.alafasy/001001.mp3"
