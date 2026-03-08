#!/usr/bin/env python3
"""
Lumo Desktop Agent – Automation Backend
Executes OS commands from natural language prompts.
Supports Windows, macOS, and Linux.
"""

import os
import sys
import re
import subprocess
import webbrowser
import platform
import time
import pyautogui
from datetime import datetime
from urllib.parse import quote
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import psutil
import ctypes
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

# ----------------------------------------------------------------------
# OS detection
# ----------------------------------------------------------------------
IS_WINDOWS = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'
IS_LINUX = platform.system() == 'Linux'

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def open_application(app_name):
    """Open a system application by name."""
    app = app_name.lower().strip()

    # Notepad (Windows only)
    if 'notepad' in app:
        if IS_WINDOWS:
            subprocess.Popen(['notepad.exe'])
            return "📝 Notepad is open! Ready for some writing! ✍️"
        return "Sorry, I can only open Notepad on Windows! 😅"

    # Calculator (cross-platform)
    if 'calculator' in app or 'calc' in app:
        if IS_WINDOWS:
            subprocess.Popen(['calc.exe'])
        elif IS_MAC:
            subprocess.Popen(['open', '-a', 'Calculator'])
        elif IS_LINUX:
            # Try common Linux calculator names
            for calc in ['gnome-calculator', 'kcalc', 'qalculate-gtk']:
                try:
                    subprocess.Popen([calc])
                    break
                except FileNotFoundError:
                    continue
            else:
                return "Couldn't find a calculator app on your system! 🤷‍♂️"
        return "🧮 Calculator is ready! Time to crunch some numbers! 🔢"

    # Chrome / Google Chrome
    if 'chrome' in app or 'google chrome' in app:
        if IS_WINDOWS:
            # Common Chrome paths
            paths = [
                r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            ]
            for path in paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return "🌐 Chrome is opening! Ready to browse the web! 🚀"
            return "Hmm, couldn't find Chrome on your system! 🤔"
        elif IS_MAC:
            subprocess.Popen(['open', '-a', 'Google Chrome'])
            return "🌐 Chrome is opening! Ready to browse the web! 🚀"
        elif IS_LINUX:
            try:
                subprocess.Popen(['google-chrome'])
                return "🌐 Chrome is opening! Ready to browse the web! 🚀"
            except FileNotFoundError:
                return "Hmm, couldn't find Chrome on your system! 🤔"

    # Generic fallback – try to run as a command
    try:
        subprocess.Popen([app])
        return f"🚀 I've tried to open '{app}'! Hope it works! 😊"
    except FileNotFoundError:
        return f"Sorry, I don't know how to open '{app}'! 🤷‍♂️"

