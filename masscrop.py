import os
import cv2
import numpy as np
from pathlib import Path
import shutil

import deskrewUtils as dk

count = [0 for i in range(10)]


def resize_display_img(src, height):
    height = 800
    width = int(height*src.shape[1]/src.shape[0])
    dim = (width, height)
    imgx = cv2.resize(src, dim)
    cv2.imshow('', imgx)
    cv2.waitKey(0)


def deskrew(src):
    image = cv2.imread(src)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    coords = np.column_stack(np.where(thresh > 0))

    angle = cv2.minAreaRect(coords)[-1]
    # print("Angle1:", angle)
    if angle < 45:
        angle = - angle
    else:
        angle = 90 - angle

    # print("Angle2:", angle)
    (h, w) = image.shape[:2]  # 0,1
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    print("[INFO] angle: {:.3f}".format(angle))
    resize_display_img(rotated, 800)

    return rotated


def crop_written_cell(path):
    # print(path)
    list_obj_row = []
    # dk.deskrew(path, 700) #sao làm lệch ảnh thẳng???
    img = cv2.imread(path, 1)

    # cv2.imshow('', img)
    # cv2.waitKey(0)

    img_crop = cv2.imread(path, 0)
    thresh, img_bin = cv2.threshold(img_crop, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin
    kernel_len = np.array(img_crop).shape[1] // 100
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

    contours = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

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

    # print(boundingBoxes)
    # for box in boundingBoxes:
    #     # print(box)
    #     x, y, w, h = box
    #     imgx = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)


    mean = np.mean(heights)
    box = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w < 1000 and h < 500:
            image = cv2.rectangle(img_crop, (x, y), (x + w, y + h), (255, 255, 255), 5)
            box.append([x, y, w, h])
    row = []
    column = []
    j = 0
    for i in range(len(box)):
        if i == 0:
            column.append(box[i])
            previous = box[i]
        else:
            if box[i][1] <= previous[1] + mean / 2:
                column.append(box[i])
                previous = box[i]
                # print(previous[1])

                if i == len(box) - 1:
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
        center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]]  # lấy lại tâm của các cột
        center = np.array(center)
        center.sort()
    # print(center)
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
    outer = []
    row = 1
    for i in range(len(finalboxes)):
        if (i % 2) != 0:
            obj = {'row': row}
            for j in range(len(finalboxes[i])):
                if len(finalboxes[i][j]) == 0:
                    outer.append(' ')
                else:
                    for k in range(len(finalboxes[i][j])):
                        y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                     finalboxes[i][j][k][3]
                        # crop_img = img_crop[x + 5  : x + h - 10, y - 5 : y + w + 5 ]
                        crop_img = img_crop[x: x + h, y: y + w]
                        w, h = crop_img.shape
                        crop_img = cv2.resize(crop_img, (h * 2, w * 2))
                        # cv2.imshow('', crop_img)
                        # cv2.waitKey(0)
                        crop_img = cv2.copyMakeBorder(crop_img, 2, 2, 2, 2, cv2.BORDER_CONSTANT, None,
                                                      value=[255, 255, 255])
                        kernel = np.ones((2, 2), np.uint8)
                        crop_img = cv2.erode(crop_img, kernel, iterations=2)
                        kernel = np.ones((3, 3), np.uint8)
                        crop_img = cv2.dilate(crop_img, kernel, iterations=2)
                        obj['column ' + str(j)] = crop_img
            row += 1
            list_obj_row.append(obj)
    return list_obj_row


def detect_box(image_path, line_min_width=15):
    image = cv2.imread(image_path)
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    th1, img_bin = cv2.threshold(gray_scale, 150, 225, cv2.THRESH_BINARY)
    kernal_h = np.ones((1, line_min_width), np.uint8)
    kernal_v = np.ones((line_min_width, 1), np.uint8)
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal_h)
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN, kernal_v)
    img_bin_final = img_bin_h | img_bin_v
    final_kernel = np.ones((3, 3), np.uint8)
    img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=1)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)
    for x, y, w, h, area in stats[2:]:
        img2 = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('', img2)
    cv2.waitKey(0)
    return stats, labels


def load_all():
    # path_folder = r'DataThanhHV[ZaloPC_Folder]'
    path_folder = r'raw'
    array_path = os.listdir(path_folder)
    # print(len(array_path))
    path = 'cropped'
    # global count

    dirpath = Path('cropped')
    if dirpath.exists() and dirpath.is_dir():
        temp_path = Path('cropped/')
        shutil.rmtree(temp_path)
    else:
        dirpath.mkdir()
    for i in range(len(array_path)):
        array_path[i] = path_folder + '/' + array_path[i]

        # detect_box(array_path[i])

        lst_obj_row = crop_written_cell(array_path[i])
        for j in range(len(lst_obj_row)):
            # crop_img = lst_obj_row[j]
            for k in range(10):
                temp = lst_obj_row[j]['column '+str(k)]
                # cv2.imshow('', temp)
                # cv2.waitKey(0)
                count[k] += 1
                # print('type: ' + str(k))
                # print('count ' + str(k) + ' = ' + str(count[k]))
                # print('path3: ' + path + '/' + str(k) + '/' + str(k) + '-' + str(count[k]) + ".jpg")
                p = Path(path + '/' + str(k))
                p.mkdir(exist_ok=True)
                path3 = path + '/' + str(k) + '/' + str(k) + '-' + str(count[k]) + ".jpg"
                cv2.imwrite(path3, temp)
        print(i)
    # return array_path


# load_all()
# print(len(count))
# print(count)

deskrew('raw/image-005.jpg')
