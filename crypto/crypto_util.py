import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

class RSAUtil:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        key = RSA.generate(self.key_size)
        self.private_key = key
        self.public_key = key.publickey()

    def export_keys(self):
        private_pem = self.private_key.export_key()
        public_pem = self.public_key.export_key()
        return private_pem, public_pem

    def load_private_key(self, private_pem):
        self.private_key = RSA.import_key(private_pem)
        self.public_key = self.private_key.publickey()

    def load_public_key(self, public_pem):
        if isinstance(public_pem, RsaKey):
            self.public_key = public_pem
        else:
            self.public_key = RSA.import_key(public_pem)

    def encrypt(self, message):
        cipher = PKCS1_OAEP.new(self.public_key)
        encrypted_message = cipher.encrypt(message.encode())
        return base64.b64encode(encrypted_message).decode()

    def decrypt(self, encrypted_message):
        cipher = PKCS1_OAEP.new(self.private_key)
        decrypted_message = cipher.decrypt(base64.b64decode(encrypted_message))
        return decrypted_message.decode()

    def sign(self, message):
        """Signs a message using the private key."""
        if not self.private_key:
            raise ValueError("Private key not loaded.")
        hash_obj = SHA256.new(message.encode())
        signature = pkcs1_15.new(self.private_key).sign(hash_obj)
        return base64.b64encode(signature).decode()

    def verify_sign(self, message, signature, hash_obj=None):
        """Verifies the message signature using the public key."""
        if not self.public_key:
            raise ValueError("Public key not loaded.")
        if hash_obj is None:
            if isinstance(message, str):
                message = message.encode()
            hash_obj = SHA256.new(message)
        try:
            pkcs1_15.new(self.public_key).verify(hash_obj, base64.b64decode(signature))
            return True
        except (ValueError, TypeError) as e:
            print(e)
            return False



if __name__ == '__main__':
# Example usage
    rsa_util = RSAUtil()
    rsa_util.generate_keys()
    private_key, public_key = rsa_util.export_keys()

    # Signing and verifying a message
    message = "Hello, RSA signing!"
    signature = rsa_util.sign(message)
    verification = rsa_util.verify_sign(message, signature)

    print(f"Signature: {signature}")
    print(f"Verification result: {verification}")





