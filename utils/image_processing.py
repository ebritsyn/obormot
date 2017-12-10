import io

import cv2
import numpy as np
from PIL import Image
import dlib
from keras.models import model_from_json


def convert2rgb(img):

    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def rect_to_bb(rect):

    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


def get_faces(img):

    image = img
    detector = dlib.get_frontal_face_detector()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    faces = []
    for rect in rects:
        faces.append(rect_to_bb(rect))
    return faces


def get_smile_label(model, img_face):

    gray_cr_res = cv2.cvtColor(cv2.resize(img_face, (32, 32)),
                               cv2.COLOR_BGR2GRAY)
    gray_cr_res = np.reshape(gray_cr_res, (32, 32, 1)) / 255
    score = model.predict(np.array([gray_cr_res]))[0][1]
    threshold = 0.12
    if score > threshold:
        label = 1
    else:
        label = 0
    return label, score


def get_sticker_backgr(backgr, sticker):

    sticker_gray = cv2.cvtColor(sticker, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(sticker_gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    backgr_bg = cv2.bitwise_and(backgr, backgr, mask=mask_inv)
    sticker_fg = cv2.bitwise_and(sticker, sticker, mask=mask)
    merged = cv2.add(backgr_bg, sticker_fg)
    return merged


def get_sticker_size(faces):

    heights = list(map(lambda x: x[2], faces))
    return int(np.mean(heights) / 2.5)


def add_stickers(img, faces, labels, sticker_size):

    smiley = cv2.imread('data/pics/smiling.png')
    neut = cv2.imread('data/pics/neutral.png')

    smiley = cv2.cvtColor(smiley, cv2.COLOR_BGR2RGB)
    neut = cv2.cvtColor(neut, cv2.COLOR_BGR2RGB)

    smiley = cv2.resize(smiley, (sticker_size, sticker_size))
    neut = cv2.resize(neut, (sticker_size, sticker_size))

    image = np.array(img)
    t = sticker_size
    for i in range(len(labels)):
        x, y, w, h = faces[i]
        if labels[i] == 1:

            image[y+h-t:y+h, x+w-t:x+w] = \
                get_sticker_backgr(image[y+h-t:y+h, x+w-t:x+w], smiley)
        else:
            image[y+h-t:y+h, x+w-t:x+w] = \
                get_sticker_backgr(image[y+h-t:y+h, x+w-t:x+w], neut)

    return image


def find_faces_n_get_labels(img):

    model = model_from_json(open('data/model/model.json').read())
    model.load_weights('data/model/weights.h5')
    image = bytes2ndarray(img)
    # image = img
    faces = get_faces(image)
    num_faces = len(faces)
    labels = []
    scores = []
    if num_faces == 0:
        return num_faces, scores, image
    for (x, y, w, h) in faces:
        img_cropped = image[y:y + h, x:x + w]
        label, score = get_smile_label(model, img_cropped)
        labels.append(label)
        scores.append(score)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    sticker_size = get_sticker_size(faces)
    image = add_stickers(image, faces, labels, sticker_size)
    return num_faces, scores, ndarray2bytes(image)


def ndarray2bytes(array):

    buf = io.BytesIO()
    Image.fromarray(array).save(buf, format="jpeg")
    return buf


def bytes2ndarray(buf):

    image = np.array(Image.open(buf))
    return image
