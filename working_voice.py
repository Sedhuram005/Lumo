import speech_recognition as sr
import pyttsx3
import time
import threading
from backend import execute_command

# Initialize speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# Improved recognition settings
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8
recognizer.dynamic_energy_threshold = True
recognizer.dynamic_adjustment_ratio = 0.5

def speak(text):
    """Convert text to speech"""
    print(f"Lumo: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_optimized():
    """Optimized listening for better wake word detection"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎙️ Listening...")
        
        # Use shorter phrase time limit for responsiveness, no timeout
        audio = recognizer.listen(source, phrase_time_limit=3)

    try:
        text = recognizer.recognize_google(audio)
        text = text.lower()
        print(f"Heard: {text}")
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"Speech service error: {e}")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

def voice_loop():
    """Optimized voice loop with fast wake word detection"""
    speak("Lumo voice system started")
    speak("Say 'lumo' to activate me")
    
    consecutive_detections = 0
    
    while True:
        text = listen_optimized()
        
        # Check for wake word
        if "lumo" in text:
            consecutive_detections += 1
            print(f"🎯 Wake word detected! (streak: {consecutive_detections})")
            
            # Show wake animation
            try:
                from lumo_animation import show_wake_animation
                animation_thread = threading.Thread(target=show_wake_animation, daemon=True)
                animation_thread.start()
            except ImportError:
                print("Animation module not available")
            
            # Only respond if this is a clear detection (not background noise)
            if consecutive_detections >= 1:
                speak("How can I help you")
                
                # Listen for command
                print("Listening for command...")
                command = listen_optimized()
                
                if command and len(command.strip()) > 2:  # Require meaningful command
                    print(f"Executing: {command}")
                    try:
                        result = execute_command(command)
                        if result:
                            speak(result)
                    except Exception as e:
                        speak(f"Sorry, I had trouble with that command")
                else:
                    speak("I didn't catch that. Please try again.")
                
                consecutive_detections = 0  # Reset counter
                time.sleep(1)  # Brief pause
            else:
                consecutive_detections = 0  # Reset if it was noise
        
        elif text == "":
            continue
        else:
            consecutive_detections = 0  # Reset on non-wake words
            continue

if __name__ == "__main__":
    voice_loop()
