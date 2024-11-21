import math

# 通过比例计算误差
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_point.txt", "r") as file:
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

# coordinates2 = []
# with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\distance_pixel_two.txt", "r") as file:
#     lines2 = file.readlines()

# for line in lines2:
#     x, y, z = map(float, line.strip().split(' '))
#     #print(x,y,z)
#     coordinates2.append((x, y, z))
# magnitude2 = []

# for x, y, z in coordinates2:
#     sum_of_squares2 = x**2 + y**2 + z**2
#     magnitude2.append(math.sqrt(sum_of_squares2))
# #print("magnitude2 is:", magnitude2)

# ratios = [a / b for a, b in zip(magnitude2, magnitude)]
# print(ratios)
# # 计算误差
value_to_subtract = 150
#print("magnitude2 is:", magnitude2)
x_subtracted_squared = [abs(x - value_to_subtract) / value_to_subtract for x in magnitude]
sum_22 = sum(x_subtracted_squared) / len(magnitude)
print("相对误差：", sum_22)

x2_subtracted_squared = [(x - value_to_subtract) for x in magnitude]
sum_of_squares = sum([num ** 2 for num in x2_subtracted_squared])

ave3 = math.sqrt(sum_of_squares / len(magnitude))
print("均方根误差：", ave3)
