
# Quran Overlay Recitation Player

An open‑source Python application that:
- Retrieves Quran text (both Arabic and translation) and audio recitations (default reciter: Mishary Alafasy) via the quran.com API.
- Presents the user with a surah selection screen.
- Displays a minimalist, transparent, always‑on‑top overlay that shows the surah text in a sleek black theme.
- Plays the recitation audio while autoscrolling the text in approximate sync (calculated based on the total duration and text length).
- Offers basic playback controls (pause/resume/stop) and the ability to return to surah selection.
- Provides an audio selector option so users can choose from alternative reciters if available.

---

## 1. Project Overview

### Objectives
- **Data Integration:**  
  Use the quran.com API to fetch both the “quran-uthmani” edition for Arabic text and an English translation edition (e.g. “en.asad”) so that both versions can be displayed. Additionally, retrieve word-level details (if available) to allow for potential fine‑tuning of autoscroll behavior.

- **Audio Playback:**  
  By default, play Mishary Alafasy’s recitation with the option to select alternate recitations through an audio selector.

- **Autoscrolling:**  
  Instead of relying on per‑word timing, calculate the scroll speed based on the overall audio duration and the total height (or length) of the text. This creates a smooth, continuous autoscroll that follows the recitation.

- **User Interface:**  
  Implement a minimalist design using CustomTkinter (a modern, customizable version of Tkinter) to ensure a sleek look and feel. The application will consist of:
  - A surah selection window.
  - An overlay window with a transparent, black minimalist design that displays the surah text.
  - Basic controls for playback (pause, resume, stop) and navigation (back to surah selection).

---

## 2. Requirements

### Libraries and Tools
- **HTTP and API Communication:**  
  - `requests` for RESTful API calls.
