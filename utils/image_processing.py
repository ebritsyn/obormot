import numpy as np
import cv2
import io
from PIL import Image
from keras.models import model_from_json


def convert2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def add_s(roi, img2):
    rows,cols,channels = img2.shape
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    img1_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
    img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
    dst = cv2.add(img1_bg,img2_fg)
    return dst

def add_stickers(img, corners, labels, sticker_size, sizes):

    smiley = cv2.imread('data/pics/smiling.png')
    neutral = cv2.imread('data/pics/neutral.png')

    smiley = cv2.cvtColor(smiley, cv2.COLOR_BGR2RGB)
    neutral = cv2.cvtColor(neutral, cv2.COLOR_BGR2RGB)


    smiley = cv2.resize(smiley, (sticker_size, sticker_size))
    neutral = cv2.resize(neutral, (sticker_size, sticker_size))
    image = np.array(img)
    t2 = sticker_size
    t1 = sticker_size - t2
    for i in range(len(labels)):
        try:
            corner_x, corner_y = corners[i]
            a = (sizes[i] - t2) // 2
            if labels[i] == 1:
                image[corner_x - t1:corner_x + t2, corner_y - t2 - a:corner_y + t1 - a] = add_s(
                    image[corner_x - t1:corner_x + t2, corner_y - t2 - a:corner_y + t1 - a], smiley)
            else:
                image[corner_x - t1:corner_x + t2, corner_y - t2 - a:corner_y + t1 - a] = add_s(
                    image[corner_x - t1:corner_x + t2, corner_y - t2 - a:corner_y + t1 - a], neutral)
        except:
            print("EXCEPTION")
            continue

    return image


def find_faces_n_get_labels(img):
    img = bytes2ndarray(img)
    image = img
    model = model_from_json(open('data/model/model.json').read())
    model.load_weights('data/model/weights.h5')
    face_cascade = cv2.CascadeClassifier('data/model/haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    cropped_faces = []
    labels = []
    corners = []
    sizes = []
    for (x, y, w, h) in faces:
        sizes.append(w)
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
    image = add_stickers(image, corners, labels, sticker_size, sizes)
    return ndarray2bytes(image)


def ndarray2bytes(array):
    buf = io.BytesIO()
    Image.fromarray(array).save(buf, format="jpeg")
    return buf


def bytes2ndarray(buf):
    image = np.array(Image.open(buf))
    return image
