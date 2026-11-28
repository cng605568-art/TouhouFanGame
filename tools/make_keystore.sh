#!/bin/sh
# Makes the Android signing key for the "Android" workflow and prints the
# base64 text to paste into a repository secret named ANDROID_KEYSTORE
# (Settings > Secrets and variables > Actions > New repository secret).
# With the secret set, every APK is signed with the same key, so updates
# install over the previous version. Keep the .keystore file somewhere safe
# and never commit it.
#
#   sh tools/make_keystore.sh [password]
#
# The password defaults to "android". If you pick another one, also add it
# as a secret named ANDROID_KEYSTORE_PASSWORD. Needs keytool (any JDK).
set -eu
pass="${1:-android}"
out="fumocourt-android.keystore"
keytool -genkeypair -keystore "$out" -alias android -keyalg RSA -keysize 2048 -validity 20000 \
    -storepass "$pass" -keypass "$pass" -dname "CN=Fumo Court, O=Fumo Court fan game, C=MY"
echo
echo "Wrote $out. ANDROID_KEYSTORE secret value:"
echo
base64 < "$out" | tr -d '\n'
echo
