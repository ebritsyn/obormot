from utils.image_processing import ndarray2bytes

import numpy as np
import io


def test_ndarray2bytes():
    s = (20, 20, 3)
    arr = np.ones(s) * 255
    arr = arr.astype('uint8')
    assert isinstance(ndarray2bytes(arr), io.BytesIO)