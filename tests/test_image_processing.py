import io

import numpy as np

from utils.image_processing import ndarray2bytes, convert2rgb


def test_ndarray2bytes():
    shape = (20, 20, 3)
    arr = np.ones(shape) * 255
    arr = arr.astype('uint8')
    assert isinstance(ndarray2bytes(arr), io.BytesIO)


def test_convert2rgb():
    shape = (20, 20, 3)
    img = np.ones(shape) * 255
    img = img.astype('uint8')
    assert convert2rgb(img).shape == img.shape

