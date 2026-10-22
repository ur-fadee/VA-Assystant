import pyautogui
import pyttsx3
import speech_recognition as sr
import subprocess
import datetime
import sys
import webbrowser
import time
import psutil

width, height = pyautogui.size()

sites = {
    "google": "https://www.google.com/search?q=",
    "youtube": "https://www.youtube.com/results?search_query=",
    "wikipedia": "https://en.wikipedia.org/wiki/",
    "reddit": "https://www.reddit.com/search?q=",
    "twitch": "https://www.twitch.tv/search?q=",
    "x": "https://x.com/search?q="
}

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()
    del engine

recognizer = sr.Recognizer()
recognizer.energy_threshold = 4000
recognizer.dynamic_energy_threshold = True

def listen():
    with sr.Microphone() as microphone:
        try:
            audio = recognizer.listen(
                microphone,
                timeout=5,
                phrase_time_limit=5
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return ""

def process_command(command):
    if not command:
        return True

    if not "computer" in command:
        return

    elif command == "computer":
        speak("Sir?")
        return True

    elif "computer" in command and "what time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time} sir")

    elif "computer" in command and "open application" in command:
        appName = command.replace("computer open application", "")
        subprocess.Popen(["open", "-a", appName.strip()])
        speak(f"Opening {appName}")

    elif "computer" in command and "close application" in command:
        app_name = command.replace("computer close application", "").strip()

        for proc in psutil.process_iter(["cmdline"]):
            try:
                cmdline = proc.info["cmdline"]

                if cmdline:
                    cmd = " ".join(cmdline)

                    if app_name.lower() in cmd.lower():
                        proc.kill()
                        speak(f"Closing {app_name}")
                        break

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    elif "computer" in command and "search for" in command:
        search = command[19:]

        for site in sites:
            webbrowser.open(sites[site] + search)

        speak("Searching for " + search)

    elif "computer" in command and "delete browsing history" in command:
        subprocess.Popen(["open", "-a", "Google Chrome"])
        time.sleep(5)
        pyautogui.hotkey("command", "shift", "backspace")

        my_x = 921
        my_y = 798
        my_width = 1512
        my_height = 982
        x_percent = my_x / my_width
        y_percent = my_y / my_height

        actual_width, actual_height = pyautogui.size()
        target_x = actual_width * x_percent
        target_y = actual_height * y_percent

        pyautogui.moveTo(target_x, target_y)
        pyautogui.click()
        speak("Browsing data deleted sir")

    elif "computer" in command and "quit" in command:
        sys.exit()

    else:
        speak("Sorry sir, I did not recognize that command.")

    return True

with sr.Microphone() as microphone:
    recognizer.adjust_for_ambient_noise(microphone, duration=2)

hour = datetime.datetime.now().hour

if hour <= 11:
    speak("Good morning sir")
elif hour <= 16:
    speak("Good afternoon sir")
elif hour <= 22:
    speak("Good evening sir")
else:
    speak("Hello sir")

while True:
    command = listen()
    process_command(command)