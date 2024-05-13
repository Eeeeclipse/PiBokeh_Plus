import requests
import json
from crypto_img import *
from img_transform import *

def online_inference(url, img, focus_point, server_public_key, public_key, private_key):
    img_b64 = img_a2b64(img)
    img_encoded = img_b64.decode('utf8')
    img_, encrypt_order = encrypto_imgb64(img_encoded, server_public_key)
    focus_point_m = str(focus_point[0])+','+str(focus_point[1])
    body = {'public_key':public_key ,'image':img_, 'focus_point':focus_point_m, 'encrypt_order':encrypt_order}
    r = requests.post(url, json.dumps(body)).content
    json_file = json.loads(r.decode('utf8'))
    img_encrypt = json_file['img_encrypt']
    encrypt_order = json_file['encrypt_order']
    img_decrypt = decrypto_imgb64(img_encrypt, encrypt_order, private_key)
    bokeh_img_a = img_b642a(img_decrypt)
    return bokeh_img_a

def enable_online_inference(url):
    server_public_key = None
    can_online_inference = False
    try:
        server_public_key = requests.get(url).content
        can_online_inference = True
    except:
        server_public_key = 'Error! Client or server is offline!'
    return can_online_inference, server_public_key

