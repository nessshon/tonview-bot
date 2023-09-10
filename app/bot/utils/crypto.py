from cryptography.fernet import Fernet


def encrypt_key(key: str, api_key: str):
    cipher_suite = Fernet(key.encode())
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    return encrypted_key


def decrypt_key(key: str, encrypted_key: bytes):
    cipher_suite = Fernet(key.encode())
    decrypted_key = cipher_suite.decrypt(encrypted_key)
    return decrypted_key.decode()
