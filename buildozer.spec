[app]
title = Missing Inventory Scanner
package.name = com.yourcompany.missingscanner
package.domain = com.yourcompany
source.dir = .
version = 1.0

# FIXED: Swapped 'zbar' (hard to compile) for 'pyzbar' (easier)
# Added 'pillow' for image processing
requirements = python3,kivy,kivymd,requests,kivy_garden.zbarcam,pyzbar,pillow

orientation = portrait

# --- Crucial Android Permissions ---
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE

# --- Android Build Settings ---
[android]
android.api = 33
min_sdk_version = 21
android.accept_sdk_license = True

# Pin build tools to avoid license errors
android.sdk_build_tools_version = 34.0.0

# Native dependencies for ZBar scanner (No quotes)
android.gradle_dependencies = org.jni-libs:android-aarch64:0.0.1
