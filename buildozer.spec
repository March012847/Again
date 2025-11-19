[app]

# Application info
title = SpotDL Downloader
package.name = spotdl_downloader
package.domain = org.example
source.dir = .
entrypoint = main.py
version = 1.0.0

# Include all source files
source.include_exts = py,png,jpg,kv,txt

# Orientation
orientation = portrait

# Android SDK/NDK
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21

# Architectures
android.arch = arm64-v8a, armeabi-v7a

# Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Kivy + Python requirements
requirements = python3,kivy,yt-dlp,spotdl,mutagen

# Fullscreen
fullscreen = 0

# Assets folder
android.copy_assets = True

# Logging
log_level = 2

# Use AndroidX
android.use_androidx = True

# Presplash/Icon (optional)
presplash.filename = presplash.png
icon.filename = icon.png