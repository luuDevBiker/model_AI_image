import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv  # https://vimentor.com/vi/lesson/24-doc-va-ghi-tep-csv-trong-python-bang-mo-dun-csv-pandas

# import value as value
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import pathlib
import shutil
# read your file
'''#1)	đầu tiên ta thực hiện load file lên bằng phương thức cv2.imread()'''
file = r'Anh/mau.jpg'
img = cv2.imread(file, 0)

'''#2)	tiếp theo lấy thông số chiều cao chiều rộng độ sâu ảnh với phương thức img.shape'''
#img.shape # Lệnh img.shape để lấy ra kích thước của mảng này với h, w, d lần lượt là chiều cao, chiều rộng, độ sâu của bước ảnh
#print(img.shape)

# thresholding the image to a binary image
'''#3)	tiếp đến ta chuyển đổi ảnh về hình ảnh nhị phân bằng cv2.threshold()'''
thresh, img_bin = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) #phân ngưỡng
# https://www.phamduytung.com/blog/2020-12-24-thresholding/

# inverting the image
'''4)	đảo ngược ngưỡng để có hình ảnh nền đen font trắng. việc xử lý ảnh trong cv2 ta cần loại ảnh này.'''
img_bin = 255 - img_bin #đảo ngược ảnh ngưỡng

'''5)	Ghi file để lưu trữ hình ảnh vừa được xử lý phục vụ cho các bước tiếp theo'''
cv2.imwrite('/Users/marius/Desktop/cv_inverted.png', img_bin) #ghi ảnh vào file

# Plotting the image to see the output
plotting = plt.imshow(img_bin, cmap='gray') # sử dụng matplotlib.pyplot chuyển đổi ảnh sang ảnh thang độ xám
# https://www.it-swarm-vi.com/vi/python/cach-dat-colormap-mac-dinh-trong-matplotlib/1056902433/
#plt.show() # hiển thị ảnh

'''6)	Kế tiếp ta xác định 1 nhân nhằm phát hiện các hình hộp chữ nhật và tiếp đó là cấu trúc dạng bảng.
 Để làm được điều đó chúng tôi xác định chiều dài nhân trước bằng cách lấy chiều rộng chia lấy nguyên 100. 
 Và chúng tôi gọi nó là kernel_len'''
# countcol(width) of kernel as 100th of total width
kernel_len = np.array(img).shape[1] // 100
#print(kernel_len)
# https://codelearn.io/sharing/tim-hieu-thu-vien-numpy-trong-python

'''7)	Bước lế tiệp chúng tôi định nghĩa nhân dọc để phát hiện tất cả các đường thẳng đứng có trong hình và làm tương tự với nhân ngang.'''
# Defining a vertical kernel to detect all vertical lines of image
ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
# https://www.it-swarm-vi.com/vi/python/xoa-cac-dao-nhieu-nho-gia-trong-mot-hinh-anh-python-opencv/1053566247/
# phát hiệt các nhân dọc của bảng
# Defining a horizontal kernel to detect all horizontal lines of image
hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))

# xác địng các nhân ngang của bảng
'''8)	Sau khi đã định nghĩa được ver_kernel và hor_kernel ta vẽ ra 1 nhân với kích thước  2 x 2'''
# A kernel of 2x2
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)) # lấy ra 1 ô hình chữ nhật với kích thước 2 x 2

'''9)	Sử dụng nhân dọc ver_kernel để phát hiện tất cả các đường dọc sau đó lưu vào file và làm tương tự với nhân ngang hor_kernel.'''
# Use vertical kernel to detect and save the vertical lines in a jpg
image_1 = cv2.erode(img_bin, ver_kernel, iterations=3) #https://www.geeksforgeeks.org/python-opencv-cv2-erode-method/
vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
#https://codelungtung.wordpress.com/2018/04/24/morphological-operations/
# phối hợp Dilate và Erode để lọc nhiễu cho Binary Image.

cv2.imwrite("/Users/marius/Desktop/vertical.jpg", vertical_lines)
# Plot the generated image
plotting = plt.imshow(image_1, cmap='gray')
#plt.show()

# vẽ ra biểu đồ các đường dọc
# Use horizontal kernel to detect and save the horizontal lines in a jpg
image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
cv2.imwrite("/Users/marius/Desktop/horizontal.jpg", horizontal_lines)
# Plot the generated image
plotting = plt.imshow(image_2, cmap='gray')
#plt.show()

