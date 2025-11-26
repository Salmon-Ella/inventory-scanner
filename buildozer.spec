[app]
title = Missing Inventory Scanner
package.name = com.yourcompany.missingscanner
package.domain = com.yourcompany
source.dir = .
# Added 'zbar' explicitly to requirements to ensure the scanner library loads
requirements = python3,kivy,kivymd,requests,kivy_garden.zbarcam,zbar
icon.filename = assets/images/icon.png
orientation = portrait

# --- Crucial Android Permissions ---
android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE

# --- Android Build Settings ---
[android]
# Target modern Android API level
android.api = 33 
min_sdk_version = 21

# FIXED: Merged dependencies into a single line (removed the duplicate)
# This includes the ZBar native library reference
android.gradle_dependencies = 'org.jni-libs:android-aarch64:0.0.1'
