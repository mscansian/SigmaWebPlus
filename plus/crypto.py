#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
    crypto.py
    
    Este arquivo descreve a classe RSACrypto que serve para criptografar e descriptografar
    strings utilizando uma chave RSA (PKCS1-OAEP). As strings criptografadas sempre são 
    recebidas/retornadas codificadas em base64 (permite transmitir ela via internet).
    
    Metodos publicos
        base64str  encrypt (str data)
        str        decrypt (base64str data)
        
    Dependencias (dentro do projeto)
        
'''

from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class RSACrypto():
    key = None
    chipher = None
    
    def __init__(self, keyPath):
        self.key = RSA.importKey(open(keyPath).read())
        self.cipher = PKCS1_OAEP.new(self.key)
    
    def encrypt(self, data):
        return b64encode(self.cipher.encrypt(data))
    
    def decrypt(self, data):
        return b64encode(self.cipher.decrypt(b64decode(data)))