'''10)Sau khi có tất cả các đường ngang và đường dọc của bảng ta kết hợp chúng bằng cách lấy chung trọng số 0.5'''
# vẽ ra biểu đồ các đường ngang
# Combine horizontal and vertical lines in a new third image, with both having same weight.
img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0) # trộn 2 hình ảnh  ???
#https://ichi.pro/vi/python-for-art-tron-hai-hinh-anh-bang-opencv-230888807354109

'''11)Sau khi có khung bảng ta xói mòn ảnh nhằm loại bỏ nhiễu giữa khung và nền. 
sau đó tiếp tục thực hiện phân ngưỡng cho ảnh vừa thu được và lưu vào file.'''
# Eroding and thesholding the image
img_vh = cv2.erode(~img_vh, kernel, iterations=2)
thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imwrite("/Users/marius/Desktop/img_vh.jpg", img_vh)
#plt.imshow(img_vh, cmap='gray')
#plt.show()

'''12)	Ta đối sánh cấu trúc bảng vừa tìm được với ảnh gốc để phát hiện đối tượng đã di chuyển giữa 2 
khung hình bằng cv2.bitwise_xor và đảo ngược ngưỡng ảnh nền trắng font đen này bằng cv2.bitwise_not'''
bitxor = cv2.bitwise_xor(img, img_vh)
# các phép toán số học hoạt động theo chiều bit trên ảnh nhị phân
#plt.imshow(bitxor, cmap='gray')
#plt.show()
bitnot = cv2.bitwise_not(bitxor) # trích xuất các phần thiết yếu của hình ảnh   ???
#https://www.geeksforgeeks.org/arithmetic-operations-on-images-using-opencv-set-2-bitwise-operations-on-binary-images/
#https://www.etutorialspoint.com/index.php/323-opencv-logical-operators-bitwise-and-or-nor-xor
# Plotting the generated image
plotting = plt.imshow(bitnot, cmap='gray')
#plt.show()

'''13)	Sau khi có cấu trúc dạng bảng chúng ta phát hiện đường bao bằng hàm findContours. Việc tìm ra đường bao giúp
 chúng ta truy xuất được chính xác tọa độ của mỗi hộp.'''
# Detect contours for following box detection
contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #đưa ra danh sách các contours tìm đk    ???
#https://acodary.wordpress.com/2018/08/26/opencv-contours/

'''#14)	Tiếp theo ta xây dựng 1 hàm nhằm lấy và sắp xếp đường bao từ trên xuống dưới.
#a.	Hàm có 2 đối số truyền vào là cnts danh sách các đường bao muốn sắp xếp và phương pháp mà ta muốn sắp xếp method
b.	Hai giá trị đầu tiên là reverse khẳng định cho thứ tự sắp xếp và giá trị i vị trí của hộ giới hạn mà ta sử dụng sắp xếp.
 việc khởi tạo 2 biến này để sắp xếp theo thứ tự tăng dần cùng với trục X của hộp giới hạn của đường bao.'''
def sort_contours(cnts, method="left-to-right"): #hàm sắp xếp các contours
    # initialize the reverse flag and sort index
    reverse = False #là tham số của sort nhận true là sắp xếp đảo ngược    ???
    #https://viblo.asia/p/cach-su-dung-ham-sorted-va-sort-cua-python-3-naQZR9adKvx
    i = 0

    '''c.	Nếu là sắp xếp từ phải sang trái hoặc từ dưới lên trên thì ta sắp xếp ngược lại'''
    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top": #nếu method bằng 1 trong 2 giá trị thực hiện sắp xếp đảo ngược
        reverse = True

    '''d.Tiệp tục kiểm tra xem chúng ta đnag sắp xếp từ trên xuống dưới hay từ dưới lên trên. Nếu rơi vào 1 trong 2 trường 
    hợp này thì ta phải sắp xếp theo trục y chứ không phải trục x vì bây giờ ta đnag sắp xếp theo chiều dọc chứ không phải chiều ngang.'''
    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    '''e.	Kế tiếp là tính toán các hộp giới hạn của mỗi đường bao. Như vậy với mối đường bao ta sẽ có 1 tập giá trị bao gồm
     tọa độ x,y và chiều rộng chiều cao của đường bao đó (boundingboxes trong bài).'''
    boundingBoxes = [cv2.boundingRect(c) for c in cnts] #Hàm cv2.boundingRect() giúp tìm ra Bounding box hình chữ nhật đứng
    # https://codelungtung.wordpress.com/2018/01/31/simple-contour-properties/
    '''f.	Với các boundingboxes vừa tìm cho phép chúng tôi sắp xếp các đường viền thực tế. sau đó chúng tôi sử dụng zip 
    kết hợp sorted sắp xếp cả đường viền và hộp giới hạn theo các tiêu chí đã đề ra key = lamda, b: b [1] [i] , reverse = reverse.'''
    # tính toán hộp giới hạn của mỗi đường bao
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    #print(cnts)
    #sắp xếp các đường viền thực tế bằng cách sắp xếp hai danh sách với nhau.
    # https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/

    # return the list of sorted contours and bounding boxes
    '''g.	Cuối cùng sau khi sắp xếp xong trả về danh sách đường bao đã sắp xếp và boundingboxes.'''
    return (cnts, boundingBoxes) #trả về mảng và ràng buộc


