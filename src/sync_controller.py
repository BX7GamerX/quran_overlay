# sync_controller.py
import time

class SyncController:
    def __init__(self, text_widget, audio_player):
        self.text_widget = text_widget
        self.audio_player = audio_player
        self.running = False

    def start_sync(self):
        """
        Begins the periodic update of the text widget’s scroll position.
        """
        self.running = True
        self.update_scroll()

    def update_scroll(self):
        if not self.running:
            return
        current_time = self.audio_player.get_time()
        total_length = self.audio_player.get_length()
        if total_length <= 0:
            total_length = 1  # Avoid division by zero
        # Calculate fraction (0 to 1) of audio played.
        fraction = current_time / total_length
        # Update the text widget’s vertical scroll position.
        # yview_moveto accepts a fraction (0.0 to 1.0) where 0.0 is the top.
        self.text_widget.yview_moveto(fraction)
        # Schedule the next update after 100 ms.
        self.text_widget.after(100, self.update_scroll)

    def stop_sync(self):
        self.running = False
