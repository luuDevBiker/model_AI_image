import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2 as cv
import cv2
import numpy as np
import os

#  mảng các nhãn kết quả
arr_name_lable = ['số 1','số 2','số 3','số 4','số 5','số 6','số 7','số 8','số 9']
#  load model đã được train sẵn
model_CP2 = tf.keras.models.load_model(r'img_train_CP2.h5')

'''
hàm in nhãn dự đoán được từ model
nhận vào mảng kết quả dự đoán của hàm "array_result" 
trả về một chuỗi thông tin gồm tên số tương ứng với kết quả dự đoán của mảng và đề nghị kiểm tra lại nếu phần trăm dự đoán bé hơn 85%
'''
def plot_image(predictions_array):
  predict_label = np.argmax(predictions_array)
  return ""+arr_name_lable[predict_label-1] +" : "+str(  round(100*np.max(predictions_array),2)) + ' %'

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
        img = img.reshape(1, 28, 28, 1)
        # thêm ảnh vào mảng ảnh
        array_image.append(img)
    return  array_image
"""
hàm nhận giá trị đầu vào là một mảng ảnh được trả về từ hàm "result_array_image"
sau khi nhận diện sẽ trả về một mảng gồm các mảng kết quả kết quả 
"""
def array_result(array_image):
    array_result = []
    #  dùng model để nhận diện ảnh đưa vào
    for i in range(len(array_image)):
      # reshape kich thước để phù hợp định dạng ảnh với model
      result = model_CP2.predict(array_image[i])
      array_result.append(result)
    return array_result

def result_array_image_2(array_path):
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
        img = img.reshape(1, 28, 28, 1)
        # thêm ảnh vào mảng ảnh
        array_image.append(img)
    return  array_image

def array_result_2(array_image):
    array_result = []
    #  dùng model để nhận diện ảnh đưa vào
    for i in range(len(array_image)):
      # reshape kich thước để phù hợp định dạng ảnh với model
      result = model_CP2.predict(array_image[i])
      array_result.append(result)
    return array_result

def plot_image_2(predictions_array):
  predict_label = np.argmax(predictions_array)
  return ""+arr_name_lable[predict_label-1] +" : "+str(round(100*np.max(predictions_array),2)) + ' %'

def convert_image(image):
  img = image.copy
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
  img = img.reshape(1, 28, 28, 1)
  return img

def convert_color_befor_train(image_ip):
  arr_image_test = []
  image = image_ip.copy()
  kernal = np.zeros((90,90))
  # image = 230 - image
  # chuyển ảnh về ảnh xám
  image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # chuyển về ảnh đen trắng
  image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, 199, 1)
  # khung - nốt chuyển đổi ảnh
  kernel = np.ones((2, 2), np.uint8)
  # xóa đừng bao của nét chữ - làm mảnh nét chữ
  # image = cv2.erode(image, kernel, iterations = 1)
  image = cv2.dilate(image, kernel, iterations = 5)
  # image = 230 - image
  image = ~cv2.resize(image, (28, 28))
  arr = os.listdir('/content/drive/MyDrive/DataCrop')
  index = len(arr)
  cv2.imwrite('/content/drive/MyDrive/DataCrop/'+str(index)+'.jpg',image)
  plt.imshow(image)
  image = image.reshape(1, 28, 28, 1)
  arr_image_test.append(image)
  return arr_image_test

'''

def train_image():
  array_path_image = load_path_img()
  print('train image : len_path : ' , array_path_image)
  for valueim in array_path_image:
    print('Train image : ' , valueim)
    img = cv2.imread('/content/drive/MyDrive/img/'+valueim)
    arr_im = convert_color_befor_train(img)
    arr_rs = array_result(arr_im)
    rs = plot_image(arr_rs[0])
    print(valueim,'  ', rs)

def call_all():
  arr = os.listdir('/content/drive/MyDrive/Datasets/Anh_Mau')
  for i in arr:
    path = '/content/drive/MyDrive/Datasets/Anh_Mau/'+i
    print(path)
    crop_image_lagre(path)
    crop()
    train_image()
    print('Crop done')  


'''

