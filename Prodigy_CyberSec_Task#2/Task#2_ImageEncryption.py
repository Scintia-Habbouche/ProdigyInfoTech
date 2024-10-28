# Purpose:
# This program implements a simple image encryption tool using pixel manipulation.
# It allows the user to:
# 1. Encrypt an uploaded image using a specified key.
# 2. Decrypt an uploaded encrypted image using a specified key.
# The program uses a basic mathematical transformation to encrypt and decrypt the images.
# A simple graphical user interface (GUI) is built using Gradio to facilitate user interactions.

import gradio as gr
from PIL import Image
import numpy as np

# Encrypts the image using a key
def encrypt_image(image, key):
    image_array = np.array(image)  # Convert image to a NumPy array
    encrypted_image_array = (image_array * key) // (key + 1)
    encrypted_image_array = np.clip(encrypted_image_array, 0, 255)

    encrypted_image = Image.fromarray(np.uint8(encrypted_image_array))  # Convert back to image
    return encrypted_image

# Decrypts the image using a key
def decrypt_image(image, key):
    encrypted_image_array = np.array(image)
    decrypted_image_array = (encrypted_image_array * (key + 1)) // key
    decrypted_image_array = np.clip(decrypted_image_array, 0, 255)

    decrypted_image = Image.fromarray(np.uint8(decrypted_image_array))
    return decrypted_image

# Gradio interface function to handle image encryption
def gradio_encrypt(image, key):
    return encrypt_image(image, key)

# Gradio interface function to handle image decryption
def gradio_decrypt(image, key):
    return decrypt_image(image, key)

# Create the Gradio interface
with gr.Blocks(title="Image Encryption") as demo:
    gr.Markdown("## Image Encryption")

    with gr.Tab("Encrypt"):
        with gr.Row():
            image_input = gr.Image(label="Upload Image for Encryption")
            key_input = gr.Number(label="Encryption Key", value=1, precision=0)
        encrypted_image_output = gr.Image(label="Encrypted Image")
        encrypt_btn = gr.Button("Encrypt Image")
        encrypt_btn.click(gradio_encrypt, inputs=[image_input, key_input], outputs=encrypted_image_output)

    with gr.Tab("Decrypt"):
        with gr.Row():
            image_input_decrypt = gr.Image(label="Upload Encrypted Image")
            key_input_decrypt = gr.Number(label="Decryption Key", value=1, precision=0)
        decrypted_image_output = gr.Image(label="Decrypted Image")
        decrypt_btn = gr.Button("Decrypt Image")
        decrypt_btn.click(gradio_decrypt, inputs=[image_input_decrypt, key_input_decrypt], outputs=decrypted_image_output)

# Launch the app
if __name__ == "__main__":
    demo.launch()
