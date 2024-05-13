from Client import online_inference, enable_online_inference
from pibokeh_v4 import pibokeh_v4
from PIL import Image
import numpy as np
from take_picture import take_picture
import time
from client_generate_keys import *
import argparse
import matplotlib.pyplot as plt
from PIL import Image
can_online_inference = False
server_public_key = None
client_private_key, client_public_key = generate_client_keys()
# Your server's ip address
url = 'http://192.168.1.255:8888' 
public_key = client_public_key.export_key().decode("utf8")
private_key = client_private_key



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--online', default=False, type=bool)
    args = parser.parse_args()
    if args.online:
        can_online_inference, server_public_key = enable_online_inference(url)
        if not can_online_inference:
            assert False, server_public_key
    img = take_picture()
    img_ = Image.fromarray(img)
    img_.save('Origin.jpg')
    plt.imshow(img)
    pts = plt.ginput(1, timeout=20)
    plt.close()
    focus_point = (int(pts[0][1]), int(pts[0][0]))
    start = time.perf_counter()
    if args.online:
        if can_online_inference:
            bokeh_img_a = online_inference(url, img, focus_point, server_public_key, public_key, private_key).astype(np.uint8)
            bokeh_img = Image.fromarray(bokeh_img_a)
            bokeh_img.show()            
    else:
        bokeh_img_a = pibokeh_v4(img, focus_point).astype(np.uint8)
        bokeh_img = Image.fromarray(bokeh_img_a)
        bokeh_img.show()
    bokeh_img.save('bokeh.jpg')
    print('Running time: ' + str(time.perf_counter() - start))
