import shutil

import tensorflow as tf
import os
import cv2
import numpy as np
import pathlib
from termcolor import colored
'''
code colab
'''

#  mảng các nhãn kết quả
arr_name_lable = ['1','2','3','4','5','6','7','8','9','0']
#  load model đã được train sẵn
model_CP2 = tf.keras.models.load_model('img_train_2.h5')
def crop_image_lagre(link):

  img = cv2.imread(link, 0)
  thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  img_bin = 255 - img_bin
  kernel_len = np.array(img).shape[1] // 100
  ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
  hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
  image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
  vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)

  image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
  horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)

  img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
  img_vh = cv2.erode(~img_vh, kernel, iterations=2)
  thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

  bitxor = cv2.bitwise_xor(img, img_vh)
  bitnot = cv2.bitwise_not(bitxor)
  contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  def sort_contours(cnts, method="left-to-right"):
      reverse = False
      i = 0
      if method == "right-to-left" or method == "bottom-to-top":
          reverse = True
      if method == "top-to-bottom" or method == "bottom-to-top":
          i = 1
      boundingBoxes = [cv2.boundingRect(c) for c in cnts]
      (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                          key=lambda b: b[1][i], reverse=reverse))
      return (cnts, boundingBoxes)
  contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
  heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]

  mean = np.mean(heights)
  box = []
  for c in contours:
      x, y, w, h = cv2.boundingRect(c)
      if (w < 1000 and h < 500):
          image = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 5)
          box.append([x, y, w, h])
  row = []
  column = []
  j = 0
  for i in range(len(box)):
      if (i == 0):
          column.append(box[i])
          previous = box[i]
      else:
          if (box[i][1] <= previous[1] + mean / 2):
              column.append(box[i])
              previous = box[i]
              if (i == len(box) - 1):
                  row.append(column)
          else:
              row.append(column)
              column = []
              previous = box[i]
              column.append(box[i])
  countcol = 0
  for i in range(len(row)):
      x = len(row[i])
      if x > countcol:
          countcol = x
      center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]] #lấy lại tâm của các cột
      center = np.array(center)
      center.sort()
  finalboxes = []
  for i in range(len(row)):
      lis = []
      for k in range(countcol):
          lis.append([])
      for j in range(len(row[i])):
          diff = abs(center - (row[i][j][0] + row[i][j][2] / 4))
          minimum = min(diff)
          indexing = list(diff).index(minimum)
          lis[indexing].append(row[i][j])
      finalboxes.append(lis)
  path = r"Anh_nhan"
  p = pathlib.Path(path)
  p.mkdir(exist_ok=True )

  outer = []
  for i in range(len(finalboxes)):
    if i > 1 and i != 13 and i != 14:
        path2 = path + '/row_' + str(i)
        p = pathlib.Path(path2)
        p.mkdir(exist_ok=True)
        for j in range(len(finalboxes[i])):
            inner = ''
            if (len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                finalboxes[i][j][k][3]
                    # crop_img = img_crop[x + 5  : x + h - 10, y - 5 : y + w + 5 ]
                    crop_img = img[x - 2 : x + h + 10, y : y + w - 10]
                    w , h = crop_img.shape
                    crop_img = cv2.resize(crop_img,(h*2, w*2))
                    crop_img = cv2.copyMakeBorder(crop_img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None, value = [255,255,255])
                    kernel = np.ones((4,4), np.uint8)
                    crop_img = cv2.erode(crop_img, kernel, iterations=1)
                    path3 = path2+'/'+str(j)+".jpg"
                    cv2.imwrite(path3, crop_img)

def plot_image(predictions_array):
  predict_label = np.argmax(predictions_array)
  return ""+arr_name_lable[predict_label-1] +" : "+str(round(100*np.max(predictions_array),2))

def convert_color_befor_train_3(image_ip, i_iterations):
    arr_image_test = []
    image = image_ip.copy()
    # chuyển ảnh về ảnh xám
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # chuyển về ảnh đen trắng
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 199, 1)
    # khung - nốt chuyển đổi ảnh
    kernel = np.ones((3, 3), np.uint8)
    # xóa đừng bao của nét chữ - làm mảnh nét chữ
    image = cv2.dilate(image, kernel, iterations=i_iterations)

    image = ~cv2.resize(image, (28, 28))
    image = image.reshape(1, 28, 28, 1)
    arr_image_test.append(image)
    return arr_image_test

def load_list_file_Anhnhan():
  path_foder = r'Anh_nhan'
  array_path = os.listdir(path_foder)
  for i in range(len(array_path)):
      array_path[i] = path_foder +'/'+ array_path[i]
  return array_path


def load_path_img():
  path_foder = r'img'
  len_path = os.listdir(path_foder)
  return len_path