# Sort all the contours by top to bottom.
'''15)	Sau khi đã có hàm sắp xếp ta sắp xếp danh sách đường bao của mình từ trên xuống'''
contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")

# kể từ đây là vị trí lấy tọa độ các ô
'''Vì boundingboxes vừa có được ở trên gồm 4 phần tử theo thứ tự x,y,w,h nên ta sẽ dùng mảng 2 chiều kết hợp vòng for
 để lấy ra giá trị chiều cao của từng boundingboxes. Cụ thể ta đã dùng boundingboxes [i] [3] với giá trị I ta duyệt qua
  từng phần tử đường bao trong boundingboxes và 3 là vị trí chiều cao ta sẽ lấy ra của boundingboxes[i] đấy. 
  (bước này chúng ta truy xuất chiều cao cho mỗi ô và đưa chúng vào danh sách).'''
# Creating a list of heights for all detected boxes tạo danh sách dộ cao cho các hộp được phát hiện
heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
#print(heights)

'''17)	 Sau đó tính ra độ cao trung bình bằng hàm mean()'''
# Get mean of heights tính giá trị dộ cao trung bình
mean = np.mean(heights)
#print(mean)

'''Chúng ta tạo một mảng để phục vụ cho việc lưu trữ tọa độ chiều rộng chiều cao của các contours'''
# Create list box to store all boxes in
box = []
'''19)	 Kế tiếp ta sử dụng vòng lặp for để lấy các thông số thêm vào mảng và dùng cv2.rectangle để vẽ các hộp lên ảnh.
 Lưu ý ở đây ta quy định chỉ vẽ các hộp có độ rộng dưới 1000 và chiều cao dưới 500.'''

# Get position (x,y), width and height for every contour and show the contour on image
for c in contours:
    x, y, w, h = cv2.boundingRect(c) #lấy ra tọa dộ độ rộng và chiều cao của hộp
    if (w < 1000 and h < 500): #giới hạn độ rộng và chiều cao tối đa cho hộp tránh lấy phải bảng
        image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2) #vẽ ra hộp trên tọa độ kích thước vừa tìm
        # https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
        box.append([x, y, w, h]) #thêm hộp vào mảng

plotting = plt.imshow(image, cmap='gray')
#plt.show()

# phần này tìm xem hộp nằm ở hàng nào cột nào
# Creating two lists to define row and column in which cell is located
row = []
column = []
j = 0
'''ở giai đoạn tiếp theo là giai đoạn xác định hàng và cột. để biết được các ô vừa tìm thấy nằm ở hàng và cột nào. 
Trước hết chúng tôi sử dụng vòng lặp for để duyệt từng phần tử box. Với giá trị đầu tiên nếu i = 0 tức là 
vị trí đầu tiên của mảng box ta thêm nó vào cột và gán biến previous bằng phần tử box đầu tiên. Vói các giá trị i còn
 lại chúng tôi thực hiện như sau: '''
