import io

import numpy as np
import cv2

from utils.image_processing import Model

MODEL = Model()


def test_ndarray2bytes():
    shape = (20, 20, 3)
    arr = np.ones(shape) * 255
    arr = arr.astype('uint8')
    assert isinstance(MODEL.ndarray2bytes(arr), io.BytesIO)


def test_convert2rgb():
    shape = (20, 20, 3)
    img = np.ones(shape) * 255
    img = img.astype('uint8')
    assert MODEL.convert2rgb(img).shape == img.shape


def test_predict_labels():
    test_img = cv2.imread("tests/test_image.jpg")
    num_faces, output_img = MODEL.predict_labels(MODEL.ndarray2bytes(test_img))
    assert num_faces >= 0 and isinstance(output_img, io.BytesIO)
