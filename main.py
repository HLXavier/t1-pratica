from sys import argv
from utils import *
from ciphers import *
from PIL import Image
from avalanche import avalanche_effect
from entropy import entropy
from image import transform_image
from histogram import histogram
from execution_time import time
from correlation import correlation
from npcr_uaci import npcr_uaci


cipher = argv[1] 
op = argv[2]

ciphers = {
    'aes': [aes_encrypt, aes_decrypt, 16],
    '3des': [triple_des_encrypt, triple_des_decrypt, 16],
    'blowfish': [blowfish_encrypt, blowfish_decrypt, 16],
}

encrypt = ciphers[cipher][0]
decrypt = ciphers[cipher][1]
key_size = ciphers[cipher][2]


def _avalanche():
    encryption_rounds = int(argv[3])

    key = random_bytes(key_size)

    print(f'AVALANCHE: {avalanche_effect(encrypt, key, encryption_rounds)}')


def _entropy():
    path = argv[3]

    image = Image.open(path)

    print(f'ENTROPY: {entropy(image)}') 


def _enc_image():
    path = argv[3]
    rounds = int(argv[4]) if len(argv) >= 5 else None

    image = Image.open(path)
    key = random_bytes(key_size)
    encrypted_image = transform_image(image, encrypt, key, rounds=rounds)

    text_key = hex_to_str(key).replace(' ', '')
    print(f'KEY: {text_key}')

    rounds_label = rounds if rounds is not None else "default"
    path = path.replace('images/', f'images/encrypted_{argv[1]}_{rounds_label}_rounds_')
    encrypted_image.save(path)


def _dec_image():
    path = argv[3]
    key = argv[4]

    key = separete_hex(key)
    key = str_to_hex(key)

    image = Image.open(path)
    encrypted_image = transform_image(image, decrypt, key)

    path = path.replace('images/encrypted_', 'images/decrypted_')
    encrypted_image.save(path)
    

def _histogram():
    path = argv[3]

    image = Image.open(path)
    title = path.replace('images/', '')

    histogram(image, title)


def _time():
    size = int(argv[3])
    path = argv[4]

    image = Image.open(path)
    image = image.resize((size, size))

    key = random_bytes(key_size)
    encrypt_image = lambda: transform_image(image, encrypt, key)
    encryption_time = time(encrypt_image)

    print(f'TIME: {encryption_time}')


def _correlation():
    path = argv[3]
    
    pearson_correlation = correlation(path, f'plots/correlation_{path.replace("images/", "")}')
    print('PEARSON CORRELATION: ', pearson_correlation)

def _npcr_uaci():
    npcr_uaci(argv[3], encrypt, random_bytes(key_size), None)

ops = {
    'avalanche': _avalanche,
    'entropy': _entropy,
    'enc-image': _enc_image,
    'dec-image': _dec_image,
    'histogram': _histogram,
    'time': _time,
    'correlation': _correlation,
    'npcr-uaci': _npcr_uaci,
}

op = ops[op]
op()