def array_result(array_image):
    array_result = []
    #  dùng model để nhận diện ảnh đưa vào
    for i in range(len(array_image)):
      # reshape kich thước để phù hợp định dạng ảnh với model
      result = model_CP2.predict(array_image[i])
      array_result.append(result)
    return array_result

def res_num(path , column):
    arr_indexnumber = []
    image = cv2.imread(path + "/" + str(column) + ".jpg")
    print(path + "/" + str(column) + ".jpg")
    im3 = image.copy()

    kernel = np.ones((4, 4), np.uint8)
    im3 = cv2.erode(im3, kernel, iterations=2)

    gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 50:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if h > 50 and h < 120 and w > 40 and w < 90 and h > w:
                roi = im3[y - 10: y + h + 10, x - 10: x + w + 10]
                if roi.shape[0] > 55:
                    kernel = np.ones((4, 4), np.uint8)
                    # roi = cv2.erode(roi, kernel, iterations=2)
                    # xóa đừng bao của nét chữ - làm mảnh nét chữ
                    # roi = cv2.copyMakeBorder(roi, 2, 2 , 2, 2, cv2.BORDER_CONSTANT, None, value=[255, 255, 255])
                    cv2.imwrite("img/" +path.split('_')[2] + "_" + str(column)+ "_"+ str(x) + ".jpg",roi)
    # for cnt in contours:
    #     if cv2.contourArea(cnt) > 50:
    #         [x, y, w, h] = cv2.boundingRect(cnt)
    #         if h > 20 and h < 120 and w < 90 and h > w:
    #             roi = im3[y - 10: y + h + 10, x - 15: x + w + 10]
    #             if roi.shape[0] > 55:
    #                 roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value=[255, 255, 255])
                    arr_indexnumber.append({'index': x, 'number': roi})
    return  arr_indexnumber
'''
hàm ghép hai số lại thành một số 
do lúc cắt bị tách thành hai số riêng không lấy dấu phẩi
'''



def join_num(arr_indexnumber):
    num = []
    def get_my_key(obj):
        return obj['index']
    arr_indexnumber.sort(key=get_my_key)
    for i in arr_indexnumber:
        img = i['number']
        for i in range(5):
            arr_im = convert_color_befor_train_3(img, i)
            rs = plot_image(array_result(arr_im)[0])
            cropname = rs.split(' ')
            if int(cropname[2].split('.')[0]) > 96:
                num.append(rs.split(' ')[0])
                break
            if i == 9:
                num.append(rs.split(' ')[0])
    return ''.join(num)

def call_all_testtest(path):
    for i in load_list_file_Anhnhan():
        shutil.rmtree(i)
    crop_image_lagre(path)
    arr_indexnumber = []
    list_row = load_list_file_Anhnhan()
    for i in list_row:
        index = i.split('_')[2]
        column5 = join_num(res_num(i,5))
        column6 = join_num(res_num(i,6))
        arr_indexnumber.append({'index':int(index),'path':i,'column5':column5,'column6':column6})
    return sorted(arr_indexnumber , key=lambda x : x['index'] , reverse=False)

# image = r"Anh_nhan/row_17/6.jpg"
# img = cv2.imread(image, 1)
# # plotting = plt.imshow(img, cmap='gray')
# # plt.show()
# row = "24"
# columns = "0"
# # thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# im3 = img.copy()
# cv2.imshow('non',im3)
# cv2.waitKey(0)
# W, H, C= im3.shape
# gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (5, 5), 0)
# thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# samples = np.empty((0, 100))
# responses = []
# keys = [i for i in range(48, 58)]
#
# for cnt in contours:
#       if cv2.contourArea(cnt) > 50:
#           [x, y, w, h] = cv2.boundingRect(cnt)
#           print([x,y,w,h])
#           # print('x : ',x ,' y : ', y  ,' w : ', w  ,' h : ', h, ' W : ', W ,' H : ',H)
#           # print('w : ', w  ,' h : ', h)
#           if h > 20 and h < 120 and w < 90 and h > w:
#
#           # if h > 50 and h < 120 and w < 70 and h > w:
#               # roi = im3[y-5:y + h + 5, x-5:x + w +5]
#               roi = im3[y - 10 : y + h + 10, x - 15 : x + w + 10]
#               if roi.shape[0] > 55 :
#                 roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = [255,255,255])
#                 cv2.imshow("none", roi)
#                 cv2.waitKey(0)

# for i in load_list_file_Anhnhan():
#     shutil.rmtree(i)

# for i in load_path_img():
#     os.remove('img/'+i)
#
# call_all_testtest(r'D:\DataThanhHV[ZaloPC_Folder]\1 (1).jpg')