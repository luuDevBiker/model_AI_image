from openpyxl import Workbook


def create_excel_file(arr_rs):
    wb = Workbook()
    ws = wb.active
    ws.title = "Điểm thi"
    header_arr = ["Số Thứ tự", "Mã Sinh viên", "Họ và Tên", "Lớp", "Ký tên", "Ảnh Document", "Document",
                  "Ảnh Presentation", "Presentation"]
    row_code = [code for code in range(ord('a'), ord('i') + 1)]
    for i in range(len(header_arr)):
        # print(chr(row_code[i]))
        # print(header_arr[i])
        ws[chr(row_code[i]) + '1'] = header_arr[i]
    for i in range(len(arr_rs)):
        print(arr_rs[i])
        print(len(arr_rs[i]))
        ws[chr(row_code[i])+str(i)] = arr_rs[i]
    wb.save(filename='Diemthi.xlsx')



