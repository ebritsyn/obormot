import io
import cv2
import numpy as np
from PIL import Image
from keras.models import model_from_json
import tensorflow as tf
import dlib


class Model:
    """This class represents the base model of the whole project. The model
    predicts if the face on the picture is smiling or not. The model and
    its weights are being loaded from data/model/. The main method of the
    class is predict_labels(), which takes an input image, finds faces in
    this image, draws their boundary boxes and labels these faces by adding
    corresponding emojis on the picture.
    """
    def __init__(self):

        self.smiley = cv2.imread('data/pics/smiling.png')
        self.neutral = cv2.imread('data/pics/neutral.png')
        self.smiley = cv2.cvtColor(self.smiley, cv2.COLOR_BGR2RGB)
        self.neutral = cv2.cvtColor(self.neutral, cv2.COLOR_BGR2RGB)
        self.model = model_from_json(open('data/model/model.json').read())
        self.model.load_weights('data/model/weights.h5')
        self.graph = tf.get_default_graph()

    @staticmethod
    def convert2rgb(img):
        """Convert BGR image into RGB
            Parameters: img: ndarray
            :rtype: ndarray
        """
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    def rect_to_bb(rect):
        """Returns rectangle parameters from rectangle object
            Parameters: rect: object
            :rtype: list
        """
        rect_x = rect.left()
        rect_y = rect.top()
        rect_w = rect.right() - rect_x
        rect_h = rect.bottom() - rect_y
        return rect_x, rect_y, rect_w, rect_h

    def get_faces(self, img):
        """Find faces in the picture and return list of boundary boxes
        of found faces
            Parameters: img: ndarray
            :rtype: list
        """
        image = img
        detector = dlib.get_frontal_face_detector()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        faces = []
        for rect in rects:
            faces.append(list(self.rect_to_bb(rect)))
        return faces

    def get_smile_label(self, img_face):
        """Predict smile on a face and return label
        (0 for neutral and 1 for smiling face)
            Parameters: img_face: ndarray
            :rtype: int
        """
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
        """Merge a sticker and its background and return merged image
            Parameters: backgr: ndarray
                        sticker: ndarray
            :rtype: ndarray
        """
        sticker_gray = cv2.cvtColor(sticker, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(sticker_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        backgr_bg = cv2.bitwise_and(backgr, backgr, mask=mask_inv)
        sticker_fg = cv2.bitwise_and(sticker, sticker, mask=mask)
        merged = cv2.add(backgr_bg, sticker_fg)
        return merged

    @staticmethod
    def crop_face(bound_box, img):
        """Crop face from the input image according to its boundary box
            Parameters: bound_box: list
                        img: ndarray
            :rtype: ndarray
        """
        f_x, f_y, f_w, f_h = bound_box
        top, bottom, left, right = 0, 0, 0, 0
        if f_y < 0:
            top = - f_y
            f_y = 0

        if f_x < 0:
            left = - f_x
            f_x = 0

        if f_x + f_w > img.shape[1]:
            right = f_x + f_w - img.shape[1]
            f_w -= right

        if f_y + f_h > img.shape[0]:
            bottom = f_y + f_h - img.shape[0]
            f_h -= bottom
        img_cropped = img[f_y:f_y + f_h, f_x:f_x + f_w]

        img_cropped = cv2.copyMakeBorder(img_cropped,
                                         top, bottom, left, right,
                                         cv2.BORDER_REPLICATE)

        return img_cropped

    def add_stickers(self, img, faces, labels):
        """Add emoji sticker in the input picture according to predicted
        smile labels
            Parameters: img: ndarray of input image
                        faces: list of boundary boxes
                        labels: list of smile labels
            :rtype: ndarray
        """
        image = np.array(img)
        for i, label in enumerate(labels):

            if faces[i][0] < 0:
                faces[i][2] += faces[i][0]
                faces[i][0] = 0

            if faces[i][1] < 0:
                faces[i][3] += faces[i][1]
                faces[i][1] = 0

            if faces[i][0] + faces[i][2] > image.shape[1]:
                faces[i][2] = image.shape[1] - faces[i][0]

            if faces[i][1] + faces[i][3] > image.shape[0]:
                faces[i][3] = image.shape[0] - faces[i][1]

            st_size = int(min(faces[i][2], faces[i][3]) // 2.2)

            smiley = cv2.resize(self.smiley, (st_size, st_size))
            neutral = cv2.resize(self.neutral, (st_size, st_size))

            y_1 = faces[i][1] + faces[i][3] - st_size
            y_2 = faces[i][1] + faces[i][3]
            x_1 = faces[i][0] + faces[i][2] - st_size
            x_2 = faces[i][0] + faces[i][2]
            if label == 1:
                image[y_1:y_2, x_1:x_2] = \
                    self.get_sticker_backgr(image[y_1:y_2, x_1:x_2], smiley)
            else:
                image[y_1:y_2, x_1:x_2] = \
                    self.get_sticker_backgr(image[y_1:y_2, x_1:x_2], neutral)

        return image

    def predict_labels(self, img):
        """Predict if there smiles on picture and label faces with corresponding emoji
            Parameters: img: ndarray of input image
            :rtype: ndarray
        """
        image = self.bytes2ndarray(img)
        faces = self.get_faces(image)
        num_faces = len(faces)
        labels = []
        if num_faces == 0:
            return num_faces, image
        for bound_box in faces:
            img_cropped = self.crop_face(bound_box, image)
            label = self.get_smile_label(img_cropped)
            labels.append(label)
        color = (0, 255, 0)
        for (f_x, f_y, f_w, f_h) in faces:
            cv2.rectangle(image, (f_x, f_y), (f_x + f_w, f_y + f_h), color, 2)

        image = self.add_stickers(image, faces, labels)
        return num_faces, self.ndarray2bytes(image)

    @staticmethod
    def ndarray2bytes(array):
        """Convert image into bytes
            Parameters: array: ndarray
            :rtype: io.BytesIO
        """
        buf = io.BytesIO()
        Image.fromarray(array).save(buf, format="jpeg")
        return buf

    @staticmethod
    def bytes2ndarray(buf):
        """Convert image into bytes
            Parameters: buf: io.BytesIO
            :rtype: ndarray
        """
        image = np.array(Image.open(buf))
        return image
