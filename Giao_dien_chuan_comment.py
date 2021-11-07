from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import cv2
import model as md
import catAnh as ca
import CodeColab as CL

_path = []

class Ui_MainWindow(object):
    '''
    mở file ảnh đồng thời hiện ảnh lên lbl ảnh nhận diện tab2 và lấy link path ảnh trong local
    lấy link path để chuyển vào hàm chuyển đồi ảnh gọi từ modul "model.py" tại hàm "train"
    '''
    def openFile(self):
        global _path
        file_filter = 'Folder();;Image files (*.jpg *.gif)'
        path = QFileDialog.getOpenFileName(filter=file_filter)[0]
        pixmap = QPixmap(path)
        self.lblAnhnhandien.setPixmap(pixmap)
        _path = path
    def add_item_to_table(self,row_table,result,valueim,bool):
        item = QtWidgets.QTableWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('img/' + str(valueim)))
        item.setIcon(icon)
        self.tbKetqua.setItem(row_table - 1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText(result)
        if bool == True:
            item.setBackground(QtGui.QColor(255,0,0))
        self.tbKetqua.setItem(row_table - 1, 1, item)
    def train(self):
        global _path
        arr_rs = CL.call_all_testtest(_path)
        # result_max = []
        # int_max = 0
        # ca.crop_image_lagre(_path)
        # ca.crop()
        # array_path_image = os.listdir(r'img')
        row_table = 1
        self.tbKetqua.setRowCount(row_table)
        self.tbKetqua.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ảnh")
        self.tbKetqua.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Documents")
        self.tbKetqua.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Ảnh")
        self.tbKetqua.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Presentation")
        self.tbKetqua.setItem(0, 3, item)
        for i in arr_rs:
            row_table += 1
            self.tbKetqua.setRowCount(row_table)
            item = QtWidgets.QTableWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(i['path']+'/5.jpg'))
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i['column5'])
            self.tbKetqua.setItem(row_table - 1, 1, item)
            item = QtWidgets.QTableWidgetItem()
            pixmap = QtGui.QPixmap(i['path']+'/6.jpg')
            pixmap.scaled(200,900)

            icon = QtGui.QIcon()
            icon.addPixmap(pixmap)
            item.setIcon(icon)
            self.tbKetqua.setItem(row_table - 1, 2, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i['column6'])
            self.tbKetqua.setItem(row_table - 1, 3, item)
        # for valueim in array_path_image:
        #     row_table += 1
        #     self.tbKetqua.setRowCount(row_table)
        #     print('Train image : ', valueim)
        #     img = cv2.imread('img/' + valueim)
        #     for i in range(10):
        #         print(i)
        #         arr_im = md.convert_color_befor_train(img, i)
        #         rs = md.plot_image(md.array_result(arr_im)[0])
        #         cropname = rs.split(' ')
        #         if int(cropname[2].split('.')[0]) > int_max:
        #             result_max = rs
        #             int_max = int(cropname[2].split('.')[0])
        #         if int(cropname[2].split('.')[0]) == 100:
        #             self.add_item_to_table(row_table=row_table,result=rs,valueim=valueim,bool=False)
        #             break
        #         if i == 9:
        #             self.add_item_to_table(row_table=row_table,result=result_max,valueim=valueim,bool=True)


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(878, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget) #tạo tab để chứa các tab con dạy máy, nhận diện, cấu hình
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 871, 551))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        '''label tab khác'''

        self.label = QtWidgets.QLabel(self.tab) #tạo label text danh sách đã chọn.
        self.label.setGeometry(QtCore.QRect(0, 10, 141, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.tab) #label nhãn
        self.label_2.setGeometry(QtCore.QRect(460, 80, 55, 16))
        self.label_2.setObjectName("label_2")

        self.txtNhan = QtWidgets.QLineEdit(self.tab) #tạo text nhập nhãn
        self.txtNhan.setGeometry(QtCore.QRect(530, 80, 131, 22))
        self.txtNhan.setObjectName("txtNhan")

        self.btOpen = QtWidgets.QPushButton(self.tab) #tạo button open
        self.btOpen.setGeometry(QtCore.QRect(460, 170, 93, 28))
        self.btOpen.setObjectName("btOpen")
        # self.btOpen.clicked.connect(self.openFile)

        self.btTrain = QtWidgets.QPushButton(self.tab) #tạo button train
        self.btTrain.setGeometry(QtCore.QRect(620, 170, 93, 28))
        self.btTrain.setObjectName("btTrain")
        # self.btTrain.clicked.connect()

        self.label_3 = QtWidgets.QLabel(self.tab) #tạo label  tiến trình
        self.label_3.setGeometry(QtCore.QRect(560, 290, 61, 16))
        self.label_3.setObjectName("label_3")

        self.proTientrinh = QtWidgets.QProgressBar(self.tab) #tạo progressbar tiến trình
        self.proTientrinh.setGeometry(QtCore.QRect(460, 340, 291, 23))
        self.proTientrinh.setProperty("value", 10)
        self.proTientrinh.setObjectName("proTientrinh")

        self.label_4 = QtWidgets.QLabel(self.tab) #tạo label hiển thị số trang 1/9
        self.label_4.setGeometry(QtCore.QRect(180, 440, 41, 31))
        self.label_4.setObjectName("label_4")

        self.btBack = QtWidgets.QPushButton(self.tab) #tạo button black
        self.btBack.setGeometry(QtCore.QRect(60, 440, 93, 28))
        self.btBack.setObjectName("btBack")

        self.btNext = QtWidgets.QPushButton(self.tab) #button next
        self.btNext.setGeometry(QtCore.QRect(240, 440, 93, 28))
        self.btNext.setObjectName("btNext")

        self.lblAnhnhandien_2 = QtWidgets.QLabel(self.tab) #hãn đưỡng dẫn ảnh
        self.lblAnhnhandien_2.setGeometry(QtCore.QRect(0, 40, 361, 351))
        self.lblAnhnhandien_2.setObjectName("lblAnhnhandien_2")

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
        self.lblAnhnhandien.setGeometry(QtCore.QRect(10, 80, 511, 371))
        self.lblAnhnhandien.setStyleSheet("border: 1px solid rgb(23, 152, 68);")
        self.lblAnhnhandien.setObjectName("lblAnhnhandien")

        self.tbKetqua = QtWidgets.QTableWidget(self.tab_2) #tạo table dữ liệu nhận được
        self.tbKetqua.setGeometry(QtCore.QRect(540, 80, 321, 371))
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


        self.tbKetqua.horizontalHeader().setVisible(False)
        self.tbKetqua.horizontalHeader().setDefaultSectionSize(105)
        self.tbKetqua.horizontalHeader().setHighlightSections(True)
        self.tbKetqua.verticalHeader().setVisible(False)
        self.tbKetqua.verticalHeader().setDefaultSectionSize(28)
        self.tbKetqua.verticalHeader().setHighlightSections(True)

        self.btTrichxuat = QtWidgets.QPushButton(self.tab_2) #button trích xuất
        self.btTrichxuat.setGeometry(QtCore.QRect(70, 470, 93, 28))
        self.btTrichxuat.setObjectName("btTrichxuat")
        self.btTrichxuat.clicked.connect(self.train)

        self.btSave = QtWidgets.QPushButton(self.tab_2) #button save
        self.btSave.setGeometry(QtCore.QRect(320, 470, 93, 28))
        self.btSave.setObjectName("btSave")

        self.btXuatExel = QtWidgets.QPushButton(self.tab_2) #button xuất excel
        self.btXuatExel.setGeometry(QtCore.QRect(630, 470, 93, 28))
        self.btXuatExel.setObjectName("btXuatExel")

        self.label_6 = QtWidgets.QLabel(self.tab_2) #label dữ liệu nhận được
        self.label_6.setGeometry(QtCore.QRect(540, 50, 111, 16))
        self.label_6.setObjectName("label_6")
        #
        self.tabWidget.addTab(self.tab_2, "") #tạo tab nhận diện
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.label_7 = QtWidgets.QLabel(self.tab_3) #label thông tin cần lấy
        self.label_7.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.tab_3) #label tên
        self.label_8.setGeometry(QtCore.QRect(10, 40, 31, 16))
        self.label_8.setObjectName("label_8")

        self.txtName = QtWidgets.QLineEdit(self.tab_3) # text nhập tên
        self.txtName.setGeometry(QtCore.QRect(10, 70, 161, 22))
        self.txtName.setObjectName("txtName")

        self.label_9 = QtWidgets.QLabel(self.tab_3) #label vị trí
        self.label_9.setGeometry(QtCore.QRect(340, 40, 55, 16))
        self.label_9.setObjectName("label_9")

        self.txtIndex = QtWidgets.QLineEdit(self.tab_3) #text nhập vị trí
        self.txtIndex.setGeometry(QtCore.QRect(340, 70, 113, 22))
        self.txtIndex.setObjectName("txtIndex")

        self.label_10 = QtWidgets.QLabel(self.tab_3) # label loại
        self.label_10.setGeometry(QtCore.QRect(590, 40, 55, 16))
        self.label_10.setObjectName("label_10")

        self.cbbLoai = QtWidgets.QComboBox(self.tab_3) #cbb loại
        self.cbbLoai.setGeometry(QtCore.QRect(590, 80, 141, 22))
        self.cbbLoai.setObjectName("cbbLoai")

        self.lbl_Thiet_Lap = QtWidgets.QLabel(self.tab_3) #label bảng thiết lập
        self.lbl_Thiet_Lap.setGeometry(QtCore.QRect(20, 120, 81, 16))
        self.lbl_Thiet_Lap.setObjectName("blbThietLap")
        '''tb thiết lập tab3'''
        # self.tbBangMau = QtWidgets.QTableWidget(self.tab_3) #tb bảng mẫu (hiển thị bảng thiết lập
        # self.tbBangMau.setGeometry(QtCore.QRect(20, 140, 361, 351))
        # self.tbBangMau.setObjectName("tbBangMau")
        # self.tbBangMau.setColumnCount(0)
        # self.tbBangMau.setRowCount(0)

        self.btThietlap = QtWidgets.QPushButton(self.tab_3) #button thiết lập cấu hình
        self.btThietlap.setGeometry(QtCore.QRect(580, 190, 121, 28))
        self.btThietlap.setObjectName("btThietlap")

        self.pushButton_2 = QtWidgets.QPushButton(self.tab_3) #button mới
        self.pushButton_2.setGeometry(QtCore.QRect(580, 280, 121, 28))
        self.pushButton_2.setObjectName("pushButton_2")

        self.btSudung = QtWidgets.QPushButton(self.tab_3) #button sử dụng
        self.btSudung.setGeometry(QtCore.QRect(580, 380, 121, 28))
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
        self.lblDuongdan = QtWidgets.QLabel(self.tab)
        self.lblDuongdan.setGeometry(QtCore.QRect(60, 490, 271, 20))
        self.lblDuongdan.setObjectName("lblDuongdan")
        # label image train
        self.lblAnhnhandien_2.setText(_translate("MainWindow", "TextLabel"))
        self.lblDuongdan.setText(_translate("MainWindow", "Duong_dan_anh"))

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
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
