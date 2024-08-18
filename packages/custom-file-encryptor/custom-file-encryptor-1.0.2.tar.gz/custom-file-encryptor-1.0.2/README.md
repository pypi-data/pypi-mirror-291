# Custom File Encryptor

A custom Python library for file encryption and decryption using a simple, self-made encryption algorithm. This library supports encryption of any file type and is easy to integrate into other projects.

## Features

- Encrypt and decrypt any file type (e.g., `.txt`, `.jpg`, `.pdf`, `.mp4`).
- Custom encryption algorithm with simple operations (XOR and byte shifts).
- Easy-to-use API for integrating into other Python projects.

## Installation

To install the library, simply use pip:

```bash
pip install custom-file-encryptor
```

## Usage
Here is a basic example of how to use the CustomFileEncryptor class to encrypt and decrypt files:

```bash
from custom_file_encryptor.encryptor import CustomFileEncryptor

# Initialize the encryptor with a password
encryptor = CustomFileEncryptor(password="my_secure_password")

# Encrypt a file
encryptor.encrypt_file("example.jpg", "example_encrypted.enc")

# Decrypt the file back to its original form
encryptor.decrypt_file("example_encrypted.enc", "example_decrypted.jpg")

```



## Contact
For any questions or inquiries, please contact the author:
- Name: Liu Yu chen
- Email: liuyuchen032901@outlook.com