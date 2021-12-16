import cv2
from openpyxl import Workbook
from openpyxl.drawing.image import Image

def create_excel_file(arr_data):
    print('Creating workbook...')
    wb = Workbook()
    ws = wb.active
    ws.title = "Điểm thi"
    header_arr = ["Số Thứ tự", "Mã Sinh viên", "Họ và Tên", "Lớp", "Ký tên", "Ảnh Document", "Document",
                  "Ảnh Presentation", "Presentation"]
    row_code = [code for code in range(ord('a'), ord('i') + 1)]
    # Write header to wb
    print('Writing header')
    for i in range(len(header_arr)):
        # print(chr(row_code[i]))
        # print(header_arr[i])
        ws[chr(row_code[i]) + '1'] = header_arr[i]
    print('Writing data')
    # Write data to wb
    for i in range(len(arr_data)):
        print('i: ' + str(i))
        for j in range(len(header_arr)):
            print('j: ' + str(j))

            cell_name = chr(row_code[i]) + str(j)
            print(cell_name)
            if j != 6 or j != 8:
                cell_img = arr_data[i][j]
                cv2.imshow(cell_name, cell_img)
                cv2.waitKey(0)
            else:
                cell_data = arr_data[i][j]
                print(cell_name + ': ' + cell_data)
            # print()
            # print(chr(row_code[i])+str(j) + ': ' + arr_data[i][j])
        # print(len(arr_data[i]))
        # ws[chr(row_code[i])+str(i)] = arr_data[i]
    print('Workbook created, saving to file...')
    # wb.save(filename='Diemthi.xlsx')
    print('File saved')
