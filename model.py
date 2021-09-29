import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2 as cv
import cv2
import numpy as np

#  mảng các nhãn kết quả
arr_name_lable = ['số 1','số 2','số 3','số 4','số 5','số 6','số 7','số 8','số 9']
#  load model đã được train sẵn
model_CP2 = tf.keras.models.load_model(r'C:\Users\admin\Documents\model_AI\img_train_CP2.h5')
#  hàm in nhãn dự đoán được từ model
def plot_image(predictions_array):
  predict_label = np.argmax(predictions_array)
  if 100*np.max(predictions_array)< 85:
    note = 'kiểm tra lại'
  else :
    note = ''
  return ""+arr_name_lable[predict_label-1] +" "+note

"""
- hàm nhận đầu vào là 1 mảng đường dẫn ảnh ảnh màu
- ảnh sẽ được chuyển đổi từ ảnh màu về ảnh nhị phân chuẩn đầu vào của model
- ảnh sau khi được xử lý sẽ được thêm vào mảng
- hàm sẽ trả về mảng ảnh để chuẩn bị cho việc nhận diện bằng model
"""
def result_array_image(array_path):
    array_image = []
    for i in range(len(array_path)):
        #  đọc ảnh từ thư viện bằng openCV2
        img = cv2.imread(array_path[i])
        img = np.array(255 * (img / 255) ** 1, dtype='uint8')
        # chuyển ảnh về ảnh xám
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # chuyển về ảnh đen trắng
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 199, 1)
        # khung - nốt chuyển đổi ảnh
        kernel = np.ones((2, 2), np.uint8)
        # xóa đừng bao của nét chữ - làm mảnh nét chữ
        img = cv2.erode(img, kernel, iterations=4)
        img = ~cv2.resize(img, (28, 28))
        # reshape kich thước để phù hợp định dạng ảnh với model
        img = img.reshape(1, 28, 28, 1)
        # thêm ảnh vào mảng ảnh
        array_image.append(img)
    return  array_image
"""
hàm nhận giá trị đầu vào là một mảng ảnh sau khi nhận diện sẽ trả về một mảng kết quả
"""
def array_result(array_image):
    #  dùng model để nhận diện ảnh đưa vào
    array_result_model = model_CP2.predict(array_image)
    return array_result_model
