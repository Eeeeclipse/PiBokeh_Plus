from PIL import Image
from io import BytesIO
import numpy as np
import base64
def img_a2b(img_a):
    img = Image.fromarray(img_a.astype(np.uint8))
    img_b = BytesIO()
    img.save(img_b, format='JPEG')
    img_b = img_b.getvalue()
    return img_b

def img_a2b64(img_a):
    img_b = img_a2b(img_a)
    img_b64 = base64.b64encode(img_b)
    return img_b64

def img_b2a(img_b):
    img_a = Image.open(BytesIO(img_b))
    return np.array(img_a)

def img_b2Img(img_b):
    img = Image.open(BytesIO(img_b))
    return np.array(img)

def img_b642a(img_b64):
    img_b = base64.b64decode(img_b64)
    img_a = Image.open(BytesIO(img_b))
    return np.array(img_a)

def img_b642Img(img_b64):
    img_b = base64.b64decode(img_b64)
    img = Image.open(BytesIO(img_b))
    return np.array(img)