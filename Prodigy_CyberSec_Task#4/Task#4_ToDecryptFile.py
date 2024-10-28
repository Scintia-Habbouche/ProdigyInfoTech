from cryptography.fernet import Fernet

# Ask for the name of the log file to decrypt
log_file_path = input("Enter the name of the log file to decrypt: ")

# Ask for the decryption key as text
key_input = input("Enter the decryption key: ").encode()

# Create a Fernet object with the provided key
cipher_suite = Fernet(key_input)

# Read and decrypt the log file
try:
    with open(log_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Display the decrypted content
    print("Decrypted file content:")
    print(decrypted_data.decode("utf-8"))

except Exception as e:
    print("Error during decryption:", e)
