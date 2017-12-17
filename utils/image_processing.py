import io
import cv2
import numpy as np
from PIL import Image
import dlib
from keras.models import model_from_json
import tensorflow as tf


class Model:

    def __init__(self):
        self.model = model_from_json(open('data/model/model.json').read())
        self.model.load_weights('data/model/weights.h5')
        self.graph = tf.get_default_graph()

    @staticmethod
    def convert2rgb(img):

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def rect_to_bb(rect):

        rect_x = rect.left()
        rect_y = rect.top()
        rect_w = rect.right() - rect_x
        rect_h = rect.bottom() - rect_y
        return (rect_x, rect_y, rect_w, rect_h)

    def get_faces(self, img):

        image = img
        detector = dlib.get_frontal_face_detector()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        faces = []
        for rect in rects:
            faces.append(self.rect_to_bb(rect))
        return faces

    def get_smile_label(self, img_face):

        gray_cr_res = cv2.cvtColor(cv2.resize(img_face, (32, 32)),
                                   cv2.COLOR_BGR2GRAY)
        gray_cr_res = np.reshape(gray_cr_res, (32, 32, 1)) / 255

        with self.graph.as_default():
            score = self.model.predict(np.array([gray_cr_res]))[0][1]

        threshold = 0.12
        if score > threshold:
            label = 1
        else:
            label = 0
        return label

    @staticmethod
    def get_sticker_backgr(backgr, sticker):

        sticker_gray = cv2.cvtColor(sticker, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(sticker_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        backgr_bg = cv2.bitwise_and(backgr, backgr, mask=mask_inv)
        sticker_fg = cv2.bitwise_and(sticker, sticker, mask=mask)
        merged = cv2.add(backgr_bg, sticker_fg)
        return merged

    @staticmethod
    def get_sticker_size(faces):

        heights = list(map(lambda x: x[2], faces))
        return int(np.mean(heights) / 2.5)

    def add_stickers(self, img, faces, labels):

        st_size = self.get_sticker_size(faces)
        smiley = cv2.imread('data/pics/smiling.png')
        neut = cv2.imread('data/pics/neutral.png')

        smiley = cv2.cvtColor(smiley, cv2.COLOR_BGR2RGB)
        neut = cv2.cvtColor(neut, cv2.COLOR_BGR2RGB)

        smiley = cv2.resize(smiley, (st_size, st_size))
        neut = cv2.resize(neut, (st_size, st_size))

        image = np.array(img)
        for i, label in enumerate(labels):
            y_1 = faces[i][1] + faces[i][3] - st_size
            y_2 = faces[i][1] + faces[i][3]
            x_1 = faces[i][0] + faces[i][2] - st_size
            x_2 = faces[i][0] + faces[i][2]
            if label == 1:
                image[y_1:y_2, x_1:x_2] = \
                    self.get_sticker_backgr(image[y_1:y_2, x_1:x_2], smiley)
            else:
                image[y_1:y_2, x_1:x_2] = \
                    self.get_sticker_backgr(image[y_1:y_2, x_1:x_2], neut)

        return image

    def predict_labels(self, img):

        image = self.bytes2ndarray(img)
        faces = self.get_faces(image)
        num_faces = len(faces)
        labels = []
        if num_faces == 0:
            return num_faces, image
        for (f_x, f_y, f_w, f_h) in faces:
            img_cropped = image[f_y:f_y + f_h, f_x:f_x + f_w]

            label = self.get_smile_label(img_cropped)
            labels.append(label)
        color = (0, 255, 0)
        for (f_x, f_y, f_w, f_h) in faces:
            cv2.rectangle(image, (f_x, f_y), (f_x + f_w, f_y + f_h), color, 2)

        image = self.add_stickers(image, faces, labels)
        return num_faces, self.ndarray2bytes(image)

    @staticmethod
    def ndarray2bytes(array):

        buf = io.BytesIO()
        Image.fromarray(array).save(buf, format="jpeg")
        return buf

    @staticmethod
    def bytes2ndarray(buf):

        image = np.array(Image.open(buf))
        return image
