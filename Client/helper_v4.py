import numpy as np
import onnxruntime as ort
import scipy.signal as sy
import multiprocessing as mp

def normalize(image, mean, std):
    for channel in range(3):
        image[:, :, channel] = (image[:, :, channel] - mean[channel]) / std[channel]
    return image

def process(image):
    new_img = np.transpose(image, (2, 0, 1))
    new_img = np.ascontiguousarray(new_img).astype(np.float32)
    return new_img

def transform(image):
    image = image / 255
    image = normalize(image, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    image = process(image)
    return image[np.newaxis,...]

def gen_kernel(kernel_size):
    kernels = np.zeros((kernel_size, kernel_size + 1, kernel_size + 1))
    for i in range(kernel_size):
        kernel = np.zeros((kernel_size + 1, kernel_size + 1))
        for j in range(kernel_size + 1):
            for k in range(kernel_size + 1):
                if (j - int((kernel_size+1)/2) )**2 + (k - int((kernel_size+1)/2))**2 <= (i/2)**2:
                    kernel[j, k] = 1
        kernel = kernel / kernel.sum()
        kernels[i] = kernel
    return kernels

def fft_convolve(imgs, kernels, depth_range):
    conv0 = sy.fftconvolve(imgs[0,:,:,0], kernels[0], mode='same')
    conv1 = sy.fftconvolve(imgs[0,:,:,1], kernels[0], mode='same')
    conv2 = sy.fftconvolve(imgs[0,:,:,2], kernels[0], mode='same')
    for i in range(1,depth_range):
        conv0 += sy.fftconvolve(imgs[i,:,:,0], kernels[i], mode='same')
        conv1 += sy.fftconvolve(imgs[i,:,:,1], kernels[i], mode='same')
        conv2 += sy.fftconvolve(imgs[i,:,:,2], kernels[i], mode='same')
    out1 = np.stack((conv0, conv1, conv2), axis = 2)
    out1[out1 < 0] = 0
    out1[out1 > 255] = 255
    return out1

def mfft_helper(imgs, kernels):
    conv0 = sy.fftconvolve(imgs[0,:,:,0], kernels[0], mode='same')
    conv1 = sy.fftconvolve(imgs[0,:,:,1], kernels[0], mode='same')
    conv2 = sy.fftconvolve(imgs[0,:,:,2], kernels[0], mode='same')
    for i in range(1,len(kernels)):
        conv0 += sy.fftconvolve(imgs[i,:,:,0], kernels[i], mode='same')
        conv1 += sy.fftconvolve(imgs[i,:,:,1], kernels[i], mode='same')
        conv2 += sy.fftconvolve(imgs[i,:,:,2], kernels[i], mode='same')
    out1 = np.stack((conv0, conv1, conv2), axis = 2)
    return out1

def mfft(imgs, kernels, depth_range):
    num_cores = 8
    pool = mp.Pool(num_cores)
    task_split = []
    size = depth_range // num_cores
    for i in range(num_cores):
        if i != num_cores - 1:
            task_split.append((imgs[i * size:(i+1) * size], kernels[i * size:(i+1) * size]))
        else:
            task_split.append((imgs[i * size:], kernels[i * size:]))
    results = [pool.apply_async(mfft_helper, args=(imgs, kernels)) for imgs, kernels in task_split]
    out = np.zeros(imgs[0].shape)
    for p in results:
        out += p.get()
    out[out < 0] = 0
    out[out > 255] = 255
    return out

def da_infer(model_filename, input):
    session = ort.InferenceSession(model_filename)
    depth = session.run(None, {"image": transform(input)})[0][0,0]
    depth = (depth - depth.min()) / (depth.max() - depth.min())
    return depth


def standardize_output(output, depth_range, focus_point):
    x, y = focus_point
    output_ = abs(output - output[int(x), int(y)])
    output_ = np.round((depth_range - 1) * output_ / output_.max())
    output_ = output_.astype(np.uint8)
    return output_

def slice_input(image, output):
    imgs = []
    for i in range(output.min(), output.max()+1):
        temp_img = np.zeros(image.shape)
        idx_x, idx_y = np.where(output == i)
        idxs = np.vstack((idx_x, idx_y)).T
        for idx in idxs:
            temp_img[idx[0],idx[1]] = image[idx[0],idx[1]]
        imgs.append(temp_img)
    return np.array(imgs)