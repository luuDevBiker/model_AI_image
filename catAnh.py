import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2 as cv
import cv2
import numpy as np
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
try:
    from PIL import Image
except ImportError:
    import Image
import pathlib
import shutil

def crop_image_lagre(link):
  print(link)
  img = cv2.imread(link, 0)
  img_crop = img.copy()
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
      if i > 1 and i != 14 and i != 16:
        path2 = path + '/row_' + str(i)
        p = pathlib.Path(path2)
        p.mkdir(exist_ok=True)
        for j in range(len(finalboxes[i])):
            if (len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                finalboxes[i][j][k][3]
                    crop_img = img_crop[x  : x + h - 2, y  : y + w - 10 ]
                    w , h = crop_img.shape
                    crop_img = cv2.resize(crop_img,(h*2, w*2))
                    crop_img = cv2.copyMakeBorder(crop_img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None, value = [255,255,255])
                    kernel = np.ones((4,4), np.uint8)
                    crop_img = cv2.erode(crop_img, kernel, iterations=1)
                    # crop_img = cv2.dilate(crop_img, kernel, iterations=3)
                    path3 = path2+'/'+str(j)+".jpg"
                    cv2.imwrite(path3, crop_img)

def Crop_number(image , row , columns):
  im3 = image.copy()
  W, H, C = image.shape
  gray = cv2.cvtColor(im3, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5, 5), 0)
  thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  samples = np.empty((0, 100))
  responses = []
  keys = [i for i in range(48, 58)]

  for cnt in contours:
      if cv2.contourArea(cnt) > 50:
          [x, y, w, h] = cv2.boundingRect(cnt)
          # print('x : ',x ,' y : ', y  ,' w : ', w  ,' h : ', h, ' W : ', W ,' H : ',H)
          # print('w : ', w  ,' h : ', h)
          if h > 50 and h < 120 and w < 70 and h > w:
          # if h > 55 and h < 120 and w < 100 and h > w:
              # roi = im3[y-5:y + h + 5, x-5:x + w +5]
              roi = im3[y - 10 : y + h + 10, x - 15 : x + w + 10]
              if roi.shape[0] > 55 :
                roismall = cv2.resize(roi, (W * 2, H * 2))
                kernel = np.ones((4,4), np.uint8)
                roismall = np.array(255 * (roismall / 255) ** 1, dtype='uint8')
                # xóa đừng bao của nét chữ - làm mảnh nét chữ
                roismall = cv2.erode(roismall, kernel, iterations=5)
                roismall = cv2.dilate(roismall, kernel, iterations=1)
                roi = cv2.copyMakeBorder(roi, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, value = [255,255,255])
                arr = os.listdir('img')
                index = len(arr)
                cv2.imwrite("img/"+row+'_'+columns+'_'+str(x)+".jpg",roi)
                print('crop number : ' , "img/"+row+'_'+columns+'_'+str(x)+".jpg")

def load_list_file_Anhnhan():
  path_foder = r'Anh_nhan'
  array_path = os.listdir(path_foder)
  for i in range(len(array_path)):
      array_path[i] = path_foder +'/'+ array_path[i]
      # print(array_path[i])
  return array_path

def load_path_img():
  path_foder = r'img'
  len_path = os.listdir(path_foder)
  return len_path

def crop():
  array_path = load_list_file_Anhnhan()
  path_foder = r'img'
  len_path = os.listdir(path_foder)
  for i in len_path:
    print('img/'+i)
    os.remove('img/'+i)
  for i in array_path:
      print(i)
      try:
        index_row = i.split('_')[2]
        print(index_row)
        print(i)
        img = cv2.imread(i+"/5.jpg")
        Crop_number(img,index_row , '5')
        img = cv2.imread(i+"/6.jpg")
        Crop_number(img,index_row , '6')
        print('crop : ' ,i)
      except :
        print('error : crop()')