# Sorting the boxes to their respective row and column sắp xếp hàng và cột tương ứng
for i in range(len(box)):
    if (i == 0):
        column.append(box[i])
        previous = box[i]
        #print(previous)
    else:
        '''a.	Nếu phần tử thứ 2 của box tại vị trí i nhỏ hơn giá trị của tọa độ y lấy từ previous cộng với nửa độ cao 
        trung bình thì ta thực hiện thêm box vào cột và gán lại giá trị cho previous đúng bằng box tại vị trí i vừa 
        thêm vào cột.( với việc ta lấy giá trị y của các box sau đó là độ cao thì ta sẽ biết được nó có chung vị trí 
        hàng hay không vì cùng tung độ và độ cao thì nó sẽ nằm trên 1 hàng). Trong trường này nếu i là phần tử cuối cùng
         của box thì ta sẽ chuyển sang hàng mới.'''
        if (box[i][1] <= previous[1] + mean / 2):
            column.append(box[i])
            previous = box[i]
            #print(previous[1])

            if (i == len(box) - 1):
                row.append(column)

        else:
            '''b.	ở trường hợp còn lại ta thêm hàng mới khởi tạo lại mảng cột gán lại giá trị previous và định nghĩa
             ô đầu tiên của hàng điều này nhằm phục vụ cho việc sắp xếp hàng mới.'''
            row.append(column)
            column = []
            previous = box[i]
            column.append(box[i])
            '''c.	Như vậy sau các bước trên kết thúc vòng lặp for chúng tôi đã sắp xếp được các ô box về đúng với hàng
             và cột của chúng.'''

#print(column)
#print(row)

# calculating maximum number of cells tính toán số ô tối đa
'''21)	 Kế đến chúng tôi tính toán số lượng cột tối đa và lấy lại tâm các cột, việc tính toán lại các cột và lấy lại 
tâm nhằm phục vụ cho việc trích xuất dữ liệu. 
a.	Trước hết chúng tôi tính số cột tối đa bằng cách duyệt tất cả các hàng so sánh và lấy ra hàng có nhiều cột nhất.'''
countcol = 0
#print(row[0])
#print(row[1])
for i in range(len(row)):
    x = len(row[i])
    if x > countcol:
        countcol = x
    #print(countcol)
    # Retrieving the center of each column
    #print(row[i])
    #print(len(row))
    center = [int(row[i][j][0] + row[i][j][2] / 2) for j in range(len(row[i])) if row[0]] #lấy lại tâm của các cột
    #center = []
    #print(row[0])
    '''if row[0]:
        for j in range(len(row[i])):
            center = [int(row[i][j][0] + row[i][j][2] / 2)]
            print(row[i][j][0])
            print(row[i][j][2])'''



    center = np.array(center)
    #print(str(i)+' '+str(center))
    #print("++++")
    center.sort()
    #print(center)
print(center)
# Regarding the distance to the columns center, the boxes are arranged in respective order
# khỏang cách đến tâm cột, các cột sắp xếp theo trình tự tương ứng
finalboxes = []
for i in range(len(row)):
    lis = []
    for k in range(countcol):
        lis.append([])
    for j in range(len(row[i])):
        #print(center)
        #print(row[i][j][0])
        #print(row[i][j][2])
        diff = abs(center - (row[i][j][0] + row[i][j][2] / 4)) #hàm abs() trả về giá trị tuyệt đối.
        minimum = min(diff)
        indexing = list(diff).index(minimum) #hàm list(diff) chuyển đổi diff sang dạng list.
        #hàm index() trả về vị trí thấp nhất (vị trí đối tượng minium xuất hiện lần đầu trong list)
        lis[indexing].append(row[i][j])
    finalboxes.append(lis)
    #print(finalboxes)
#print(finalboxes)
# from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
# trích xuất dữ liệu bằng pytesseract và lưu trữ chúng trong danh sách
path = "Anh_nhan"
p = pathlib.Path(path)
p.mkdir(exist_ok=True )

outer = []
for i in range(len(finalboxes)):
    path2 = path + '/row_' + str(i)
    p = pathlib.Path(path2)
    p.mkdir(exist_ok=True)
    print(path2)
    for j in range(len(finalboxes[i])):
        inner = ''
        '''p = pathlib.Path(path2 + '/column_' + str(j))
        p.mkdir(exist_ok=True)
        path3 = path2 + '/column_' + str(j) + '/' '''
        if (len(finalboxes[i][j]) == 0):
            outer.append(' ')
        else:
            for k in range(len(finalboxes[i][j])):
                y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], \
                             finalboxes[i][j][k][3]
                crop_img = img[x:x + h, y:y + w]
                path3 = path2+'/'+str(j)+".jpg"
                cv2.imwrite(path3, crop_img)




