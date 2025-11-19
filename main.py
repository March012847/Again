import os
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

from syncedlyrics import search_lyrics
from yt_dlp import YoutubeDL


ROOT = os.getcwd()
DOWNLOAD_DIR = os.path.join(ROOT, "downloads")
OSPY = "python3"  # Android python runtime alias injected by Buildozer

FFMPEG = os.path.join(ROOT, "ffmpeg", "ffmpeg")
FFPROBE = os.path.join(ROOT, "ffmpeg", "ffprobe")


class DownloaderUI(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)

        self.url_input = TextInput(
            hint_text="Paste Spotify or YouTube URL",
            multiline=False,
            size_hint_y=None,
            height=45
        )
        self.add_widget(self.url_input)

        self.log_label = Label(
            text="Ready.",
            size_hint_y=None,
            height=200
        )
        self.add_widget(self.log_label)

        dl_btn = Button(
            text="Download",
            size_hint_y=None,
            height=50
        )
        dl_btn.bind(on_press=self.start_download)
        self.add_widget(dl_btn)

    def log(self, msg):
        self.log_label.text = msg
        print(msg)

    def start_download(self, *args):
        url = self.url_input.text.strip()
        if not url:
            self.log("No URL provided.")
            return

        thread = threading.Thread(target=self.download_handler, args=(url,))
        thread.start()

    # MAIN LOGIC
    def download_handler(self, url):

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        if "spotify.com" in url:
            self.log("Detected Spotify URL → Using SpotDL...")
            mp3_path = self.download_spotify(url)
        else:
            self.log("Detected YouTube URL → Using yt-dlp...")
            mp3_path = self.download_youtube(url)

        if not mp3_path:
            self.log("Download failed.")
            return

        self.log("Fetching synced lyrics...")
        name = os.path.splitext(os.path.basename(mp3_path))[0]

        try:
            lrc = search_lyrics(name)
            if lrc:
                with open(os.path.join(DOWNLOAD_DIR, name + ".lrc"), "w", encoding="utf-8") as f:
                    f.write(lrc)
                self.log("LRC saved.")
            else:
                self.log("No synced lyrics found.")
        except Exception as e:
            self.log(f"LRC error: {e}")

        self.log("Done.")

    # YOUTUBE METHOD
    def download_youtube(self, url):
        self.log("Downloading via yt-dlp...")

        pattern = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
        opts = {
            "format": "bestaudio/best",
            "outtmpl": pattern,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "ffmpeg_location": FFMPEG
        }

        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "track")
                return os.path.join(DOWNLOAD_DIR, f"{title}.mp3")
        except Exception as e:
            self.log(f"yt-dlp ERROR: {e}")
            return None

    # SPOTDL METHOD
    def download_spotify(self, url):
        self.log("Downloading via SpotDL...")

        # SpotDL output will go to the working directory, so set CWD
        cmd = [
            OSPY,      # Buildozer's python runtime inside APK
            "-m", "spotdl",
            "download",
            "--ffmpeg", FFMPEG,
            "--output", os.path.join(DOWNLOAD_DIR, "{title}.{ext}"),
            url
        ]

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in proc.stdout:
                self.log(line.strip())

            proc.wait()
        except Exception as e:
            self.log(f"SpotDL ERROR: {e}")
            return None

        # Find MP3 result
        try:
            for f in os.listdir(DOWNLOAD_DIR):
                if f.endswith(".mp3"):
                    return os.path.join(DOWNLOAD_DIR, f)
        except:
            pass

        return None


class SpotDLApp(App):
    def build(self):
        return DownloaderUI()


if __name__ == "__main__":
    SpotDLApp().run()