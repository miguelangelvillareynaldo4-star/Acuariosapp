[app]

# Application metadata
title = AcuarioApp
package.name = acuarioapp
package.domain = com.aquarium.app

# Source files
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
platform = android
orientation = portrait

# Build settings
log_level = 2
android.api = 34
android.minapi = 21
android.archs = arm64-v8a
android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.enable_androidx = True
android.gradle_dependencies = com.google.android.material:material:1.11.0

# Python dependencies
requirements = python3,kivy==2.3.1,kivymd==2.0.0rc4,pillow==10.4.0,plyer==2.1.0

# Versioning
version = 0.1.0
android.numeric_version = 1

# Debug build
debug = True
