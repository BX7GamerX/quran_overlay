# gui.py
import customtkinter as ctk
import tkinter as tk
from api_client import get_surah_list, get_surah_text, get_surah_translation, get_audio_url
from audio_player import AudioPlayer
from sync_controller import SyncController

class SurahSelection(ctk.CTk):
    def __init__(self, on_surah_selected_callback):
        super().__init__()
        self.title("Select Surah")
        self.geometry("400x600")
        self.on_surah_selected_callback = on_surah_selected_callback
        self.surah_list = []
        self.listbox = tk.Listbox(self, font=("Helvetica", 12))
        self.listbox.pack(fill="both", expand=True, padx=20, pady=20)
        self.listbox.bind("<<ListboxSelect>>", self.surah_selected)
        self.fetch_surahs()

    def fetch_surahs(self):
        try:
            self.surah_list = get_surah_list(language="en")
            for surah in self.surah_list:
                display_text = f"{surah.get('id', '')}. {surah.get('translated_name', {}).get('name', '')} ({surah.get('name_arabic', '')})"
                self.listbox.insert(tk.END, display_text)
        except Exception as e:
            print("Error fetching surahs:", e)

    def surah_selected(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            surah = self.surah_list[index]
            surah_id = surah.get("id")
            self.on_surah_selected_callback(surah_id)
            self.destroy()

class OverlayWindow(ctk.CTkToplevel):
    def __init__(self, surah_id):
        super().__init__()
        self.title("Surah Overlay")
        self.geometry("800x200")
        # Always-on-top and transparency settings.
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.8)  # 80% opaque
        self.configure(bg="black")
        
        # Frame for text display
        self.text_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=0)
        self.text_frame.pack(fill="both", expand=True)
        
        # Scrollable text widget (using standard Tkinter Text widget)
        self.text_widget = tk.Text(self.text_frame, bg="black", fg="white",
                                   font=("Helvetica", 18), bd=0, highlightthickness=0)
        self.text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Insert surah text (Arabic and translation)
        self.insert_surah_text(surah_id)
        
        # Control panel frame
        self.control_frame = ctk.CTkFrame(self, fg_color="black", corner_radius=0)
        self.control_frame.pack(fill="x", padx=10, pady=(0,10))
        self.pause_button = ctk.CTkButton(self.control_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=5)
        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop", command=self.stop_playback)
        self.stop_button.pack(side="left", padx=5)
        # Audio selector dropdown (placeholder – can be expanded as needed)
        self.audio_var = tk.StringVar(value="Mishary Alafasy")
        self.audio_selector = ctk.CTkOptionMenu(self.control_frame, variable=self.audio_var,
                                                 values=["Mishary Alafasy", "Other Reciter"])
        self.audio_selector.pack(side="left", padx=5)
        self.back_button = ctk.CTkButton(self.control_frame, text="Back", command=self.close_overlay)
        self.back_button.pack(side="right", padx=5)
        
        # Initialize audio player and start playback
        self.audio_player = AudioPlayer()
        # Get the audio URL for the selected surah and reciter (default: Mishary Alafasy)
        self.audio_url = get_audio_url(surah_id, reciter="ar.alafasy")
        self.audio_player.play(self.audio_url)
        
        # Start synchronization of autoscroll with audio playback
        self.sync_controller = SyncController(self.text_widget, self.audio_player)
        self.sync_controller.start_sync()
        
        self.paused = False

    def insert_surah_text(self, surah_id):
        try:
            # Fetch Arabic text and English translation.
            surah_ar = get_surah_text(surah_id, edition="quran-uthmani")
            surah_en = get_surah_translation(surah_id, edition="en.asad")
            # For demonstration, assume each surah response contains a "verses" key with a list of verses.
            arabic_text = "\n".join([verse.get("text", "") for verse in surah_ar.get("verses", [])])
            english_text = "\n".join([verse.get("text", "") for verse in surah_en.get("verses", [])])
            full_text = arabic_text + "\n\n" + english_text
            self.text_widget.insert(tk.END, full_text)
            self.text_widget.config(state="disabled")
        except Exception as e:
            self.text_widget.insert(tk.END, f"Error loading surah text: {e}")

    def toggle_pause(self):
        if self.paused:
            self.audio_player.pause()  # Resume playback
            self.pause_button.configure(text="Pause")
            self.paused = False
        else:
            self.audio_player.pause()  # Pause playback (toggle behavior)
            self.pause_button.configure(text="Resume")
            self.paused = True

    def stop_playback(self):
        self.audio_player.stop()
        self.sync_controller.stop_sync()

    def close_overlay(self):
        self.stop_playback()
        self.destroy()
