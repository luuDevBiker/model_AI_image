import tensorflow as tf
import cv2 as cv
import cv2
import numpy as np
import os
from sklearn.utils import shuffle
from pathlib import Path
import shutil
image = []
label = []
path = r'img/'
path_img_data_new = r'cropped/'


def convert_image(image):
    arr_indexnumber = []
    kernel = np.ones((2, 2), np.uint8)
    im3 = cv2.erode(image, kernel, iterations=2)
    gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        try:
            if cv2.contourArea(cnt) > 100:
                [x, y, w, h] = cv2.boundingRect(cnt)
                roi = im3[y - 6: y + h + 6, x - 6: x + w + 6]
        except Exception as e:
            print('error re_num : ', e)
    img = roi
    img = ~cv2.resize(img, (28, 28))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(img, (28, 28))
    return resized / 255.00


def load_data():
    print('load data')
    listFolder = os.listdir(path)
    for path_Jr in listFolder:
        for path_im in os.listdir(path + path_Jr):
            img = cv2.imread(path + path_Jr + "/" + path_im, cv.IMREAD_GRAYSCALE)
            resized = cv2.resize(img, (28, 28))
            features = resized / 255.00
            image.append(features)
            label.append(np.uint8(path_Jr))


    listFolder = os.listdir(path_img_data_new)
    for jr in listFolder:
        listimage = os.listdir(path_img_data_new + '/' + jr)
        for path_im_jr in listimage:
            im = cv2.imread(path_img_data_new + jr + '/' + path_im_jr)
            lenObj = len(os.listdir(r'img/' + jr))
            cv2.imwrite(r'img/' + jr + '/' + str(lenObj) + '.jpg', im)
            # print(r'img/' + jr + '/' + str(lenObj) + '.jpg')
            im = convert_image(im)
            image.append(im)
            label.append(np.uint8(jr))
    print('load data done')


def load_model():
    print('Load model')
    model_CP2 = tf.keras.models.load_model('img_train_CP2.h5')
    model_CP2.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    print('Load model done')
    return model_CP2


model_CP2 = load_model()


def train_epoch():
    x = np.asarray(image)
    y = np.asarray(label)
    model_CP2.fit(x, y, epochs=1)


def clearn_folder():
    print('Clearn Data')
    listFolder = os.listdir(path_img_data_new)
    for jr in listFolder:
        listimage = os.listdir(path_img_data_new + '/' + jr)
        for path_im_jr in listimage:
            os.remove(path_img_data_new + '/' + jr + '/' + path_im_jr)
    print('Clearn data done')


def save_model():
    dirpath = Path('model')
    if dirpath.exists() and dirpath.is_dir():
        sttmodel = len(os.listdir('model'))
        model_CP2.save('model/model_version_' + str(sttmodel) + '.H5')
    else:
        os.mkdir('model')
        sttmodel = len(os.listdir('model'))
        model_CP2.save('model/model_version_' + str(sttmodel) + '.H5')
