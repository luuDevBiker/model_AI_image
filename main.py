import os
import model
path_foder = r'..\model_AI\img'
array_path = os.listdir(path_foder)
for i in range(len(array_path)):
    array_path[i] = path_foder +'\\'+ array_path[i]
    print(array_path[i])
array_image = model.result_array_image(array_path)
print(len(array_image))
array_result = model.array_result(array_image)
print(len(array_result))
# print(len(array_result))
# for i in range(len(array_result)):
#     print(array_result[i])
