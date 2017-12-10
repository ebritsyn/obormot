import io

import numpy as np

from utils.image_processing import ndarray2bytes


def test_ndarray2bytes():
    shape = (20, 20, 3)
    arr = np.ones(shape) * 255
    arr = arr.astype('uint8')
    assert isinstance(ndarray2bytes(arr), io.BytesIO)
