[app]
title = Missing Inventory Scanner
package.name = com.yourcompany.missingscanner
package.domain = com.yourcompany
source.dir = .
requirements = python3,kivy,kivymd,requests
icon.filename = assets/images/icon.png  ; REMINDER: You must place an icon here
orientation = portrait

# --- Crucial Android Permissions for App Functionality ---
android.permissions = \
    CAMERA, \
    INTERNET, \
    WRITE_EXTERNAL_STORAGE

# --- Android Build Settings ---
[android]
# Target modern Android API level for security and compatibility
android.api = 33 
min_sdk_version = 21

# Include dependencies for the ZBar scanner compilation
android.gradle_dependencies = \
    hostpython3, \
    zbar-dev 

# Required to include external modules like kivy-garden.zbarcam
android.gradle_dependencies = ['org.jni-libs:android-aarch64:0.0.1']
