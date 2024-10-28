# Purpose:
# This program implements the Caesar cipher
# It allows the user to:
# 1. Encrypt a message (manual input or file) using a specified shift value.
# 2. Decrypt a message using a specified shift value.
# 3. Perform a brute force attack to decrypt a message without knowing the shift value.

def menu():
    print("\n---   M  E  N  U   ---")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Brute force attack")
    print("4. Quit")
    
    while True: # Loop to ensure the user enters a valid option
        try:
            choice = int(input("Choose an option (1-4) : "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Please Choose a valid option (1-4).")
        except ValueError:
            print("Invalid Input. Please enter a number.")

# Function to encrypt a message using Caesar cipher with a shift value, optionally including digits
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
            # Keep non-alphabetic and non-digit characters unchanged
            encrypted_message += char
    return encrypted_message

# Function to decrypt a message by applying the reverse Caesar cipher (negative shift)
def decrypt(message, shift):
    return encrypt(message, -shift)

# Function to brute-force decrypt a message by trying all possible shift values
def brute_force_decrypt(message):
    print("\n--- Brute Force Attack Results ---\n")
    for shift in range(1, 26):  # Test all possible shifts (from 1 to 25)
        decrypted_message = decrypt(message, shift)
        print(f"Shift {shift}: {decrypted_message}")

# Function to get a valid shift value from the user (must be an integer)
def get_valid_shift():
    while True:
        try:
            shift = int(input("Enter the shift value:  : "))
            return shift % 26
        except ValueError:
            print("Please enter a valid integer.")

# Function to read message content from a file
def read_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("The specified file was not found.")
        return None

# Function to write content to a file
def write_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

# Function to get the message, either by manual input or from a file
def get_message():
    choice_input = input("Would you like to enter the text manually or via a file? (T)exte/(F)ile : ").upper()
    
    if choice_input == 'T':
        return input("Enter the message: ")
    elif choice_input == 'F':
        file_path = input("Enter the path of the text file:")
        message = read_from_file(file_path)
        if message is None:
            return None
        return message
    else:
        print("Invalid choice.")
        return None
    

# Main function to run the Caesar cipher program
def caesar_cipher():
    while True:
        choice = menu()
        
        if choice == 4:  # Quit
            print("Goodbye!")
            break
        
        message = get_message()
        if message is None:
            continue
        
        if choice == 1:  # Encrypt
            shift = get_valid_shift()
            include_digits = input("Would you also like to encrypt digits?  (Y/N) : ").upper() == 'Y'
            result_message = encrypt(message, shift, include_digits)
            print(f"Encrypted message: {result_message}")
        elif choice == 2:  # decrypt
            shift = get_valid_shift()
            result_message = decrypt(message, shift)
            print(f"Decrypted message: {result_message}")
        elif choice == 3:  # Brute Force 
            brute_force_decrypt(message)
            continue  # No need to save the brute force results
        
        # Ask if the user wants to save the result to a file
        save_choice = input("Would you like to save the result to a file? (Y/N) : ").upper()
        if save_choice == 'Y':
            output_file_path = input("Enter the path of the output file: ")
            write_to_file(output_file_path, result_message)
            print(f"The result has been saved to {output_file_path}")

# Run the Caesar cipher program
caesar_cipher()

