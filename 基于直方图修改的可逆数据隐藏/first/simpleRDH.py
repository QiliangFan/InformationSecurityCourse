#!/bin/python3
# from utils.de_en_code import encode_to_bin
# from utils.de_en_code import str_to_bytes
from PIL import Image
from pylab import *

data = "0101001101010101101101101010101110"

im = array(Image.open('../img/lenna.bmp'))
sorted_pixel_array = im.flatten()  # get the pixels in the form of 1-D array
pixel_array = im.flatten()

sorted_pixel_array.sort()

num_of_pixel = {}
for i in range(len(sorted_pixel_array)):
    if str(sorted_pixel_array[i]) in num_of_pixel:
        num_of_pixel[str(sorted_pixel_array[i])] += 1
    else:
        num_of_pixel[str(sorted_pixel_array[i])] = 1

random_item = list(num_of_pixel.items())[0]
max_value = random_item[0]
max_number = random_item[1]
min_value = random_item[0]
min_number = random_item[1]
for key,value in num_of_pixel.items():
    if max_number <= value:
        max_value = int(key)
        max_number = value
    if min_number >= value:
        min_value = int(key)
        min_number = value

# 获取零点
if min_value < 255:
    min_value = min_value+1

# print the value for test
print(max_value)
print(min_value)

# 预处理, 将[max_value,min_value-1] 的像素值都+1
for i in range(len(pixel_array)):
    if max_value <= pixel_array[i] <= min_value-1:
        pixel_array[i] += 1

# 顺序扫描, 进行数据隐藏
times = 0
data_cur = 0
for i in range(len(pixel_array)):
    if pixel_array[i] == max_value+1:
        if data[data_cur] == '1':
            pixel_array[i] -= 1
        elif data[data_cur] == '0':
            pass
        data_cur += 1
        times += 1
    if data_cur==len(data)-1:
        break
    if times == max_number:
        print("warning! 可供隐藏数据的位数已经用完!")
        break
print(im.shape)
new_array = np.reshape(pixel_array, im.shape)
with open("lenna_with_data.bmp", "wb") as fp:
    Image.fromarray(new_array).save(fp) # 展示隐藏后的图片

figure()
gray()
contour(im, origin='image')
axis('equal')
axis('off')
figure()

# 顺序扫描, 进行数据提取
# 到这一步应当注意到, 使用像素值最多的那个值, 必须记住是哪个才能用于恢复
# ... 然而使用像素值最多的左边那个值, 可以不必记住=> 但是更不安全
# 同时也当注意到, 必须知道源数据的二进制位数才能有效的终止程序
result_data_cur = 0
result = []
for i in range(len(pixel_array)):
    if pixel_array[i] == max_value:
        result.append("1")
        result_data_cur+=1
    elif pixel_array[i] == max_value+1:
        result.append("0")
        result_data_cur+=1
    if result_data_cur == len(data):
        break
result = "".join(result)
print(result) # get the data

# 图像恢复
for i in range(len(pixel_array)):
    if pixel_array[i] > max_value:
        pixel_array[i] -= 1

new_array = np.reshape(pixel_array, im.shape)
with open("lenna_recover.bmp", "wb") as fp:
    Image.fromarray(new_array).save(fp) # 展示恢复后的图片

figure()
gray()
contour(im, origin='image')
axis('equal')
axis('off')
figure()

hist(pixel_array, 256)
show()
