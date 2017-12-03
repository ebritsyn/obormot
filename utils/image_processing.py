import numpy as np
import matplotlib.pyplot as plt
import cv2
import keras
from keras.models import model_from_json

model = model_from_json(open('../data/model/model.json').read())
model.load_weights('../data/model/weights.h5')


def convert2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def get_faces(img):
    image = np.array(img)
    face_cascade = cv2.CascadeClassifier('../data/model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image


def get_smiles(img, show=False):
    image = np.array(img)
    smile_cascade = cv2.CascadeClassifier("../data/model/haarcascade_smile.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    smiles = smile_cascade.detectMultiScale(gray, 1.1, 60)

    for (x, y, w, h) in smiles:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return image


def add_stickers(img, corners, labels, sticker_size):
    smiley = cv2.imread('../data/pics/smiling.png')
    neutral = cv2.imread('../data/pics/neutral.png')
    smiley = cv2.resize(smiley, (sticker_size, sticker_size))
    neutral = cv2.resize(neutral, (sticker_size, sticker_size))
    image = np.array(img)
    t2 = sticker_size
    t1 = sticker_size - t2
    for i in range(len(labels)):
        try:
            corner_x, corner_y = corners[i]
            if labels[i] == 1:
                image[corner_x - t1:corner_x + t2, corner_y - t2:corner_y + t1] = smiley
            else:
                image[corner_x - t1:corner_x + t2, corner_y - t2:corner_y + t1] = neutral
        except:
            print("EXCEPTION")
            continue

    return image


def find_faces_n_get_labels(img):
    image = np.array(img)
    face_cascade = cv2.CascadeClassifier('../data/model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    cropped_faces = []
    labels = []
    corners = []
    for (x, y, w, h) in faces:
        corners.append((y, x + w))
        img_cropeed = img[y:y + h, x:x + w]
        cropped_faces.append(img_cropeed)
        gray_cr_res = cv2.cvtColor(cv2.resize(img_cropeed, (32, 32)), cv2.COLOR_BGR2GRAY)
        gray_cr_res = np.reshape(gray_cr_res, (32, 32, 1)) / 255
        score = model.predict(np.array([gray_cr_res]))[0][1]
        label = round(score)
        labels.append(label)

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    sticker_size = int(np.median(list(map(lambda x: x.shape[0], cropped_faces)))) // 3
    image = add_stickers(image, corners, labels, sticker_size)
    return image



