from Crypto import Random
from Crypto.PublicKey import RSA
import os
def get_key(key_file):
    with open(key_file) as f:
        data = f.read()
        key = RSA.importKey(data)
    return key

def generate_client_keys():
    if os.path.exists('client_private_key.pem') and os.path.exists('client_public_key.pem'):
        pass
    else:
        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
        with open('client_private_key.pem', 'wb')as f:
            f.write(private_key)
            
        with open('client_public_key.pem', 'wb')as f:
            f.write(public_key)
    return (get_key('client_private_key.pem'), get_key('client_public_key.pem'))

