[app]
title = Missing Inventory Scanner
package.name = com.yourcompany.missingscanner
package.domain = com.yourcompany
source.dir = .
version = 1.0
requirements = python3,kivy,kivymd,requests,kivy_garden.zbarcam,zbar

# Commented out to prevent errors if you haven't uploaded an image yet.
# icon.filename = assets/images/icon.png  

orientation = portrait

# --- Crucial Android Permissions ---
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE

# --- Android Build Settings ---
[android]
android.api = 33 
min_sdk_version = 21
android.accept_sdk_license = True

# Native dependencies for ZBar scanner
android.gradle_dependencies = 'org.jni-libs:android-aarch64:0.0.1'
