# Password-Manager-Cli
A simple command-line password manager built in Python that securley stores, retrives, and manages passwords using encryption. This tool allows users to manager their credentials for different services through a secure and easy-to-use interface.

# Features
* Store Passwords: Save passwords securely with encryption.
* Retrieve Passwords: Access stored passwords by service name.
* Delete Passwords: Remove stored password by service.
* List Services: Display a list of saved services without showing passwords

# Security 
* Encryption: All passwords are encrypted using symmetric encryption (Fernet) from the cryptography library, ensuring they are safely stored.
* Master Password: Users must enter a master password to access the stored passwords.
