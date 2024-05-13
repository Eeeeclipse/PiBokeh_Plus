from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import random
import base64
def gen_order():
    ol = random.sample('0123456789', 10)
    out = ''
    for c in ol:
        out += c 
    return out

def deshuffle_order(order):
    order_r = ''
    for i in range(int(len(order))):
        order_r += str(order.index(str(i)))
    return order_r

def shuffle(order, b):
    num = len(order)
    rest_num = len(b) % num
    step = len(b) // num
    out = ''
    for i in range(num):
        out += b[int(order[i]) * step: (int(order[i])+1) * step]
    out += b[-rest_num:]
    return out

def deshuffle(order, b):
    order_r = deshuffle_order(order)
    out = shuffle(order_r, b)
    return out

def encrypt_data(public_key, order):
    cipher = PKCS1_cipher.new(public_key)
    encrypt_text = base64.b64encode(cipher.encrypt(bytes(order.encode("utf8"))))
    return encrypt_text.decode('utf-8')

def decrypt_data(private_key, encrypt_order):
    cipher = PKCS1_cipher.new(private_key)
    back_text = cipher.decrypt(base64.b64decode(encrypt_order), 0)
    return back_text.decode('utf-8')

def encrypto_imgb64(b, public_key):
    # b = b.decode('utf-8')
    public_key = RSA.import_key(public_key)
    order = gen_order()
    b_shuffled = shuffle(order, b)
    encrypt_order = encrypt_data(public_key, order)
    return b_shuffled, encrypt_order
def decrypto_imgb64(b, encrypt_order, private_key):
    decrypt_order = decrypt_data(private_key, encrypt_order)
    b_restored = deshuffle(decrypt_order, b)
    return b_restored