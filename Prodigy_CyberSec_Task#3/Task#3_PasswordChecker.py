import re
import gradio as gr

# A small sample list of common passwords 
common_passwords = [
    "123456", "password", "123456789", "12345678", "12345", "1234567", "qwerty", 
    "abc123", "football", "monkey", "letmein", "welcome", "P@$$w0rd", "toor", "P@ssw0rd"
]

def assess_password_strength(password):
    # Checking criteria
    has_numbers = any(char.isdigit() for char in password)
    has_upper_case = any(char.isupper() for char in password)
    has_lower_case = any(char.islower() for char in password)
    meets_length_requirement = len(password) >= 8
    has_special_characters = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    # Count the number of criteria met
    criteria_met = sum([has_numbers, has_upper_case, has_lower_case, meets_length_requirement, has_special_characters])

    # Providing detailed feedback based on missing criteria
    feedback = []
    if not meets_length_requirement:
        feedback.append("Password must be at least 8 characters long.")
    if not has_upper_case:
        feedback.append("Password must include at least one uppercase letter.")
    if not has_lower_case:
        feedback.append("Password must include at least one lowercase letter.")
    if not has_numbers:
        feedback.append("Password must include at least one number.")
    if not has_special_characters:
        feedback.append("Password must include at least one special character.")

    # Check if the password is in the list of common passwords
    if password in common_passwords:
        # Add specific emphasis to the password strength if it's commonly used
        strength = "Very Weak (Commonly used password - highly vulnerable to dictionary attacks)."
        feedback.append("This password is found in a list of commonly used passwords and is highly vulnerable to dictionary attacks. Choose a stronger, more unique password.")
    else:
        # Determine password strength based on criteria met
        if criteria_met == 5:
            strength = "Very Strong (All criteria are met)."
        elif criteria_met == 4:
            strength = "Strong (4 out of 5 criteria are met)."
        elif criteria_met == 3:
            strength = "Moderate (3 out of 5 criteria are met)."
        else:
            strength = "Weak (Less than 3 criteria are met)."

    return strength, feedback

def password_complexity_checker(password, show_password):
    # Assess the password strength
    strength, feedback = assess_password_strength(password)
    
    # Mask the password if needed
    if not show_password:
        if len(password) > 2:
            masked_password = password[0] + '#' * (len(password) - 2) + password[-1]
        else:
            masked_password = password
    else:
        masked_password = password

    feedback_output = "\n".join(feedback) if feedback else "All criteria met!"
    
    # Return masked password, strength, and feedback
    return f"Entered Password: {masked_password}\nStrength: {strength}\nFeedback: {feedback_output}"

# Gradio interface with updated components
interface = gr.Interface(
    fn=password_complexity_checker, 
    inputs=[gr.Textbox(label="Enter Password", type="password"), gr.Checkbox(label="Show Password")],
    outputs=gr.Textbox(), 
    title="Password Complexity Checker",
    description="Enter a password and check its strength based on various criteria such as length, uppercase, lowercase, numbers, special characters, and whether it's a common password."
)

if __name__ == "__main__":
    interface.launch()