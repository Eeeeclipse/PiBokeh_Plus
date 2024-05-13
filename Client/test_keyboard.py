from pibokeh_v4 import pibokeh_v4
from PIL import Image
import numpy as np
import time
img = Image.open('img_s.jpg')
img_a = np.array(img)
start = time.perf_counter()
o = pibokeh_v4(img_a, (210,315))
print(o.shape)
print('Running time: ' + str(time.perf_counter() - start))