def execute_system_command(cmd):
    """Run a system command and return its output (safe only)."""
    # Block dangerous commands
    dangerous = ['rm', 'del', 'format', 'shutdown', 'reboot', 'sudo']
    if any(d in cmd.lower() for d in dangerous):
        return "Command blocked for safety reasons."

    try:
        # Use shell=True to support commands like 'dir' or 'ls'
        result = subprocess.run(cmd, shell=True,
                                capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
        return output if output.strip() else "Command executed (no output)."
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error: {e}"

def create_folder(folder_name):
    """Create a folder (supports paths relative to current directory)."""
    folder_name = folder_name.strip('\'"')
    try:
        os.mkdir(folder_name)
        return f"📁 Yay! I've created the folder '{folder_name}' for you! 🎉"
    except FileExistsError:
        return f"Oops! The folder '{folder_name}' already exists! 😅"
    except Exception as e:
        return f"Sorry, I had trouble creating that folder! 🤷‍♂️ Error: {e}"

def list_files(path=None):
    """List files in a directory. Defaults to current directory."""
    if path is None:
        path = os.getcwd()
    try:
        items = os.listdir(path)
        if items:
            return f"📂 Here's what I found in your folder:\n\n" + "\n".join(items) + "\n\nAnything specific you'd like to do with these files? 😊"
        else:
            return "📂 This folder is empty! Want me to help you create something? 🎨"
    except Exception as e:
        return f"Sorry, I couldn't list the files! 🤷‍♂️ Error: {e}"

def write_in_notepad(text):
    """Open Notepad and type: given text (Windows only)."""
    if not IS_WINDOWS:
        return "Sorry, I can only write letters on Windows with Notepad! 😅"
    
    # Generate a friendly letter if no specific content provided
    if not text or text in ['a letter', 'letter', '']:
        text = generate_friendly_letter()
    else:
        # If user provided specific content, create a letter with that content
        text = f"""Dear Friend,

{datetime.now().strftime("%B %d, %Y")}

{text}

Hope you're doing well! 

Your digital friend,
Lumo 🤖

P.S. Thanks for letting me help you today! 😊"""
    
    try:
        # Open Notepad
        subprocess.Popen(['notepad.exe'])
        time.sleep(2.0)                     # Wait for Notepad to open
        
        # Focus on Notepad window
        import pygetwindow as gw
        notepad_windows = gw.getWindowsWithTitle('Notepad')
        if notepad_windows:
            notepad_windows[0].activate()
            time.sleep(0.5)
        
        # Type the letter
        pyautogui.write(text, interval=0.02)
        return f"✨ I've opened Notepad and written your letter! Check it out! 😊"
        
    except Exception as e:
        return f"😅 Oops! I had trouble writing the letter: {str(e)}"

def generate_friendly_letter():
    """Generate a friendly, conversational letter."""
    from datetime import datetime
    current_date = datetime.now().strftime("%B %d, %Y")
    
    return f"""Dear Friend,

{current_date}

I hope this letter finds you well! I wanted to reach out and say hello. 

Life has been pretty interesting lately - I've been helping with all sorts of tasks, from opening applications to writing letters just like this one! It's amazing what we can do with a little bit of technology and creativity.

How have you been? I'd love to hear about what you've been up to lately. Whether it's work, hobbies, or just enjoying the simple things in life, every story is worth sharing.

Remember, if you ever need help with anything - whether it's writing another letter, opening an app, or just having a chat - I'm here for you!

Take care and stay awesome!

Your digital friend,
Lumo 🤖

P.S. Thanks for letting me help you today! It makes me happy to be useful. 😊"""

# ----------------------------------------------------------------------
# Enhanced web automation
# ----------------------------------------------------------------------
def play_youtube_video(command):
    # Clean command
    query = command.lower()
    query = query.replace("open chrome", "")
    query = query.replace("search", "")
    query = query.replace("play", "")
    query = query.replace("on youtube", "")
    query = query.replace("youtube", "")
    query = query.replace("video", "")
    query = query.strip()

    if query == "":
        return "Please specify what you want to search for on YouTube! 😊"

    encoded_query = urllib.parse.quote(query)

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service("chromedriver.exe")  # make sure chromedriver.exe is in project folder

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Open YouTube search page
        driver.get(f"https://www.youtube.com/results?search_query={encoded_query}")

        # Wait for page to load
        time.sleep(5)

        # Try multiple selectors to find the first video
        videos = None
        selectors = [
            "a#video-title",
            "a.yt-simple-endpoint.style-scope.ytd-video-renderer",
            "#video-title",
            "ytd-video-renderer a#video-title",
            "[id='video-title']"
        ]
        
        for selector in selectors:
            try:
                videos = driver.find_elements(By.CSS_SELECTOR, selector)
                if videos:
                    break
            except:
                continue

        if videos and len(videos) > 0:
            # Click the first video
            driver.execute_script("arguments[0].click();", videos[0])
            
            # Wait for video to load
            time.sleep(3)
            
            # Try to click play button if video doesn't auto-play
            try:
                play_button = driver.find_element(By.CSS_SELECTOR, "button.ytp-play-button")
                if play_button:
                    driver.execute_script("arguments[0].click();", play_button)
            except:
                pass
            
            return f"🎬 Successfully opened YouTube and playing '{query}'! 🎥\n\n🎶 Video is now playing in Chrome! 🚀"
        else:
            return f"😅 No video found for '{query}'. Try a different search! 🤷‍♂️"

    except Exception as e:
        # Fallback to webbrowser method
        webbrowser.open(f"https://www.youtube.com/results?search_query={encoded_query}")
        time.sleep(5)
        pyautogui.press("tab", presses=5)
        pyautogui.press("enter")
        return f"🎬 Using fallback method for '{query}'! 🎥\n\n🎶 Video should start playing! 🚀"

def open_url(url):
    """Open a URL in the default browser."""
    if not url.startswith(('http://', 'https://')):
        if '.' in url and ' ' not in url:
            url = 'https://' + url
        else:
            # Treat as a search query using Google
            url = 'https://www.google.com/search?q=' + quote(url)
    webbrowser.open(url)
    return f"🌐 Opened {url}! 🚀"

def search_youtube(query):
    """Search YouTube for a query and open the results."""
    search_url = "https://www.youtube.com/results?search_query=" + quote(query)
    webbrowser.open(search_url)
    return f"🔍 Searching YouTube for '{query}'! 🎬"

def search_google(query):
    """Perform a Google search."""
    search_url = "https://www.google.com/search?q=" + quote(query)
    webbrowser.open(search_url)
    return f"🔍 Searching Google for '{query}'! 🌐"

def open_youtube_home():
    webbrowser.open("https://www.youtube.com")
    return "🌐 Opened YouTube! Ready to watch some videos! 🎬"

def open_and_play_youtube(song_query):
    """
    Open YouTube and search for the song. (Could be extended to play first result.)
    """
    return search_youtube(song_query)

def open_site_and_search(site, query):
    """
    Open a specific site (e.g., google, youtube) and perform a search.
    """
    site = site.lower().strip()
    if 'youtube' in site:
        return search_youtube(query)
    elif 'google' in site:
        return search_google(query)
    elif 'bing' in site:
        search_url = "https://www.bing.com/search?q=" + quote(query)
        webbrowser.open(search_url)
        return f"🔍 Searching Bing for '{query}'! 🌐"
    elif 'duckduckgo' in site:
        search_url = "https://duckduckgo.com/?q=" + quote(query)
        webbrowser.open(search_url)
        return f"🔍 Searching DuckDuckGo for '{query}'! 🦆"
    else:
        # Fallback: try to open site + search if site is a domain
        if '.' in site and ' ' not in site:
            url = f"https://{site}/search?q={quote(query)}"
            webbrowser.open(url)
            return f"🔍 Searching {site} for '{query}'! 🌐"
        else:
            return f"🤔 Unknown site '{site}'. Try 'youtube', 'google', etc! 😊"

def open_youtube_in_chrome():
    """Open Chrome (or default browser) to YouTube."""
    if IS_WINDOWS:
        chrome_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, 'https://www.youtube.com'])
                return "🌐 Chrome is opening YouTube! Ready to watch some videos! 🎬"
    elif IS_MAC:
        try:
            subprocess.Popen(['open', '-a', 'Google Chrome', 'https://www.youtube.com'])
            return "🌐 Chrome is opening YouTube! Ready to watch some videos! 🎬"
        except FileNotFoundError:
            pass
    elif IS_LINUX:
        try:
            subprocess.Popen(['google-chrome', 'https://www.youtube.com'])
            return "🌐 Chrome is opening YouTube! Ready to watch some videos! 🎬"
        except FileNotFoundError:
            pass
    webbrowser.open('https://www.youtube.com')
    return "🌐 Opening YouTube in your browser! Time to watch some videos! 🎬"

