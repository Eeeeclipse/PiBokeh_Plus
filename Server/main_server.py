from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pibokeh_v4 import *
from img_transform import *
from server_generate_keys import *
from crypto_img import * 
server_private_key, server_public_key = generate_server_keys()
public_key = server_public_key.export_key()
private_key = server_private_key
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(public_key)

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        file_content = self.rfile.read(content_length)
        json_file = json.loads(file_content.decode('utf8'))
        img_encrypt = json_file['image']
        encrypt_order = json_file['encrypt_order']
        client_public_key = json_file['public_key']
        focus_point_m = json_file['focus_point'].split(',')
        focus_point = (int(focus_point_m[0]),int(focus_point_m[1]))
        img_decrypt = decrypto_imgb64(img_encrypt, encrypt_order, private_key)
        img_b64 = bytes(img_decrypt, 'utf8')
        img_a = img_b642a(img_b64)

        bokeh_img_a = pibokeh_v4(img_a, focus_point)
        bokeh_img_b64 = img_a2b64(bokeh_img_a)
        bokeh_img_b64 = bokeh_img_b64.decode('utf8')
        img_encrypt, encrypt_order = encrypto_imgb64(bokeh_img_b64, client_public_key)
        body = {'img_encrypt':img_encrypt ,'encrypt_order':encrypt_order}
        self.wfile.write(bytes(json.dumps(body), 'utf8'))

if __name__ == '__main__':
    with HTTPServer(('', 8888), handler) as server:
        server.serve_forever()