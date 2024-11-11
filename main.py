# You'll need to install the cryptography library first. To do so, run: pip install cryptography # 

import json
import os
from cryptography.fernet import Fernet
from getpass import getpass

# Load encryption key from .env or create a new key
def load_key():
    # Generate a key if one doesn't exist and save it to .env
    if not os.path.exists(".env"):
        key = Fernet.generate_key()
        with open(".env", "wb") as key_file:
            key_file.write(key)
    # Load the key from .env
    with open(".env", "rb") as key_file:
        return key_file.read()

# Encrypt and decrypt functions
def encrypt_password(password, fernet):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password, fernet):
    return fernet.decrypt(encrypted_password.encode()).decode()

# Add password
def add_password(service, password, fernet):
    encrypted_password = encrypt_password(password, fernet)
    try:
        with open("passwords.json", "r+") as file:
            data = json.load(file)
            data[service] = encrypted_password
            file.seek(0)
            json.dump(data, file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open("passwords.json", "w") as file:
            json.dump({service: encrypted_password}, file)
    print(f"Password for {service} saved successfully!")

# Retrieve password
def retrieve_password(service, fernet):
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
            encrypted_password = data.get(service)
            if encrypted_password:
                return decrypt_password(encrypted_password, fernet)
            else:
                print(f"No password found for {service}.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No passwords stored yet.")
    return None

# List all services
def list_services():
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
            print("Stored services:")
            for service in data.keys():
                print(f"- {service}")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No passwords stored yet.")

# Delete password
def delete_password(service):
    try:
        with open("passwords.json", "r+") as file:
            data = json.load(file)
            if service in data:
                del data[service]
                file.seek(0)
                file.truncate()
                json.dump(data, file)
                print(f"Password for {service} deleted successfully.")
            else:
                print(f"No password found for {service}.")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No passwords stored yet.")

# Main function
def main():
    key = load_key()
    fernet = Fernet(key)

    # Prompt user for master password
    master_password = getpass("Enter the master password: ")

    # Basic menu
    while True:
        print("\nPassword Manager")
        print("1. Add a password")
        print("2. Retrieve a password")
        print("3. List all services")
        print("4. Delete a password")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            service = input("Enter the service name: ")
            password = getpass("Enter the password for the service: ")
            add_password(service, password, fernet)
        elif choice == '2':
            service = input("Enter the service name to retrieve the password: ")
            password = retrieve_password(service, fernet)
            if password:
                print(f"Password for {service}: {password}")
        elif choice == '3':
            list_services()
        elif choice == '4':
            service = input("Enter the service name to delete the password: ")
            delete_password(service)
        elif choice == '5':
            print("Exiting Password Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
