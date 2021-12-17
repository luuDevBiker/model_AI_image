import tensorflow as tf
import cv2 as cv
import cv2
import numpy as np
import os
from numpy import vstack
from numpy import hstack
from sklearn.utils import shuffle


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
        print('error re_num : ',e)
  img = roi
  img = ~cv2.resize(img, (28, 28))
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  resized = cv2.resize(img, (28,28))
  return resized/255.00
def retrain():
  print('retrain running')
  path = r'img/'
  listFolder = os.listdir(path)
  image_old = []
  label_old = []
  for path_Jr in listFolder:
    for path_im in os.listdir(path + path_Jr):
      img = cv2.imread(path + path_Jr + "/" + path_im, cv.IMREAD_GRAYSCALE)
      resized = cv2.resize(img, (28, 28))
      features = resized / 255.00
      image_old.append(features)
      label_old.append(np.uint8(path_Jr))
  path_img_data_new = r'cropped/'
  listFolder = os.listdir(path_img_data_new)
  image_new = []
  label_new = []
  for jr in listFolder :
    listimage = os.listdir(path_img_data_new+'/'+jr)
    for path_im_jr in listimage:
      im = cv2.imread(path_img_data_new+jr+'/'+path_im_jr)
      cv2.write(r'img/'+path_im_jr , img)
      im = convert_image(im)
      image_new.append(im)
      label_new.append(np.uint8(jr))

  model_CP2 = tf.keras.models.load_model('img_train_CP2.h5')
  model_CP2.compile(
      optimizer="adam",
      loss = "sparse_categorical_crossentropy",
      metrics=["accuracy"]
      )
  x = np.asarray(image_new)
  y = np.asarray(label_new)
  epochs = 50
  for i in range(epochs):
    model_CP2.fit(x,y , epochs = 1)

    # tiến trình được tính tại đây nhá


  for jr in listFolder :
    listimage = os.listdir(path_img_data_new+'/'+jr)
    for path_im_jr in listimage:
      os.remove(path_img_data_new+'/'+jr+'/'+path_im_jr)
  print('retrain done')


