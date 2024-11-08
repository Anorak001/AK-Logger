from cryptography.fernet import Fernet

# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

cipher = Fernet(load_key())
LOG_FILE = "keystrokes.log"

# Decrypt and display keystrokes
with open(LOG_FILE, "rb") as file:
    for line in file:
        decrypted_data = cipher.decrypt(line.strip())
        print(decrypted_data.decode())
