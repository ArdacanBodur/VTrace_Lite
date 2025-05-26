# Version 1.8 (Modular - COPILOT - CHECKPOINT) 07.05 12:30 (Compatible with 1.8.1, 1.9)

import os
import bcrypt
from getpass import getpass

# Path to the file storing the hashed password
PASSWORD_FILE = "password.hash"

def set_password():
    
    # Sets a new password for the user and saves its hash.
    
    password = getpass("Enter a new password: ")
    confirm_password = getpass("Confirm the new password: ")
    if password != confirm_password:
        print("❌ Passwords do not match!")
        return
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(PASSWORD_FILE, 'wb') as password_file:
        password_file.write(hashed_password)
    print("✅ Password has been set successfully.")

def authenticate_user():
    
    # Authenticates the user by verifying the entered password.

    # Returns:
        # bool: True if authentication is successful, False otherwise.
    
    if not os.path.exists(PASSWORD_FILE):
        print("⚠️ No password has been set. Please set a password first.")
        set_password()
        return False
    with open(PASSWORD_FILE, 'rb') as password_file:
        hashed_password = password_file.read()
    password = getpass("Enter your password: ")
    if bcrypt.checkpw(password.encode(), hashed_password):
        print("✅ Authentication successful.")
        return True
    else:
        print("❌ Authentication failed. Invalid password.")
        return False