import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class Crypto:

    _key = None
    

    def __init__(self, password = None):
        if Crypto._key == None and password:
            Crypto._key = generateKeyFromPassword(password)


    def is_initialized(self):
        return not Crypto._key == None


    def uninitialize(self):
        Crypto._key = None


    def encrypt(self, text: str) -> str:
        crypted_text = Fernet(Crypto._key).encrypt(text.encode())
        return base64.urlsafe_b64encode(crypted_text).decode()


    def decrypt(self, text: str):
        return Fernet(self._key).decrypt(base64.urlsafe_b64decode(text)).decode()


def generateKeyFromPassword(password: str):
    # Always the same salt that only the password is used as input for encryption key
    salt = b'y\x01\x9e\x02\x13\xa93\x13;u6\xcc\xef\xad\xc1\x92'
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def generateVerificationStringFromPassword(password: str):
    key = generateKeyFromPassword(password)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key)
    return base64.urlsafe_b64encode(digest.finalize()).decode()