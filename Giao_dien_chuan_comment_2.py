# import PySide2
# import self as self
import this

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import cv2
from tensorflow.python.ops.linalg_ops import self_adjoint_eig

import model as md
import catAnh as ca
import CodeColab2 as CL

_path = ''
list_row = []
class Ui_MainWindow(object):
    '''
    mở file ảnh đồng thời hiện ảnh lên lbl ảnh nhận diện tab2 và lấy link path ảnh trong local
    lấy link path để chuyển vào hàm chuyển đồi ảnh gọi từ modul "model.py" tại hàm "train"
    '''


    def openAnh(self):
        global duongdan
        global fileNames
        # global _path
        # file_filter = 'Folder();'
        # path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        # print("AHHHHHHHHH")
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setViewMode(QFileDialog.List)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            # print(fileNames)
        list_File = os.listdir(fileNames[0])
        # print(list_File)
        anh = list_File[0]
        nhan = fileNames[0]
        textnhan = nhan[len(nhan)-1]
        self.index = 0
        duongdan = str(fileNames[0]) + "/" + str(anh)
        pixmap = QPixmap(duongdan)
        self.lblAnhnhandien_2.setScaledContents(True)
        self.lblAnhnhandien_2.setPixmap(pixmap)
        self.lblDuongdan.setText(duongdan)
        self.label_4.setText(str(self.index + 1) + " / " + str(len(list_File)))
        self.txtNhan.setText("Số "+textnhan)

    def chuyenNext(self):
        list_file = os.listdir(fileNames[0])
        self.index += 1
        tong = len(list_file)
        if(self.index == tong):
            self.index = 0
        anh = list_file[self.index]
        duongdan = str(fileNames[0]) + "/" + str(anh)
        self.lblDuongdan.setText(duongdan)
        self.label_4.setText(str(self.index + 1) + " / " + str(tong))
        pixmap = QPixmap(duongdan)
        self.lblAnhnhandien_2.setScaledContents(True)
        self.lblAnhnhandien_2.setPixmap(pixmap)

    def chuyenBack(self):
        list_file = os.listdir(fileNames[0])
        self.index -= 1
        tong = len(list_file)
        if(self.index == 0):
            self.index = tong - 1
        anh = list_file[self.index]
        duongdan = str(fileNames[0]) + "/" + str(anh)
        self.lblDuongdan.setText(duongdan)
        self.label_4.setText(str(self.index + 1) + " / " + str(tong))
        pixmap = QPixmap(duongdan)
        self.lblAnhnhandien_2.setScaledContents(True)
        self.lblAnhnhandien_2.setPixmap(pixmap)


    def openFile(self):
        global _path
        file_filter = 'Folder();;Image files (*.jpg *.gif)'
        path = QFileDialog.getOpenFileName(filter=file_filter)[0]
        pixmap = QPixmap(path)
        self.lblAnhnhandien.setScaledContents(True)
        self.lblAnhnhandien.setPixmap(pixmap)
        _path = path

    def convert_nparray_to_QPixmap(self, img):
        w, h, ch = img.shape
        # Convert resulting image to pixmap
        if img.ndim == 1:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        qimg = QImage(img.data, h, w, 3 * h, QImage.Format_RGB888)
        qpixmap = QPixmap(qimg)

        return qpixmap
    def Save_image_in_table(self):
        global list_row
        count_row = self.tbKetqua.rowCount()
        for row in range(count_row):


            index_im = 0
            num_rs = self.tbKetqua.item(row,6).text()
            for item in num_rs:
                try:
                    print('vào')
                    index = len(os.listdir('img/'+item))
                    print(1)
                    res = [i['rs_column5']['anh_'+str(index_im)] for i in list_row if i['row'] == row][0]
                    print(1)
                    print(res)
                    cv2.imwrite('img/'+item+'/'+str(index)+'.jpg',res)
                    index_im+=1

                except Exception as e :
                    print('error Save image : ',e)

    def add_rs_to_table(self,row_table,i):
        try:
            self.tbKetqua.setRowCount(row_table)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 0']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 0, item)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 1']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 1, item)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 2']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 2, item)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 3']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 3, item)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 4']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 4, item)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 5']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 5, item)
            try:
                item = QtWidgets.QTableWidgetItem()
                item.setText(''.join(i['rs_column5']['num_rs']))
                self.tbKetqua.setItem(row_table - 1, 6, item)
            except Exception as e:
                print(e)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(self.convert_nparray_to_QPixmap(i['column 6']))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 7, item)
            try:
                item = QtWidgets.QTableWidgetItem()
                item.setText(''.join(i['rs_column6']['num_rs']))
                self.tbKetqua.setItem(row_table - 1, 8, item)
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
            return "NaN"
    def train(self):
        global _path
        global list_row
        print(_path)
        arr_rs = CL.call_all_testtest(_path)
        list_row = arr_rs
        row_table = 1
        self.tbKetqua.setRowCount(row_table)
        self.tbKetqua.setColumnCount(9)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Số Thứ tự")
        self.tbKetqua.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Mã Sinh viên")
        self.tbKetqua.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Họ và Tên")
        self.tbKetqua.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Lớp")
        self.tbKetqua.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ký tên")
        self.tbKetqua.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ảnh Document")
        self.tbKetqua.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Document")
        self.tbKetqua.setItem(0, 6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ảnh Presentation")
        self.tbKetqua.setItem(0, 7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Presentation")
        self.tbKetqua.setItem(0, 8, item)
        try:
            for i in arr_rs:
                row_table += 1
                self.add_rs_to_table(row_table=row_table,i=i)
        except Exception as e:
            print(e)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1878, 1000)
        MainWindow.showMaximized()
        MainWindow.setWindowFlags(MainWindow.windowFlags() | QtCore.Qt.CustomizeWindowHint)
        MainWindow.setWindowFlags(MainWindow.windowFlags() & ~ QtCore.Qt.WindowMaximizeButtonHint)
        # MainWindow.setFixedSize(1878, 1000)
        # MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        # self.layout().setSizeConstraint(QLayout::SetFixedSize)
        # self.setFixedSize(QSize(750, 400))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget) #tạo tab để chứa các tab con dạy máy, nhận diện, cấu hình
        self.tabWidget.setGeometry(QtCore.QRect(50, 0, 1800, 950))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        '''label tab khác'''

        self.label = QtWidgets.QLabel(self.tab) #tạo label text danh sách đã chọn.
        self.label.setGeometry(QtCore.QRect(30, 20, 141, 35))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.tab) #label nhãn
        self.label_2.setGeometry(QtCore.QRect(1100, 80, 55, 35))
        self.label_2.setObjectName("label_2")

        self.txtNhan = QtWidgets.QLineEdit(self.tab) #tạo text nhập nhãn
        self.txtNhan.setGeometry(QtCore.QRect(1180, 80, 300, 30))
        self.txtNhan.setObjectName("txtNhan")

        self.btOpen = QtWidgets.QPushButton(self.tab) #tạo button open
        self.btOpen.setGeometry(QtCore.QRect(1100, 200, 120, 35))
        self.btOpen.setObjectName("btOpen")
        self.btOpen.clicked.connect(self.openAnh)

        self.btTrain = QtWidgets.QPushButton(self.tab) #tạo button train
        self.btTrain.setGeometry(QtCore.QRect(1340, 200, 120, 35))
        self.btTrain.setObjectName("btTrain")
        # self.btTrain.clicked.connect()

        self.label_3 = QtWidgets.QLabel(self.tab) #tạo label  tiến trình
        self.label_3.setGeometry(QtCore.QRect(1260, 310, 61, 35))
        self.label_3.setObjectName("label_3")

        self.proTientrinh = QtWidgets.QProgressBar(self.tab) #tạo progressbar tiến trình
        self.proTientrinh.setGeometry(QtCore.QRect(1100, 360, 400, 35))
        self.proTientrinh.setProperty("value", 5)
        self.proTientrinh.setObjectName("proTientrinh")

        self.label_4 = QtWidgets.QLabel(self.tab) #tạo label hiển thị số trang 1/9
        self.label_4.setGeometry(QtCore.QRect(340, 860, 41, 35))
        self.label_4.setObjectName("label_4")

        self.btBack = QtWidgets.QPushButton(self.tab) #tạo button black
        self.btBack.setGeometry(QtCore.QRect(200, 860, 93, 28))
        self.btBack.setObjectName("btBack")
        self.btBack.clicked.connect(self.chuyenBack)

        self.btNext = QtWidgets.QPushButton(self.tab) #button next
        self.btNext.setGeometry(QtCore.QRect(420, 860, 93, 28))
        self.btNext.setObjectName("btNext")
        self.btNext.clicked.connect(self.chuyenNext)

        self.lblAnhnhandien_2 = QtWidgets.QLabel(self.tab) #hãn đưỡng dẫn ảnh
        self.lblAnhnhandien_2.setGeometry(QtCore.QRect(30, 60, 761, 680))
        self.lblAnhnhandien_2.setStyleSheet("border: 1px solid rgb(23, 152, 68);")
        self.lblAnhnhandien_2.setObjectName("lblAnhnhandien_2")

        self.lblDuongdan = QtWidgets.QLabel(self.tab)
        self.lblDuongdan.setGeometry(QtCore.QRect(30, 760, 350, 20))
        self.lblDuongdan.setObjectName("lblDuongdan")

        self.tabWidget.addTab(self.tab, "") #tạo tab dạy máy
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.btOpenfile = QtWidgets.QPushButton(self.tab_2) #button openfile
        self.btOpenfile.setGeometry(QtCore.QRect(10, 10, 93, 28))
        self.btOpenfile.setObjectName("btOpenfile")
        self.btOpenfile.clicked.connect(self.openFile)

        self.label_5 = QtWidgets.QLabel(self.tab_2) #nhãn ảnh nhận diện
        self.label_5.setGeometry(QtCore.QRect(10, 50, 91, 16))
        self.label_5.setObjectName("label_5")

        self.lblAnhnhandien = QtWidgets.QLabel(self.tab_2) #label cho phép hiển thị ảnh load từ file để nhận diện
        self.lblAnhnhandien.setGeometry(QtCore.QRect(10, 80, 850, 700))
        self.lblAnhnhandien.setStyleSheet("border: 1px solid rgb(23, 152, 68);")
        self.lblAnhnhandien.setObjectName("lblAnhnhandien")

        self.tbKetqua = QtWidgets.QTableWidget(self.tab_2) #tạo table dữ liệu nhận được
        self.tbKetqua.setGeometry(QtCore.QRect(870, 80, 900, 700))
        self.tbKetqua.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tbKetqua.setStyleSheet("text-align: center")
        self.tbKetqua.setAutoScroll(True)
        self.tbKetqua.setTabKeyNavigation(True)
        self.tbKetqua.setProperty("showDropIndicator", True)
        self.tbKetqua.setDragDropOverwriteMode(True)
        self.tbKetqua.setTextElideMode(QtCore.Qt.ElideRight)
        self.tbKetqua.setShowGrid(True)
        self.tbKetqua.setWordWrap(True)
        self.tbKetqua.setCornerButtonEnabled(True)
        self.tbKetqua.setObjectName("tbKetqua")
        self.tbKetqua.setIconSize(QtCore.QSize(200, 50))

        self.tbKetqua.horizontalHeader().setVisible(False)
        self.tbKetqua.horizontalHeader().setDefaultSectionSize(150)
        self.tbKetqua.horizontalHeader().setHighlightSections(True)
        self.tbKetqua.verticalHeader().setVisible(False)
        self.tbKetqua.verticalHeader().setDefaultSectionSize(50)
        self.tbKetqua.verticalHeader().setHighlightSections(True)

        self.btTrichxuat = QtWidgets.QPushButton(self.tab_2) #button trích xuất
        self.btTrichxuat.setGeometry(QtCore.QRect(70, 850, 93, 28))
        self.btTrichxuat.setObjectName("btTrichxuat")
        self.btTrichxuat.clicked.connect(self.train)

        self.btSave = QtWidgets.QPushButton(self.tab_2) #button save
        self.btSave.setGeometry(QtCore.QRect(320, 850, 93, 28))
        self.btSave.setObjectName("btSave")
        self.btSave.clicked.connect(self.Save_image_in_table)

        self.btXuatExel = QtWidgets.QPushButton(self.tab_2) #button xuất excel
        self.btXuatExel.setGeometry(QtCore.QRect(630, 850, 93, 28))
        self.btXuatExel.setObjectName("btXuatExel")

        self.label_6 = QtWidgets.QLabel(self.tab_2) #label dữ liệu nhận được
        self.label_6.setGeometry(QtCore.QRect(870, 50, 111, 16))
        self.label_6.setObjectName("label_6")
        #
        self.tabWidget.addTab(self.tab_2, "") #tạo tab nhận diện
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.label_7 = QtWidgets.QLabel(self.tab_3) #label thông tin cần lấy
        self.label_7.setGeometry(QtCore.QRect(30, 10, 111, 35))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.tab_3) #label tên
        self.label_8.setGeometry(QtCore.QRect(30, 40, 31, 35))
        self.label_8.setObjectName("label_8")

        self.txtName = QtWidgets.QLineEdit(self.tab_3) # text nhập tên
        self.txtName.setGeometry(QtCore.QRect(30, 70, 210, 35))
        self.txtName.setObjectName("txtName")

        self.label_9 = QtWidgets.QLabel(self.tab_3) #label vị trí
        self.label_9.setGeometry(QtCore.QRect(440, 40, 55, 35))
        self.label_9.setObjectName("label_9")

        self.txtIndex = QtWidgets.QLineEdit(self.tab_3) #text nhập vị trí
        self.txtIndex.setGeometry(QtCore.QRect(440, 70, 210, 35))
        self.txtIndex.setObjectName("txtIndex")

        self.label_10 = QtWidgets.QLabel(self.tab_3) # label loại
        self.label_10.setGeometry(QtCore.QRect(1350, 40, 55, 35))
        self.label_10.setObjectName("label_10")

        self.cbbLoai = QtWidgets.QComboBox(self.tab_3) #cbb loại
        self.cbbLoai.setGeometry(QtCore.QRect(1350, 80, 161, 35))
        self.cbbLoai.setObjectName("cbbLoai")

        self.lbl_Thiet_Lap = QtWidgets.QLabel(self.tab_3) #label bảng thiết lập
        self.lbl_Thiet_Lap.setGeometry(QtCore.QRect(30, 120, 140, 35))
        self.lbl_Thiet_Lap.setObjectName("blbThietLap")
        '''tb thiết lập tab3'''

        self.tbBangMau = QtWidgets.QTableWidget(self.tab_3) #tb bảng mẫu (hiển thị bảng thiết lập
        self.tbBangMau.setGeometry(QtCore.QRect(20, 150, 950, 700))
        self.tbBangMau.setObjectName("tbBangMau")
        self.tbBangMau.setColumnCount(0)
        self.tbBangMau.setRowCount(0)

        self.btThietlap = QtWidgets.QPushButton(self.tab_3) #button thiết lập cấu hình
        self.btThietlap.setGeometry(QtCore.QRect(1350, 190, 161, 35))
        self.btThietlap.setObjectName("btThietlap")

        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3) #button mới
        self.pushButton_2.setGeometry(QtCore.QRect(1350, 280, 161, 35))
        self.pushButton_2.setObjectName("pushButton_2")

        self.btSudung = QtWidgets.QPushButton(self.tab_3) #button sử dụng
        self.btSudung.setGeometry(QtCore.QRect(1350, 380, 161, 35))
        self.btSudung.setObjectName("btSudung")

        self.tabWidget.addTab(self.tab_3, "") #tạo tab cấu hình
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nhận diện ảnh"))
        self.label.setText(_translate("MainWindow", "Danh sách ảnh đã chọn: "))
        self.label_2.setText(_translate("MainWindow", "Nhãn: "))
        self.btOpen.setText(_translate("MainWindow", "Open"))
        self.btTrain.setText(_translate("MainWindow", "Train"))
        self.label_3.setText(_translate("MainWindow", "Tiến trình"))
        self.label_4.setText(_translate("MainWindow", "1/9"))
        self.btBack.setText(_translate("MainWindow", "<<"))
        self.btNext.setText(_translate("MainWindow", ">>"))
        # label image train
        self.lblAnhnhandien_2.setText(_translate("MainWindow", "Label hiển thị ảnh dạy"))
        self.lblDuongdan.setText(_translate("MainWindow", ""))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Dạy máy"))
        self.btOpenfile.setText(_translate("MainWindow", "Open File"))
        self.label_5.setText(_translate("MainWindow", "Ảnh nhận diện:"))
        # self.lblAnhnhandien.setText(_translate("MainWindow", "<html><head/><body><p><img src=\"Anh/anh_mau_1.jpg\" widght = \"320\" height = \"360\"/></p></body></html>"))
        __sortingEnabled = self.tbKetqua.isSortingEnabled()


        self.tbKetqua.setSortingEnabled(__sortingEnabled)
        self.btTrichxuat.setText(_translate("MainWindow", "Trích xuất"))
        self.btSave.setText(_translate("MainWindow", "Lưu"))
        self.btXuatExel.setText(_translate("MainWindow", "Xuất Excel"))
        self.label_6.setText(_translate("MainWindow", "Dữ liệu nhận được: "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Nhận diện"))
        self.label_7.setText(_translate("MainWindow", "Thông tin cần lấy: "))
        self.label_8.setText(_translate("MainWindow", "Tên: "))
        self.label_9.setText(_translate("MainWindow", "Vị trí: "))
        self.label_10.setText(_translate("MainWindow", "Loại: "))
        self.lbl_Thiet_Lap.setText(_translate("MainWindow", "Bảng thiết lập: "))
        self.btThietlap.setText(_translate("MainWindow", "Thiết lập cấu hình"))
        self.pushButton_2.setText(_translate("MainWindow", "Mới"))
        self.btSudung.setText(_translate("MainWindow", "Sử dụng cấu hình"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "cấu hình"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # QtWidgets.QMainWindow.resizeEvent(self, event)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
