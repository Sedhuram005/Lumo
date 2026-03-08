# Lumo Voice Assistant Setup

## 🎤 Voice Commands Overview

Lumo now supports **hands-free voice control** with wake word activation!

## 🚀 Quick Start

### 1. Run Voice Listener
```bash
python start_lumo_voice.py
```

### 2. Say Wake Word
```
"Hey Lumo"
```

### 3. Lumo Responds
```
"How can I help you?"
```

### 4. Give Command
```
"Open Chrome"
"Play Python tutorial on YouTube"
"Create folder test"
"Write a letter"
```

## 📋 Available Voice Commands

### 🌐 Browser & Web
- "Open Chrome" → Opens Chrome browser
- "Play [video] on YouTube" → Searches and plays YouTube videos
- "Search Google for [query]" → Google search
- "Open [website]" → Opens specific website

### 📁 File & System
- "Create folder [name]" → Creates new folder
- "List files" → Shows directory contents
- "Open calculator" → Opens calculator app
- "Open notepad" → Opens Notepad

### ✍️ Writing
- "Write a letter" → Writes complete friendly letter
- "Write a letter saying [text]" → Custom letter content

### 🧮 Math
- "What is 2+2" → Performs calculations
- "Calculate 5*3" → Math operations

### 🎬 Entertainment
- "Play [song/movie/tutorial]" → YouTube content
- "Play music" → Music videos
- "Play movie trailers" → Latest trailers

## 🛠️ Installation

### Required Libraries
```bash
pip install SpeechRecognition pyttsx3 pyaudio psutil pygetwindow
```

### Windows PyAudio Installation
```bash
pip install pipwin
pipwin install pyaudio
```

## 🎯 Wake Word System

### How It Works
1. **Background Listener** runs continuously
2. **Detects "Hey Lumo"** wake word
3. **Opens Lumo UI** automatically
4. **Listens for command**
5. **Executes command** and speaks response

### Wake Words Supported
- "Hey Lumo"
- "Hi Lumo" 
- "Hello Lumo"

### Stop Commands
- "Stop listening"
- "Goodbye"
- "Exit"
- "Shutdown"

## 🔄 Usage Scenarios

### Scenario 1: Working in Browser
1. You're browsing the web
2. Say "Hey Lumo"
3. Lumo opens and asks "How can I help you?"
4. Say "Play Python tutorial on YouTube"
5. Video starts playing

### Scenario 2: Working in VS Code
1. You're coding
2. Say "Hey Lumo"
3. Lumo opens and asks "How can I help you?"
4. Say "Create folder project"
5. Folder is created

### Scenario 3: Need Calculator
1. You're working anywhere
2. Say "Hey Lumo"
3. Lumo opens and asks "How can I help you?"
4. Say "Open calculator"
5. Calculator opens

## 🎮 UI Integration

The Lumo UI also has a **microphone button** (🎤) for manual voice commands:

1. Click the 🎤 button
2. Button turns red (🔴) when listening
3. Speak your command
4. Lumo executes and responds

## 🔧 Troubleshooting

### Microphone Not Working
- Check microphone permissions
- Ensure microphone is not muted
- Try "pip install pyaudio" if missing

### Voice Not Recognized
- Speak clearly and at normal volume
- Reduce background noise
- Try different wake word variations

### UI Not Opening
- Check that `.venv/lumo.py` exists
- Ensure Python is in system PATH
- Try running `py .venv/lumo.py` manually

## 🚀 Advanced Usage

### Add to Windows Startup
1. Create shortcut to `start_lumo_voice.py`
2. Place in Windows Startup folder
3. Lumo will auto-start with PC

### Custom Wake Words
Edit `wake_listener.py` to add more wake words:
```python
if "hey lumo" in text or "hi lumo" in text or "your custom phrase" in text:
```

## 📱 Voice Features

- ✅ **Wake Word Detection** - Continuous listening
- ✅ **Natural Language** - Understands conversational commands
- ✅ **Voice Feedback** - Speaks responses
- ✅ **Error Handling** - Graceful failure recovery
- ✅ **Background Operation** - Works while you use other apps

## 🎉 Enjoy Your Voice Assistant!

You now have a **Jarvis-style voice assistant** that's always ready to help! 🤖🎤
