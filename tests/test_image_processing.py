import io

import numpy as np
import cv2

from utils.image_processing import ndarray2bytes, convert2rgb,\
    find_faces_n_get_labels


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


def test_find_faces_n_get_labels():
    test_img = cv2.imread("tests/test_image.jpg")
    num_faces, output_img = find_faces_n_get_labels(ndarray2bytes(test_img))
    assert num_faces >= 0 and isinstance(output_img, io.BytesIO)