def open_chrome_youtube_video(video_query=None):
    """Open Chrome to YouTube and start playing the user's exact video choice."""
    
    if video_query:
        # Direct search for exactly what the user requested
        # No conditions - just play what user asked for
        video_url = f"https://www.youtube.com/results?search_query={quote(video_query)}"
        message = f"🎬 Opening Chrome and searching for '{video_query}' on YouTube! �\n\n📝 Click on the video you want to watch! 😊"
    else:
        # Default popular video
        video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # A well-known video
        message = "🎬 Chrome is opening YouTube with a popular video! Get ready to watch! 🍿"
    
    if IS_WINDOWS:
        chrome_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, video_url])
                return message
    elif IS_MAC:
        try:
            subprocess.Popen(['open', '-a', 'Google Chrome', video_url])
            return message
        except FileNotFoundError:
            pass
    elif IS_LINUX:
        try:
            subprocess.Popen(['google-chrome', video_url])
            return message
        except FileNotFoundError:
            pass

    # Fallback: default browser
    webbrowser.open(video_url)
    return message

def play_specific_youtube_video(video_name):
    """Try to find and play a specific YouTube video directly."""
    # This is a more advanced function that could use YouTube API
    # For now, we'll search and let user choose
    return open_chrome_youtube_video(video_name)

