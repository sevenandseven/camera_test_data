import math

# 通过比例计算误差
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixe_类型2-6.txt", "r") as file:
    lines = file.readlines()
# 初始化一个空列表来存储坐标
coordinates = []

for line in lines:
    x, y, z = map(float, line.strip().split(' '))
    coordinates.append((x, y, z))

# 存储最终的真实值
magnitude = []
# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates:
    sum_of_squares = x**2 + y**2 + z**2
    magnitude.append(math.sqrt(sum_of_squares))

print("magnitude is:", magnitude)

value_to_subtract = 60
x21_subtracted_squared = [abs(x - value_to_subtract) / value_to_subtract for x in magnitude]
sum_21 = sum(x21_subtracted_squared) / len(magnitude)
print("第二组数据6cm时的误差：", sum_21)

coordinates2 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel_类型2-12.txt", "r") as file:
    lines2 = file.readlines()

for line in lines2:
    x, y, z = map(float, line.strip().split(' '))
    #print(x,y,z)
    coordinates2.append((x, y, z))
magnitude2 = []

for x, y, z in coordinates2:
    sum_of_squares2 = x**2 + y**2 + z**2
    magnitude2.append(math.sqrt(sum_of_squares2))
print("magnitude2 is:", magnitude2)
# # 计算误差
value_to_subtract22 = 120
#print("magnitude2 is:", magnitude2)
x22_subtracted_squared = [abs(x - value_to_subtract22) / value_to_subtract22 for x in magnitude2]
sum_22 = sum(x22_subtracted_squared) / len(magnitude2)
print("第二组数据12cm时的误差：", sum_22)


coordinates3 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel_类型1-30.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    x, y, z = map(float, line.strip().split(' '))
    coordinates3.append((x, y, z))

magnitude3 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates3:
    sum_of_squares3 = x**2 + y**2 + z**2
    magnitude3.append(math.sqrt(sum_of_squares3))

print("magnitude3 is  计算的真实值:", magnitude3)
value_to_subtract3 = 300
x11_subtracted_squared = [abs(x - value_to_subtract3) / value_to_subtract3 for x in magnitude3]
sum_11 = sum(x11_subtracted_squared) / len(magnitude3)
print("第一组数据30cm时的误差：", sum_11)


coordinates4 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel_类型1-60.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    x, y, z = map(float, line.strip().split(' '))
    coordinates4.append((x, y, z))

magnitude4 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates4:
    sum_of_squares4 = x**2 + y**2 + z**2
    magnitude4.append(math.sqrt(sum_of_squares4))

print("magnitude4 is  计算的真实值:", magnitude4)
value_to_subtract4 = 600
x12_subtracted_squared = [abs(x - value_to_subtract4) / value_to_subtract4 for x in magnitude4]
sum_12 = sum(x12_subtracted_squared) / len(magnitude4)
print("第一组数据60cm时的误差：", sum_12)

coordinates5 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel 类型3-25.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    x, y, z = map(float, line.strip().split(' '))
    coordinates5.append((x, y, z))

magnitude5 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates5:
    sum_of_squares5 = x**2 + y**2 + z**2
    magnitude5.append(math.sqrt(sum_of_squares5))

print("magnitude5 is  计算的真实值:", magnitude5)
value_to_subtract5 = 250
x31_subtracted_squared = [abs(x - value_to_subtract5) / value_to_subtract5 for x in magnitude5]
sum_31 = sum(x31_subtracted_squared) / len(magnitude5)
print("第三组数据25cm时的误差：", sum_31)

coordinates6 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel_类型3-50.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    x, y, z = map(float, line.strip().split(' '))
    coordinates6.append((x, y, z))

magnitude6 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates6:
    sum_of_squares6 = x**2 + y**2 + z**2
    magnitude6.append(math.sqrt(sum_of_squares6))

print("magnitude6 is  计算的真实值:", magnitude6)
value_to_subtract6 = 500
x32_subtracted_squared = [abs(x - value_to_subtract6) / value_to_subtract6 for x in magnitude6]
sum_32 = sum(x32_subtracted_squared) / len(magnitude6)
print("第三组数据50cm时的误差：", sum_32)

len1 = len(magnitude3) + len(magnitude4)
sum1 = sum(x11_subtracted_squared) + sum(x12_subtracted_squared)
print("第一组数据的平均误差比例:", sum1 / len1)

len2 = len(magnitude) + len(magnitude2)
sum2 = sum(x21_subtracted_squared) + sum(x22_subtracted_squared)
print("第二组数据的平均误差比例:", sum2 / len2)

len3 = len(magnitude5) + len(magnitude6)
sum3 = sum(x32_subtracted_squared) + sum(x31_subtracted_squared)
print("第三组数据的平均误差比例:", sum3 / len3)

len_all = len1 + len2 + len3
sum_all = sum2 + sum1 + sum3
print("三组数据平均误差比例：", sum_all / len_all)