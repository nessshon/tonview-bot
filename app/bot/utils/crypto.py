from cryptography.fernet import Fernet


def encrypt_key(key: str, api_key: str):
    """
    Encrypts the given API key using the provided encryption key.

    Parameters:
        key (str): The encryption key used to encrypt the API key.
        api_key (str): The API key to be encrypted.

    Returns:
        str: The encrypted API key.
    """
    cipher_suite = Fernet(key.encode())
    encrypted_key = cipher_suite.encrypt(api_key.encode())
    return encrypted_key


def decrypt_key(key: str, encrypted_key: bytes):
    """
    Decrypts the given encrypted key using the provided key.

    Parameters:
        key (str): The key used to decrypt the encrypted key.
        encrypted_key (bytes): The encrypted key to be decrypted.

    Returns:
        str: The decrypted key as a string.
    """
    cipher_suite = Fernet(key.encode())
    decrypted_key = cipher_suite.decrypt(encrypted_key)
    return decrypted_key.decode()