def search_google(query):
    """Perform a Google search."""
    search_url = "https://www.google.com/search?q=" + quote(query)
    webbrowser.open(search_url)
    return f"🔍 Searching Google for '{query}'! 🌐"

# ----------------------------------------------------------------------
# Voice Listening Functions
# ----------------------------------------------------------------------
import speech_recognition as sr

recognizer = sr.Recognizer()

def listen_command():
    """Listen for voice command and return text"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Could not understand")
        return ""
    except sr.RequestError:
        print("Speech service error")
        return ""

def start_voice():
    """Start continuous voice listening"""
    while True:
        command = listen_command()
        if command == "":
            continue
        execute_command(command)

# ----------------------------------------------------------------------
# Strong Math Parser for Voice Commands
# ----------------------------------------------------------------------
def parse_math(command):
    """Parse math expressions from voice commands (STRONG VERSION)"""
    command = command.lower()

    replacements = {
        "plus": "+",
        "add": "+",
        "minus": "-",
        "subtract": "-",
        "multiply": "*",
        "multiplied by": "*",
        "times": "*",
        "divide": "/",
        "divided by": "/"
    }

    for word, symbol in replacements.items():
        command = command.replace(word, symbol)

    expression = re.findall(r"[0-9\+\-\*\/\.]+", command)

    if expression:
        return "".join(expression)

    return None

# ----------------------------------------------------------------------
# System Control Functions
# ----------------------------------------------------------------------
def lock_system():
    """Lock the computer screen."""
    if IS_WINDOWS:
        ctypes.windll.user32.LockWorkStation()
        return "🔒 System locked! 🔒"
    elif IS_MAC:
        subprocess.run(["pmset", "displaysleepnow"])
        return "🔒 System locked! 🔒"
    else:
        subprocess.run(["xdg-screensaver", "lock"])
        return "🔒 System locked! 🔒"

def mute_volume():
    """Mute/unmute the system volume."""
    pyautogui.press("volumemute")
    return "🔇 Volume toggled! 🔇"

def increase_volume():
    """Increase system volume."""
    for i in range(5):
        pyautogui.press("volumeup")
    return "🔊 Volume increased! 🔊"

def decrease_volume():
    """Decrease system volume."""
    for i in range(5):
        pyautogui.press("volumedown")
    return "🔉 Volume decreased! 🔉"

def take_screenshot():
    """Take a screenshot and save it."""
    try:
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Save to current directory
        filepath = os.path.join(os.getcwd(), filename)
        screenshot.save(filepath)
        
        return f"📸 Screenshot saved as {filename}! 📸\n\n📁 Location: {filepath}"
        
    except Exception as e:
        return f"❌ Failed to take screenshot: {str(e)}"

def check_battery():
    """Check battery status."""
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = battery.power_plugged
        
        if plugged:
            return f"🔋 Battery is {percent}% and charging! 🔋"
        else:
            if percent < 20:
                return f"⚠️ Battery is {percent}% - Low battery! ⚠️"
            else:
                return f"🔋 Battery is {percent}% 🔋"
    else:
        return "🔌 No battery detected (desktop system) 🔌"

def cpu_usage():
    """Check CPU usage."""
    cpu = psutil.cpu_percent(interval=1)
    if cpu < 50:
        return f"💻 CPU usage is {cpu}% - Normal 💻"
    elif cpu < 80:
        return f"⚠️ CPU usage is {cpu}% - Moderate ⚠️"
    else:
        return f"🔥 CPU usage is {cpu}% - High! 🔥"

def calculate_in_calculator(command):
    """Calculate math expression in Windows calculator (FORCE FRESH VERSION)"""
    try:
        print(f"🧮 Parsing math from: {command}")
        expression = parse_math(command)

        if not expression:
            print("❌ No math expression found")
            return "❌ No math expression found"

        print(f"📝 Math expression: {expression}")

        # close previous calculator (important) - ignore if not running
        try:
            print("🔄 Closing previous calculator...")
            subprocess.call("taskkill /IM Calculator.exe /F", shell=True)
        except:
            print("ℹ️ No calculator running, opening fresh")

        time.sleep(1)

        # open fresh calculator
        print("🚀 Opening fresh calculator...")
        subprocess.Popen("calc")

        time.sleep(2)

        # clear calculator
        print("🗑️ Clearing calculator...")
        pyautogui.press("esc")

        # type expression
        print(f"⌨️ Typing expression: {expression}")
        pyautogui.write(expression)

        # calculate
        print("🎯 Calculating...")
        pyautogui.press("enter")
        
        result = f"🧮 Calculator opened! {expression} calculated! 🧮"
        print(f"✅ Success: {result}")
        return result
            
    except Exception as e:
        print(f"❌ Calculator error: {e}")
        return f"❌ Error: {e}"

def calculate(command):
    """Calculate math expression in Windows calculator"""
    return calculate_in_calculator(command)

def open_calculator_with_math(math_expression):
    """Open calculator and perform math calculation automatically (legacy function)"""
    return calculate(f"calculate {math_expression}")

# ----------------------------------------------------------------------
# Intent detection and command execution
# ----------------------------------------------------------------------
def detect_intent(command):
    cmd = command.lower()
    
    if "youtube" in cmd or "video" in cmd:
        return "youtube"
    elif "write" in cmd and "letter" in cmd:
        return "letter"
    elif "create folder" in cmd:
        return "folder"
    elif "open" in cmd:
        return "app"
    elif "calculate" in cmd:
        return "calculate"
    elif "calculator" in cmd or "calc" in cmd:
        # Check if there's a math expression with calculator
        math_match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd)
        if math_match:
            return "calculator_math"
        else:
            return "calculator"
    elif "add" in cmd and re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd):
        return "calculator_math"
    elif "multiply" in cmd and re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd):
        return "calculator_math"
    elif "divide" in cmd and re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd):
        return "calculator_math"
    elif "subtract" in cmd and re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd):
        return "calculator_math"
    elif "list files" in cmd or "show files" in cmd:
        return "files"
    elif "search" in cmd:
        return "search"
    elif re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd):
        return "math"
    elif "lock system" in cmd or "lock computer" in cmd:
        return "lock"
    elif "mute volume" in cmd or "mute" in cmd:
        return "mute"
    elif "increase volume" in cmd or "volume up" in cmd or "turn up volume" in cmd:
        return "volume_up"
    elif "decrease volume" in cmd or "volume down" in cmd or "turn down volume" in cmd:
        return "volume_down"
    elif "screenshot" in cmd or "take screenshot" in cmd or "capture screen" in cmd:
        return "screenshot"
    elif "battery" in cmd or "check battery" in cmd:
        return "battery"
    elif "cpu usage" in cmd or "cpu" in cmd:
        return "cpu"
    elif cmd.startswith('run ') or cmd in ['ipconfig', 'ifconfig', 'dir', 'ls', 'pwd']:
        return "system"
    else:
        return "unknown"

# ----------------------------------------------------------------------
# Command parsing and execution
# ----------------------------------------------------------------------
def execute_command(command):
    """
    Main entry point. Interprets a natural language command and performs
    corresponding action. Returns a string response for the chat.
    """
    cmd = command.strip()
    lower = cmd.lower()
    
    print(f"🎯 Processing command: {cmd}")
    
    # Force calculator for every math command - more precise detection
    if ("calculate" in lower or 
        "plus" in lower or 
        "minus" in lower or 
        "multiply" in lower or 
        "times" in lower or 
        "divide" in lower or
        "divided by" in lower or
        "+" in cmd or 
        "-" in cmd or 
        "*" in cmd or 
        "/" in cmd or
        "multiplied by" in lower):
        
        print(f"🧮 Math command detected, using calculator")
        return calculate_in_calculator(command)
    
    # Detect intent
    intent = detect_intent(cmd)
    
    # Execute based on intent
    if intent == "youtube":
        return play_youtube_video(command)
    elif intent == "letter":
        # Handle letter writing
        if 'saying' in lower:
            match = re.search(r'write a letter\s+saying\s+(.+)', lower)
            if match:
                content = match.group(1).strip()
                return write_in_notepad(content)
        elif 'about' in lower:
            match = re.search(r'write a letter\s+about\s+(.+)', lower)
            if match:
                content = match.group(1).strip()
                return write_in_notepad(content)
        else:
            return write_in_notepad("")
    elif intent == "folder":
        match = re.search(r'create folder\s+[\'"]?([^\'"]+)[\'"]?', lower)
        if match:
            return create_folder(match.group(1))
    elif intent == "app":
        if lower.startswith('open '):
            app = cmd[5:].strip()
            return open_application(app)
    elif intent == "calculator":
        return open_application("calculator")
    elif intent == "calculate":
        return calculate(cmd)
    elif intent == "calculator_math":
        # Extract the math expression
        math_match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', cmd)
        if math_match:
            math_expr = math_match.group(1)
            return open_calculator_with_math(math_expr)
        else:
            return open_application("calculator")
    elif intent == "files":
        if 'desktop' in lower:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            return list_files(desktop)
        return list_files()
    elif intent == "search":
        if 'youtube' in lower:
            parts = lower.split('search youtube for')
            if len(parts) > 1:
                query = parts[1].strip()
                return search_youtube(query)
        elif 'google' in lower:
            parts = lower.split('search google for')
            if len(parts) > 1:
                query = parts[1].strip()
                return search_google(query)
        elif 'bing' in lower:
            parts = lower.split('search bing for')
            if len(parts) > 1:
                query = parts[1].strip()
                search_url = "https://www.bing.com/search?q=" + quote(query)
                webbrowser.open(search_url)
                return f"🔍 Searching Bing for '{query}'! 🌐"
    elif intent == "math":
        match = re.search(r'(\d+\s*[+\-*/]\s*\d+)', lower)
        if match:
            expr = match.group(1)
            if all(c in '0123456789+-*/() ' for c in expr):
                try:
                    result = eval(expr)
                    return f"🧮 Let me calculate that for you... {expr} = {result}! 🎯\n\nAnything else you'd like me to help with? 😊"
                except:
                    return "Oops! I had trouble with that calculation! 🤷‍♂️"
    elif intent == "lock":
        return lock_system()
    elif intent == "mute":
        return mute_volume()
    elif intent == "volume_up":
        return increase_volume()
    elif intent == "volume_down":
        return decrease_volume()
    elif intent == "screenshot":
        return take_screenshot()
    elif intent == "battery":
        return check_battery()
    elif intent == "cpu":
        return cpu_usage()
    elif intent == "system":
        if lower.startswith('run '):
            sys_cmd = cmd[4:].strip()
            return execute_system_command(sys_cmd)
        elif cmd in ['ipconfig', 'ifconfig', 'dir', 'ls', 'pwd']:
            return execute_system_command(cmd)

    # Fallback for unknown intent
    return (f"🤔 Hmm, I'm not sure how to help with '{cmd}'! But don't worry, I'm still learning! 😊\n\n"
            "Here are some things I CAN do for you:\n"
            "📝 Write a letter\n"
            "🧮 Open calculator\n"
            "🌐 Open Chrome\n"
            "📁 Create folders\n"
            "📂 List files\n"
            "🔢 Do math (like 2+2)\n"
            "💻 Run system commands\n"
            "🔒 Lock system\n"
            "🔇 Mute/unmute volume\n"
            "🔊 Increase/decrease volume\n"
            "📸 Take screenshots\n"
            "🔋 Check battery\n"
            "💻 Check CPU usage\n\n"
            "Just try one of these and I'll do my best to help! 🚀")
