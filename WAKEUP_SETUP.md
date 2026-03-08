# Lumo Wake-Up Service Setup

## 🎤 Always-On Voice Assistant

Make Lumo listen for "lumo" wake word anywhere on your computer!

## 🚀 Quick Start

### 1. Start Wake-Up Service
```bash
python lumo_wakeup.py
```

### 2. Test Wake Word
Say **"lumo"** anywhere:
- On desktop
- In Chrome
- In VS Code
- While gaming

Lumo will open automatically!

## ⚡ Windows Auto-Start Setup

### Method 1: Startup Folder (Easy)

1. **Press Win + R**
2. **Type:** `shell:startup`
3. **Press Enter**
4. **Create shortcut** to `lumo_wakeup.py`
5. **Restart computer**

Now Lumo starts automatically with Windows!

### Method 2: Task Scheduler (Advanced)

1. **Open Task Scheduler**
2. **Create Basic Task**
3. **Name:** "Lumo Wake-Up"
4. **Trigger:** "When computer starts"
5. **Action:** Start program `python lumo_wakeup.py`
6. **Finish**

## 🎯 Wake Word Variations

Lumo detects multiple variations:
- ✅ **"lumo"**
- ✅ **"lima"** 
- ✅ **"limo"**
- ✅ **"luma"**

## 🔄 How It Works

```
Background Listener (always running)
        ↓
Detect "lumo" anywhere
        ↓
Open Lumo Application
        ↓
Ready for voice commands
```

## 📱 Usage Examples

### Wake Up Assistant
```
You say: "lumo"
System: Opens Lumo UI
```

### Then Use Voice Commands
```
"lumo open chrome"
"lumo play youtube video"
"lumo take screenshot"
"lumo lock system"
"lumo check battery"
```

## 🛠️ Troubleshooting

### Wake Word Not Detected
- Speak clearly and at normal volume
- Reduce background noise
- Try different variations: "limo", "luma"

### Lumo Won't Open
- Check that `.venv\lumo.py` exists
- Ensure Python is installed
- Try running `py .venv\lumo.py` manually

### Multiple Lumo Windows
- Service checks if Lumo is already running
- Prevents opening multiple instances

## 🔧 Advanced Options

### Custom Wake Word
Edit `lumo_wakeup.py`:
```python
if "lumo" in text or "lima" in text or "limo" in text or "luma" in text:
    # Add your custom wake word here
```

### Custom UI Path
Edit the `ui_paths` list in `lumo_wakeup.py`:
```python
ui_paths = [
    "path/to/your/lumo.py",
    "another/path.py"
]
```

## 🎉 Features

- ✅ **Always listening** for wake word
- ✅ **Works anywhere** on your system
- ✅ **Smart detection** - avoids duplicates
- ✅ **Auto-start** with Windows
- ✅ **Low resource** usage
- ✅ **Error handling** and recovery

## 🚀 Complete Voice Control

Now you have:
1. **Background wake word detection**
2. **Automatic UI opening**
3. **Full voice command control**
4. **System automation**
5. **Windows integration**

Your personal AI assistant is ready! 🤖🎤✨
