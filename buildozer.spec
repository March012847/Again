[app]

title = SpotDL Downloader
package.name = spotdl_downloader
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,txt,mp3,json,xml,bin,sh,so

version = 1.0

# Main requirements:
requirements = python3,kivy,requests,mutagen,yt-dlp,syncedlyrics,spotdl,python-slugify,colorama,tqdm,platformdirs,websockets

# Include ffmpeg binaries
android.copy_files = ffmpeg/ffmpeg:ffmpeg, ffmpeg/ffprobe:ffprobe
android.add_src = ffmpeg

# Permissions for downloads + internet
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE

# Make ffmpeg runnable
android.allow_backup = 1
android.archive = False

# Kivy / SDL2 / Android API setup
android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.accept_sdk_license = True

fullscreen = 0
orientation = portrait
log_level = 2

android.enable_androidx = True
android.use_storage_framework = True

[buildozer]
log_level = 2
warn_on_root = 0