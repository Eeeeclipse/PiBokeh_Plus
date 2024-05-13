from PIL import Image
import numpy as np
import cv2

from helper_v4 import mfft, gen_kernel, fft_convolve, da_infer, standardize_output, slice_input

def pibokeh_v4(image, focus_point):
    x_input_img, y_input_img, c = image.shape
    image = cv2.resize(image, (y_input_img - y_input_img % 14, x_input_img - x_input_img % 14))
    depth_range = int(image.shape[0] / 25)
    kernels = gen_kernel(depth_range)
    output = da_infer('da.onnx', image)
    output_ = standardize_output(output, depth_range, focus_point)
    sliced_image = slice_input(image, output_)
    out = fft_convolve(sliced_image, kernels, depth_range)
    return out