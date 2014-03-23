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
PY4A_MODULES := "plyer openssl pyjnius kivy"

# Android SDK setting


# Android settings
APK_PACKAGE := org.drpexe.sigmawebplus
APP_NAME := "SigmaWeb+"
APK_NAME := SigmaWebPlus
APK_VERSION := 0.1
APK_ORIENTATION := portrait
APK_ICON := $(PROJECT_DIR)/res/udesc.png
APK_PRESPLASH := $(PROJECT_DIR)/res/udesc_background.png
APK_DEBUG := $(PYTHON_FOR_ANDROID_PACKAGE)/bin/$(APK_NAME)-$(APK_VERSION)-debug.apk
APK_RELEASE := $(PYTHON_FOR_ANDROID_PACKAGE)/bin/$(APK_NAME)-$(APK_VERSION)-release-unsigned.apk
APK_FINAL := $(PYTHON_FOR_ANDROID_PACKAGE)/bin/$(APK_NAME).apk
APK_ALIAS := sigmaplus
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
	rm $(VENV) -r
	sudo rm python-for-android -r

.PHONY: android
android:
	source env_var.sh; \
	cd $(PYTHON_FOR_ANDROID_PACKAGE); \
	$(PY) ./build.py --package $(APK_PACKAGE) --name $(APP_NAME) --version $(APK_VERSION) --orientation $(APK_ORIENTATION) --icon $(APK_ICON) --presplash $(APK_PRESPLASH) --dir $(PROJECT_DIR) $(APK_PERMISSIONS) debug installd

.PHONY: logcat
logcat:
	source env_var.sh; \
	adb logcat python:I *:S

# Setup
.PHONY: installenv
installenv:
	sudo rm $(VENV) -r -f
	sudo rm python-for-android -r -f
	sudo apt-get install build-essential patch git-core ccache ant python-pip python-dev
	sudo apt-get install ia32-libs  libc6-dev-i386
	pip install virtualenv
	sudo virtualenv -p python2.7 --system-site-packages $(VENV)
	$(PIP) install kivy
	$(PIP) install cython
	git clone git://github.com/kivy/python-for-android
	chmod +x env_var.sh

.PHONY: createdist
createdist:
	source env_var.sh; \
	source "$(VENV)/bin/activate"; \
	cd $(PYTHON_FOR_ANDROID); \
	./distribute.sh -m $(PY4A_MODULES)

.PHONY: install
install: installenv createdist
