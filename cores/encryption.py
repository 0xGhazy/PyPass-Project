import os
from cryptography.fernet import Fernet


class EncryptionHandler:
    """
    Class for handling all encryption process in the application.

    Attributes
    ----------
        key_value
        encrypted_payload
        decrypted_payload
        security_key


    Methods
    -------
        generate_key() -> None
        load_encryption_key() -> Bytes
        encrypt(plain_text) -> str
        decrypt(encrypted_text) -> str
    """

    def __init__(self) -> None:
        # change working directory to __file__ dirname
        os.chdir(os.path.dirname(__file__))
        self.key_value = None
        self.encrypted_payload = None
        self.decrypted_payload = None
        self.security_key = "security_key.key"
        if self.security_key in os.listdir():
            pass
        else:
            self.generate_key()

    def generate_key(self: str) -> None:
        """Function to generate encryption key at first time of running the application."""
        self.key_value = Fernet.generate_key()
        with open(self.security_key, "wb") as key_obj:
            key_obj.write(self.key_value)

    def load_encryption_key(self) -> bin:
        """Function to read encryption key (security_key.key) from the same directory"""
        try:
            with open(self.security_key, "rb") as key_obj:
                return key_obj.read()
        except Exception as error_message:
            raise Exception(f"[-] {str(error_message)}")

    def encrypt(self, message: bytes) -> bytes:
        """Function to encrypt message/data using encryption key"""
        # reading the encryption key
        key = self.load_encryption_key()
        encoded_message = message
        f = Fernet(key)
        # return the encrypted message
        encrypted_message = f.encrypt(encoded_message)
        self.encrypted_payload = encrypted_message
        return self.encrypted_payload

    def decrypt(self, encrypted_message: bytes) -> bytes:
        """Decrypts an encrypted message"""
        key = self.load_encryption_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)
        self.decrypted_payload = decrypted_message
        return self.decrypted_payload


if __name__ == "__main__":
    sec_obj = EncryptionHandler()

