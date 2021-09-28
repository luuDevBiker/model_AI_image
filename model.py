import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2 as cv
import cv2

import numpy as np

#  mảng các nhãn kết quả
arr_name_lable = ['số 1','số 2','số 3','số 4','số 5','số 6','số 7','số 8','số 9']
#  load model đã được train sẵn
model_CP2 = tf.keras.models.load_model(r'C:\Users\admin\Documents\pythonProject\img_train_CP2.h5')

#  hàm in nhãn dự đoán được từ model
def plot_image(predictions_array, img):
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])

  plt.imshow(img.reshape(28,28))

  predict_label = np.argmax(predictions_array)
  color = 'red'

  if 100*np.max(predictions_array)< 85:
    note = 'kiểm tra lại'
  else :
    note = '...'
  plt.xlabel("{} {:2.0f}% {}".format(arr_name_lable[predict_label-1],
             100*np.max(predictions_array),note),
             color=color
             )

#  hàm chuyển đổi màu của hình ảnh về ảnh nhị phân
def convert_to_binary(img_grayscale, thresh=100):
  thresh, img_binary = cv.threshold(img_grayscale, thresh, maxval=255, type=cv.THRESH_BINARY)
  return img_binary

#  đọc ảnh từ thư viện bằng openCV2
img = cv2.imread(r'C:\Users\admin\Pictures\5.jpg')

img = np.array(255*(img / 255) ** 1, dtype = 'uint8')

# chuyển ảnh về ảnh xám
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# chuyển về ảnh đen trắng
img = cv2.adaptiveThreshold(img,255 , cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 199, 1)
# khung - nốt chuyển đổi ảnh
kernel = np.ones((2,2), np.uint8)
# xóa đừng bao của nét chữ - làm mảnh nét chữ
img = cv2.erode(img, kernel, iterations=4)
img = ~cv2.resize(img, (28, 28))
# reshape kich thước để phù hợp định dạng ảnh với model
img = img.reshape(1, 28, 28, 1)
#  dùng model để nhận diện ảnh đưa vào
img_rs = model_CP2.predict(img)

# hiện kết qủa dự đoán lên màn hình
plt.figure(figsize=(6, 3))
plt.subplot(1, 2, 1)
plot_image(img_rs, img)
plt.show()
cv.waitKey()

