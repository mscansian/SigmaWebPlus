from base64 import b64encode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class Crypto():
    key = None
    chipher = None
    
    def __init__(self, keyPath):
        self.key = RSA.importKey(open(keyPath).read())
        self.cipher = PKCS1_OAEP.new(self.key)
    
    def encrypt(self, data):
        return b64encode(self.cipher.encrypt(data))
    
    def decrypt(self, data):
        return b64encode(self.cipher.decrypt(data))