- **GUI Framework:**  
  - [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (which builds on standard Tkinter) for a modern, customizable, and minimalist interface.
- **Audio Playback:**  
  - [python‑vlc](https://www.olivieraubert.net/vlc/python-ctypes/) (or another suitable audio playback library) to stream and control recitation audio.
- **Time and Synchronization:**  
  - Standard Python modules like `time` and a timer class (e.g., `after()` method from Tkinter) for periodic GUI updates.
- **Optional:**  
  - JSON parsing (the built‑in `json` module) for handling API responses.
  - OS‑specific modules if needed (e.g., for always‑on‑top window management on Linux).

### API Sources
- **quran.com API (v4):**  
  Endpoints to retrieve:
  - Surah/chapter list and details  
    (see [quran.com API docs](https://api-docs.quran.com/docs/category/quran.com-api-4.0.0) citeturn0search8).
  - Verse data (with word‑level arrays for translation/transliteration).
  - Audio recitations (using the reciter “Mishary Alafasy” by default, with endpoints that return audio URLs).
- **Alternative:**  
  - [Al Quran Cloud API](https://alquran.cloud/api) if additional endpoints or formats are desired.  
    citeturn0search14

---

## 3. Application Architecture

### High-Level Workflow
1. **Surah Selection:**  
   - On launch, the application calls the quran.com API to retrieve the list of 114 surahs (with both Arabic and translation details).
   - A simple, minimalist surah selection interface is displayed using CustomTkinter.

2. **Data Retrieval:**  
   - Upon surah selection, the app retrieves:
     - The full text of the surah in Arabic (from “quran-uthmani”).
     - The English translation (from “en.asad” or similar).
     - The audio URL for Mishary Alafasy’s recitation.
     - (Optionally) word‑level breakdown for future synchronization refinement.

3. **Overlay and Playback:**  
   - An always‑on‑top overlay window is launched. It features a transparent, minimal black design.
   - The surah text is rendered in a scrollable text widget.
   - Audio playback is started (using python‑vlc or similar).
   - A timer calculates the required scroll speed based on the total audio duration and text widget height, then updates the scroll position periodically.

4. **Controls and Navigation:**  
   - Playback controls (pause, resume, stop) are provided.
   - An audio selector lets the user choose from alternative reciters.
   - A “back” control allows the user to exit the overlay and return to surah selection.

### Modular Code Structure
- **api_client.py:**  
  Functions to interface with the quran.com API. Responsibilities:
  - Fetch surah list and details.
  - Retrieve verse data (including optional word-level arrays).
  - Get audio URL based on the selected reciter.
- **gui.py:**  
  Implements the CustomTkinter-based user interface. Contains:
  - Surah selection screen.
  - Overlay window (with transparent, minimal black design).
  - Control widgets (buttons for pause/resume/stop, audio selector dropdown, back button).
- **audio_player.py:**  
  Wraps audio playback functionality using python‑vlc. Responsibilities:
  - Start, pause, resume, and stop audio.
  - Provide a method to query the current playback time.
- **sync_controller.py:**  
  Handles the synchronization between the audio playback and the scrolling text. Responsibilities:
  - Calculate the scroll increment based on audio duration and text widget dimensions.
  - Use a periodic timer (e.g. CustomTkinter’s `after()` method) to update the scroll position.
- **main.py:**  
  The entry point of the application. It:
  - Initializes the application.
  - Sets up logging, configuration, and error handling.
  - Coordinates transitions between the surah selection screen and the overlay playback screen.

---

## 4. Detailed Component Documentation

### 4.1 API Client
- **Functions:**
  - `get_surah_list(language="en")`:  
    Calls the chapters endpoint to return a list of surahs along with their Arabic names, translated names, verses count, etc.
  - `get_surah_text(surah_id, edition="quran-uthmani")`:  
    Retrieves full surah text in Arabic.
  - `get_surah_translation(surah_id, edition="en.asad")`:  
    Retrieves the English translation.
  - `get_audio_url(surah_id, reciter="ar.alafasy")`:  
    Retrieves the audio URL for the given surah and reciter (default reciter is Mishary Alafasy).  
- **Error Handling:**  
  Each function must gracefully handle API errors (e.g. network issues or invalid responses) and return useful error messages.

### 4.2 GUI Layer (Using CustomTkinter)
- **Surah Selection Window:**
  - **Layout:**  
    A simple list or grid of surah names (both Arabic and translated) in a minimalist design.
  - **Event Handling:**  
    On selection, the chosen surah ID is passed to the main controller.
- **Overlay Window:**
  - **Appearance:**  
    - Transparent background with a minimal black overlay.
    - Uses CustomTkinter window flags to remain always‑on‑top.
    - Minimal padding and margins so that only necessary space is used.
  - **Scrollable Text Widget:**  
    Displays the surah text. Supports programmatic scrolling.
  - **Control Panel:**  
    Contains:
    - A pause/resume button.
    - A stop button (to stop playback and return to surah selection).
    - An audio selector dropdown (populated with available reciters, defaulting to Mishary Alafasy).
- **Responsiveness and Minimalism:**  
  The UI should be responsive (resizing based on screen dimensions) while keeping the overall design minimal. CustomTkinter’s theming options will be used to enforce a sleek black-and‑transparent look.

### 4.3 Audio Playback Module
- **Using python‑vlc:**
  - **Initialization:**  
    Create a VLC media player instance that streams the audio from the URL.
  - **Playback Controls:**  
    Functions to play, pause, resume, and stop audio.
  - **Time Query:**  
    A method to retrieve the current playback time so that the sync controller can calculate scroll position.
- **Error Handling:**  
  Manage potential playback issues (e.g., network interruptions, unsupported audio formats).

### 4.4 Synchronization Controller
- **Calculation of Scroll Increment:**
  - Retrieve the total duration of the audio.
  - Determine the total scrollable height of the text widget.
  - Compute a scroll rate (pixels per second) that, over the audio’s duration, moves the scroll from the beginning to the end.
- **Timer Implementation:**
  - Use a recurring timer (via `after()` in CustomTkinter) to update the scroll position periodically (for example, every 100 ms).
  - The controller must check if the audio is paused or stopped and adjust updates accordingly.
- **User Intervention:**
  - If the user manually scrolls or pauses/resumes, the synchronization logic should adapt (for instance, pausing the autoscroll when playback is paused).

### 4.5 Application Flow (main.py)
- **Startup:**
  - Initialize the API client, GUI, and audio playback modules.
  - Display the surah selection window.
- **Upon Surah Selection:**
  - Retrieve text and translation for the selected surah.
  - Fetch the corresponding audio URL (defaulting to Mishary Alafasy but allowing user selection via the audio selector).
  - Close the surah selection window and open the overlay.
- **During Playback:**
  - Start the audio player.
  - Start the synchronization timer to autoscroll the text widget.
  - Monitor control inputs (pause/resume/stop, audio selector changes).
- **On Stop/Exit:**
  - Stop audio playback.
  - Cancel the synchronization timer.
  - Return to the surah selection screen or exit the application.

---

## 5. Installation and Setup

### Dependencies
- Python 3.8 or higher.
- Install required packages via pip:
  ```bash
  pip install requests customtkinter python-vlc
  ```
  (You might also need to install VLC media player on your system for python‑vlc to work properly.)

### Configuration
- API endpoint URLs and default edition IDs (e.g., `"quran-uthmani"` for Arabic, `"en.asad"` for English) can be set in a configuration file (e.g., `config.json`) or as constants in the code.
- Optionally, configure the list of reciters for the audio selector.

### Running the Application
- From the command line, run:
  ```bash
  python main.py
  ```
- The surah selection window should appear. Upon selecting a surah, the overlay window will launch and the recitation will start with synchronized autoscrolling.

---

## 6. Future Extensions and Considerations

- **Advanced Synchronization:**  
  If word‑level timing data becomes reliably available, the autoscroll could be further refined to scroll precisely to each word as it is recited.
- **User Preferences:**  
  Save user settings (e.g., chosen reciter, font size, overlay transparency) between sessions.
- **Multi‑Language Support:**  
  Extend the overlay to allow toggling between different translations or displaying both languages simultaneously.
- **Enhanced Controls:**  
  Add volume control, seek functionality (jump to a specific time in the recitation), and customizable scroll speeds.
- **Modular Extensibility:**  
  The modular design enables adding support for additional audio sources or alternative APIs (e.g., integrating with Al Quran Cloud) with minimal code changes.

---

## 7. Summary

This documentation provides a complete blueprint for your Quran Overlay Recitation Player project:

- **Data and API Integration:** Uses quran.com API endpoints to retrieve surah text, translations, and audio recitations.
- **GUI:** Built using CustomTkinter for a modern, minimalist, transparent overlay that is always on top.
- **Audio and Synchronization:** Employs python‑vlc for playback and calculates scroll speed based on audio duration and text height.
- **Controls:** Implements basic playback controls and an audio selector for user flexibility.
- **Modular Design:** Organized into separate modules for API handling, GUI, audio playback, synchronization, and main control.

Developers can use this documentation to build the project step‑by‑step while having a clear understanding of the underlying architecture and design decisions.

