AES_KEY = "zbMQ2xPVLyF6Apzn"
PY_SSIZE_T_CLEAN = "#"
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import utilum
import os
from . import utils
import sys

ENCRYPT = 'encrypt'
DECRYPT= 'decrypt'

class Crypt:
    def __init__(self, salt='4dRt45#$3T45hyh7'):
        self.salt = salt.encode('utf8')
        self.enc_dec_method = 'utf-8'

    def encrypt(self, str_to_enc, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf-8'), AES.MODE_CFB, self.salt)
            hx_enc = aes_obj.encrypt(str_to_enc.encode('utf8'))
            mret = b64encode(hx_enc).decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError(
                    'Encryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError(
                    'Encryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)

    def decrypt(self, enc_str, str_key):
        try:
            aes_obj = AES.new(str_key.encode('utf8'), AES.MODE_CFB, self.salt)
            str_tmp = b64decode(enc_str.encode(self.enc_dec_method))
            str_dec = aes_obj.decrypt(str_tmp)
            mret = str_dec.decode(self.enc_dec_method)
            return mret
        except ValueError as value_error:
            if value_error.args[0] == 'IV must be 16 bytes long':
                raise ValueError(
                    'Decryption Error: SALT must be 16 characters long')
            elif value_error.args[0] == 'AES key must be either 16, 24, or 32 bytes long':
                raise ValueError(
                    'Decryption Error: Encryption key must be either 16, 24, or 32 characters long')
            else:
                raise ValueError(value_error)
cr = Crypt()

def runCommand(config):
    command = ENCRYPT
    if(len(sys.argv)>=2):
        if(sys.argv[1]==ENCRYPT):
            command = ENCRYPT
        if(sys.argv[1]==DECRYPT):
            command = DECRYPT
            
    password = utilum.file.readFile(os.path.join(config.credsFolderPath, 'password.txt'))
    salt = utilum.file.readFile(os.path.join(config.credsFolderPath, 'salt.txt'))
    encryptedKey = cr.encrypt(password + salt, AES_KEY)
        
    if(command == ENCRYPT):
        utils.folderEncrypt(config.storageRepoPath, encryptedKey)
    if(command == DECRYPT):
        utils.folderDecrypt(config.storageRepoPath, encryptedKey)
    return
