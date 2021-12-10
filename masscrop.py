import os
import cv2
import numpy as np

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
        return cnts, boundingBoxes

    contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]

    mean = np.mean(heights)
    box = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w < 1000 and h < 500:
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
    path = r"cropped"
    p = pathlib.Path(path)
    p.mkdir(exist_ok=True)

    outer = []
    count = 0
    for i in range(len(finalboxes)):
        if i > 1 and i != 14 and i != 16:
            p = pathlib.Path(path)
            p.mkdir(exist_ok=True)
            for j in range(len(finalboxes[i])):
                if len(finalboxes[i][j]) == 0:
                    outer.append(' ')
                else:
                    for k in range(len(finalboxes[i][j])):
                        y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                                     finalboxes[i][j][k][3]
                        crop_img = img_crop[x: x + h - 2, y: y + w - 10]
                        w, h = crop_img.shape
                        crop_img = cv2.resize(crop_img, (h * 2, w * 2))
                        crop_img = cv2.copyMakeBorder(crop_img, 30, 30, 30, 30, cv2.BORDER_CONSTANT, None,
                                                      value=[255, 255, 255])
                        kernel = np.ones((4, 4), np.uint8)
                        crop_img = cv2.erode(crop_img, kernel, iterations=1)
                        # crop_img = cv2.dilate(crop_img, kernel, iterations=3)
                        path3 = path + '/' + str(count) + ".jpg"
                        count += 1
                        cv2.imwrite(path3, crop_img)


def load_list_file_Anhnhan():
    path_foder = r'cropped'
    array_path = os.listdir(path_foder)
    for i in range(len(array_path)):
        array_path[i] = path_foder + '/' + array_path[i]
        # print(array_path[i])
    return array_path