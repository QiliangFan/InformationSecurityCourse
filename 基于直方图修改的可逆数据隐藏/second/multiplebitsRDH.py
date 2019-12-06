from PIL import Image
from pylab import *

data = "010111011010111111010101010010000001001010100000101010110110101010111110101111010110"
im = array(Image.open("../img/lenna.bmp"))
sorted_pixel_array = im.flatten()
sorted_pixel_array.sort()
pixel_array = im.flatten()

left_zero_point = sorted_pixel_array[0] - 1
right_zero_point = sorted_pixel_array[-1] + 1
num_of_left_zero_points = left_zero_point - 0 + 1
num_of_right_zero_points = 255 - right_zero_point + 1
# print(sorted_pixel_array[0], sorted_pixel_array[-1])  # print to test the border
print(num_of_left_zero_points, num_of_right_zero_points)  # print to test the number

# search the peak point
num_of_pixel = {}
for i in range(len(sorted_pixel_array)):
    if str(sorted_pixel_array[i]) in num_of_pixel:
        num_of_pixel[str(sorted_pixel_array[i])] += 1
    else:
        num_of_pixel[str(sorted_pixel_array[i])] = 1
random_item = list(num_of_pixel.items())[0]
max_value = int(random_item[0])
max_number = random_item[1]
for key, value in num_of_pixel.items():
    if max_number < value:
        max_value = int(key)
        max_number = value
print("max_value:", max_value)

def left_multiple_bits_RDH():
    """
    使用最左侧连续零点进行数据隐藏, 得到隐藏了数据的图像
    """
    for i in range(len(pixel_array)):
        if left_zero_point + 1 <= pixel_array[i] <= max_value - 1:
            pixel_array[i] -= num_of_left_zero_points

    # 获取每次允许隐藏数据的最大位数N
    i = 0
    N = -1
    while 2 ** i < num_of_left_zero_points:
        i += 1
    N = i-1

    # 进行数据隐藏
    data_cur = 0
    for i in range(len(pixel_array)):
        if pixel_array[i] == max_value:
            sub_data = data[data_cur: (data_cur + N)]
            sub_data_value = int(sub_data, 2)
            # print(sub_data, sub_data_value, pixel_array[i])
            pixel_array[i] -= sub_data_value
            data_cur += len(sub_data)
        if data_cur >= len(data) :
            break

    # 保存了隐藏数据的图片( 事实上, 使用的 位数太多, 图像变化很大了)
    rdh_array = np.reshape(pixel_array, im.shape)
    Image.fromarray(rdh_array).save("lenna_with_data.bmp")


def right_multiple_bits_RDH():
    """
    same as the left's with little difference
    :return:
    """
    pass


def left_multiple_bits_reverse():
    # 获取每次允许隐藏数据的最大位数N
    i = 0
    N = -1

    while 2 ** i < num_of_left_zero_points:
        i += 1
    N = i-1

    result_data = []
    data_cur = 0

    for i in range(len(pixel_array)):
        if max_value - num_of_left_zero_points <= pixel_array[i] < max_value:
            deta = max_value - pixel_array[i]
            temp_str = str(bin(deta)).replace("0b", "")
            if len(data) - data_cur >= N:
                if len(temp_str) < N:  # 不足位数, 高位补零
                    temp_str = "".join(["0"*(N-len(temp_str)), temp_str])
                    result_data.append(temp_str)
                else:
                    result_data.append(temp_str)
                data_cur += N
            else:
                if len(temp_str) < len(data) - data_cur:
                    temp_str = "".join(["0"*(len(data)-data_cur-len(temp_str)), temp_str])
                    result_data.append(temp_str)
                else:
                    result_data.append(temp_str)
                data_cur += len(data) - data_cur
            pixel_array[i] == max_value
        elif pixel_array[i] == max_value:
            temp_str = ""
            if len(data) - data_cur >= N:
                for i in range(N):
                    temp_str += "0"
                result_data.append(temp_str)
                data_cur += N
            else:
                for i in range(len(data) - data_cur ):
                    temp_str += "0"
                result_data.append(temp_str)
                data_cur += len(data) - data_cur
        if data_cur > len(data) - 1:
            break
    # print(result_data)
    result_data = "".join(result_data)
    print(result_data)
    print("数据恢复情况:",len(result_data) == len(data))

    for i in range(len(pixel_array)):
        if 0 <= pixel_array[i] <= max_value - 1 - num_of_left_zero_points:
            pixel_array[i] += num_of_left_zero_points

    reverse_array = np.reshape(pixel_array, im.shape)
    Image.fromarray(reverse_array).save("lenna_reverse.bmp")

def right_multiple_bits_reverse():
    """
    same as the left's with little difference
    :return:
    """
    pass


if num_of_right_zero_points > num_of_right_zero_points:  # 使用左侧连续的零点进行数据隐藏
    left_multiple_bits_RDH()
    left_multiple_bits_reverse()
else:  # 使用右侧的零点进行数据隐藏
    left_multiple_bits_RDH()
    left_multiple_bits_reverse()
