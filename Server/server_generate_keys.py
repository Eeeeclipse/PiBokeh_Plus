from Crypto import Random
from Crypto.PublicKey import RSA
import os
def get_key(key_file):
    with open(key_file) as f:
        key = f.read()
        key = RSA.importKey(key)
    return key

def generate_server_keys():
    if os.path.exists('server_private_key.pem') and os.path.exists('server_public_key.pem'):
        pass
    else:
        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
        with open('server_private_key.pem', 'wb')as f:
            f.write(private_key)
        with open('server_public_key.pem', 'wb')as f:
            f.write(public_key)
    return (get_key('server_private_key.pem'), get_key('server_public_key.pem'))
