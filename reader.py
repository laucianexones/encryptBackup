# -*- encoding: utf-8 -*-
import os
# pip install pycryptodomex
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
#from Crypto.Random import get_random_bytes

AESKEYLEN = 16
SALTLEN = 16
NUMBEROFKEYS = 1
SCRYPT_N, SCRYPT_r, SCRYPT_p = 1048576, 8, 1

def transportsafe(mystring):
    return mystring.encode('utf-8')

password = transportsafe("Aglama Dalai Lama")
salt = os.urandom(SALTLEN)

key = scrypt(password, salt, AESKEYLEN, SCRYPT_N, SCRYPT_r, SCRYPT_p, NUMBEROFKEYS)
cipher = AES.new(key, AES.MODE_EAX)

data = transportsafe("this is a super secret text")
ciphertext, tag = cipher.encrypt_and_digest(data)
file_out = open("encrypted.bin", "wb")
[file_out.write(x) for x in cipher.nonce, tag, ciphertext]
file_out.close()

print 'encrypted text : %s' % ciphertext


file_in = open("encrypted.bin", "rb")
nonce, tag, ciphertext = [ file_in.read(x) for x in (16, 16, -1) ]

cipher = AES.new(key, AES.MODE_EAX, nonce)
decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

print 'decrypted text : %s' % decrypted_data
