from utils import *
from aes import AES
import triple_des as triple_des
import blowfish


def aes_encrypt(plain_text, key, rounds=None):
    aes = AES(key)
    aes.nr = 10 if rounds is None else rounds
    return aes.encrypt(plain_text)


def aes_decrypt(cipher_text, key, rounds=None):
    aes = AES(key)
    aes.nr = 10 if rounds is None else rounds
    return aes.decrypt(cipher_text)


def triple_des_encrypt(plain_text, key, rounds=None):
    tdes = triple_des.triple_des(key, triple_des.CBC, rounds=16 if rounds is None else rounds)
    return tdes.encrypt(plain_text)


def triple_des_decrypt(plain_text, key, rounds=None):
    tdes = triple_des.triple_des(key, triple_des.CBC, rounds=16 if rounds is None else rounds)
    return tdes.decrypt(plain_text)


def blowfish_encrypt(plain_text, key, rounds=None):
    cipher = blowfish.Cipher(key)
    iv = key[:8]
    return b"".join(list(cipher.encrypt_cbc(plain_text, iv, rounds=16 if rounds is None else rounds)))

def blowfish_decrypt(cipher_text, key, rounds=None):
    cipher = blowfish.Cipher(key)
    iv = key[:8]
    return b"".join(list(cipher.decrypt_cbc(cipher_text, iv, rounds=16 if rounds is None else rounds)))

