# Project settings
SHELL := /bin/bash
WD := $(shell pwd)
PROJECT_DIR := $(WD)/source
VENV := $(WD)/venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

# Python for Android settings
PYTHON_FOR_ANDROID := $(WD)/python-for-android
PYTHON_FOR_ANDROID_PACKAGE := $(PYTHON_FOR_ANDROID)/dist/default
PY4A_MODULES := "plyer openssl pyjnius kivy lxml"

# Android SDK setting


# Android settings
APK_PACKAGE := org.drpexe.sigmawebplus
APP_NAME := "SigmaWeb+"
APK_NAME := SigmaWeb+
APK_VERSION := "0.2"
APK_ORIENTATION := portrait
APK_ICON := $(PROJECT_DIR)/res/udesc.png
APK_PRESPLASH := $(PROJECT_DIR)/res/udesc_background.png
APK_DEBUG := $(PYTHON_FOR_ANDROID_PACKAGE)/bin/$(APK_NAME)-$(APK_VERSION)-debug.apk
APK_RELEASE := $(PYTHON_FOR_ANDROID_PACKAGE)/bin/$(APK_NAME)-$(APK_VERSION)-release-unsigned.apk
APK_FINAL := $(WD)/release/$(APK_NAME).apk
APK_KEYSTORE := ~/Dropbox/Pessoal/Backup/Android-Keys/org-drpexe-sigmawebplus-release-key.keystore
APK_ALIAS := sigmawebplus
APK_PERMISSIONS = --permission INTERNET

# Run
.PHONY: run
run:
	cd $(PROJECT_DIR); \
	$(PY) main.py

.PHONY: inspect
inspect:
	cd $(PROJECT_DIR); \
	$(PY) main.py -m inspector

.PHONY: distclean
distclean:
	sudo rm $(VENV) -r -f
	sudo rm python-for-android -r -f

.PHONY: android
android:
	source env_var.sh; \
	cd $(PYTHON_FOR_ANDROID_PACKAGE); \
	$(PY) ./build.py --package $(APK_PACKAGE) --name $(APP_NAME) --version $(APK_VERSION) --orientation $(APK_ORIENTATION) --icon $(APK_ICON) --presplash $(APK_PRESPLASH) --dir $(PROJECT_DIR) $(APK_PERMISSIONS) debug installd

.PHONY: logcat
logcat:
	source env_var.sh; \
	adb logcat python:I *:S

.PHONY: logcat_all
logcat_all:
	source env_var.sh; \
	adb logcat *:I

# Setup

.PHONY: install_venv
install_venv:
	sudo apt-get install python-pip -y
	sudo pip install virtualenv
	virtualenv -p python2.7 --system-site-packages $(VENV)

.PHONY: install_pipmodules
install_pipmodules:
	sudo apt-get install python-notify2 -y
	sudo apt-get install python-setuptools python-pygame python-opengl python-gst0.10 python-enchant gstreamer0.10-plugins-good libgl1-mesa-dev-lts-quantal libgles2-mesa-dev-lts-quantal -y
	sudo apt-get install build-essential patch git-core ccache ant python-pip python-dev -y
	#sudo apt-get install ia32-libs libc6-dev-i386 -y
	$(PIP) install cython
	$(PIP) install kivy

.PHONY: install_pythonforandroid
install_pythonforandroid:
	git clone git://github.com/kivy/python-for-android
	sudo chmod +x env_var.sh

.PHONY: createdist
createdist:
	source env_var.sh; \
	source "$(VENV)/bin/activate"; \
	cd $(PYTHON_FOR_ANDROID); \
	./distribute.sh -m $(PY4A_MODULES)

.PHONY: install
install: distclean install_venv install_pipmodules install_pythonforandroid createdist

.PHONY: android_release
android_release:
	source env_var.sh; \
	cd $(PYTHON_FOR_ANDROID_PACKAGE); \
	$(PY) ./build.py --package $(APK_PACKAGE) --name $(APP_NAME) --version $(APK_VERSION) --orientation $(APK_ORIENTATION) --icon $(APK_ICON) --presplash $(APK_PRESPLASH) --dir $(PROJECT_DIR) $(APK_PERMISSIONS) release
	make sign_android

.PHONY: sign_android
sign_android:
	rm -f $(APK_FINAL)
	jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore $(APK_KEYSTORE) $(APK_RELEASE) $(APK_ALIAS)
	source env_var.sh; \
	zipalign -v 4 $(APK_RELEASE) $(APK_FINAL)
