# Purpose:
# This program implements the Caesar cipher
# It allows the user to:
# 1. Encrypt a message (manual input or file) using a specified shift value.
# 2. Decrypt a message using a specified shift value.
# 3. Perform a brute force attack to decrypt a message without knowing the shift value.

import gradio as gr

# Functions from the original Caesar cipher program
def encrypt(message, shift, include_digits=False):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            #ascii_offset = 65 if char.isupper() else 97  # Use 65 for uppercase letters (A-Z), 97 for lowercase letters (a-z)
            #encrypted_message += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            start = ord('a') if char.islower() else ord('A')    #This version is functionally the same but uses more readable logic.
            encrypted_message += chr((ord(char) - start + shift) % 26 + start)
        elif include_digits and char.isdigit():
            encrypted_message += str((int(char) + shift) % 10)
        else:
            encrypted_message += char
    return encrypted_message

# Function to decrypt a message by applying the reverse Caesar cipher (negative shift)
def decrypt(message, shift):
    return encrypt(message, -shift)

# Function to brute-force decrypt a message by trying all possible shift values
def brute_force_decrypt(message):
    results = []
    for shift in range(1, 26): # Test all possible shifts (from 1 to 25)
        decrypted_message = decrypt(message, shift)
        results.append(f"Shift {shift}: {decrypted_message}")
    return "\n".join(results)

# Gradio interface functions
def caesar_interface(message, file, shift, mode, include_digits):
    # Read message from the file if a file is provided
    if file is not None:
        message = file.read().decode("utf-8")
    
    if mode == "Encrypt":
        result = encrypt(message, shift, include_digits)
    elif mode == "Decrypt":
        result = decrypt(message, shift)
    elif mode == "Brute Force":
        result = brute_force_decrypt(message)

    # Save the result to an output file
    with open("/mnt/data/output.txt", "w") as output_file:
        output_file.write(result)

    return result, "/mnt/data/output.txt"

# Set up the Gradio interface
iface = gr.Interface(
    fn=caesar_interface,
    inputs=[
        gr.Textbox(label="Message (Leave empty if uploading a file)"),  # Message input
        gr.File(label="Upload a text file"),  # File input
        gr.Slider(0, 25, step=1, label="Shift"),  # Shift value input (insure getting a valid shift value)
        gr.Radio(["Encrypt", "Decrypt", "Brute Force"], label="Mode"),  # Mode input
        gr.Checkbox(label="Include digits")  # Include digits for encryption option
    ],
    outputs=[
        "text",  # Display result text
        gr.File(label="Download output file")  # File output for downloading
    ],
    title="Caesar Cipher Tool",
    description="Encrypt, Decrypt, or Brute Force a message or file using the Caesar cipher."
)

# Launch the interface
iface.launch()
