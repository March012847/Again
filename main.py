# main.py
import os
import threading
import sys
from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread

import yt_dlp
import spotdl
from mutagen.mp3 import MP3

# Determine ffmpeg path
if getattr(sys, 'getandroidapilevel', False):
    FFMPEG_PATH = os.path.join(os.getcwd(), "libs/ffmpeg/ffmpeg")
else:
    FFMPEG_PATH = "ffmpeg"  # fallback for desktop

class DownloaderApp(App):

    def build(self):
        self.title = "SpotDL Downloader"

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input for Spotify/YouTube URL
        self.url_input = TextInput(
            hint_text="Enter Spotify/YouTube URL",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        root.add_widget(self.url_input)

        # Download button
        self.download_btn = Button(
            text="Download",
            size_hint_y=None,
            height=50,
            on_press=self.start_download
        )
        root.add_widget(self.download_btn)

        # Scrollable log area
        self.log_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.log_layout)
        root.add_widget(scroll)

        return root

    def log(self, message):
        """Thread-safe logging to UI."""
        @mainthread
        def update():
            label = Label(text=message, size_hint_y=None, height=30)
            self.log_layout.add_widget(label)
        update()

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.log("⚠️ No URL entered.")
            return
        self.download_btn.disabled = True
        threading.Thread(target=self.download_song, args=(url,), daemon=True).start()

    def download_song(self, url):
        """Download using spotdl/yt-dlp in background thread."""
        try:
            self.log(f"⬇️ Starting download: {url}")

            # Output directory
            output_dir = os.path.join(os.getcwd(), "downloads")
            os.makedirs(output_dir, exist_ok=True)

            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': True,
                'progress_hooks': [self.ydl_hook],
                'ffmpeg_location': FFMPEG_PATH,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.log("✅ Download finished.")

        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
        finally:
            self.download_btn.disabled = False

    def ydl_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total else 0
            self.log(f"⬇️ {d.get('filename','')}: {percent:.1f}%")
        elif d['status'] == 'finished':
            self.log(f"✅ Finished {d.get('filename','')}")


if __name__ == "__main__":
    DownloaderApp().run()