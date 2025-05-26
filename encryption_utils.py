# Version 1.8 (Modular - COPILOT - CHECKPOINT) 07.05 12:30 (Compatible with 1.8.1, 1.9)

from cryptography.fernet import Fernet
import os
import json

# Path to the encryption key file
KEY_FILE = "encryption.key"

# Path to the encrypted configuration file
CONFIG_FILE = "config.enc"

def generate_key():
    
    # Generates a new encryption key and saves it to a file.
    
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as key_file:
        key_file.write(key)

def load_key():
    
    # Loads the encryption key from the file. If the key file is missing, generates a new key.

    # Returns:
        # bytes: The encryption key.
    
    if not os.path.exists(KEY_FILE):
        print("⚠️ Encryption key file not found. Generating a new key...")
        generate_key()
    with open(KEY_FILE, 'rb') as key_file:
        return key_file.read()

def encrypt_config(config_data):
    
    # Encrypts the configuration data and saves it to a file.

    # Args:
        # config_data (dict): The configuration data to encrypt.
    
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(json.dumps(config_data).encode())
    with open(CONFIG_FILE, 'wb') as config_file:
        config_file.write(encrypted_data)

def decrypt_config():
    
    # Decrypts the configuration data from the encrypted file.

    # Returns:
        # dict: The decrypted configuration data.
    
    key = load_key()
    fernet = Fernet(key)
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Encrypted configuration file not found: {CONFIG_FILE}")
    with open(CONFIG_FILE, 'rb') as config_file:
        encrypted_data = config_file.read()
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)