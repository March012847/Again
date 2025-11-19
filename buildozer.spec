[app]

title = SpotDL Downloader
package.name = spotdl_downloader
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,txt,mp3,json,xml,bin,sh,so

version = 1.0

# Main Python requirements for SpotDL behavior
requirements = python3,kivy,requests,mutagen,yt-dlp,syncedlyrics,spotdl,python-slugify,colorama,tqdm,platformdirs,websockets

# Copy ffmpeg binaries
android.copy_files = ffmpeg/ffmpeg:ffmpeg, ffmpeg/ffprobe:ffprobe
android.add_src = ffmpeg

# EXTERNAL STORAGE WRITE SUPPORT
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# Disable Android Storage Framework
android.use_storage_framework = False

# Allow legacy external storage write
android.extra_manifest_xml = <uses-permission android:name="android.permission.MANAGE_EXTERNAL_STORAGE" />
android.presplash_color = "#000000"

# Required for accessing /sdcard on Android 11+
android.extra_args = --preserve-file-permissions --use-legacy-storage

# API targets
android.api = 33
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.accept_sdk_license = True

orientation = portrait
fullscreen = 0
log_level = 2
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 0