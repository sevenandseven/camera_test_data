import math

with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\leione.txt", "r") as file:
    lines = file.readlines()
# 初始化一个空列表来存储坐标
coordinates = []

for line in lines:
    x, y, z = map(float, line.strip().split(','))
    coordinates.append((x, y, z))

# 存储最终的真实值
magnitude = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates:
    sum_of_squares = x**2 + y**2 + z**2
    #print(sum_of_squares)
    #print(x,y,z)
    magnitude.append(math.sqrt(sum_of_squares))

print("magnitude is:", magnitude)

value_to_subtract = 150
x1_subtracted_squared = [(x - value_to_subtract) for x in magnitude]
sum_of_squares = sum([num ** 2 for num in x1_subtracted_squared])

ave = math.sqrt(sum_of_squares / len(magnitude)) * 0.1
print("第一组数据误差：", ave)

coordinates2 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\leitwo.txt", "r") as file:
    lines2 = file.readlines()

for line in lines2:
    x, y, z = map(float, line.strip().split(','))
    #print(x,y,z)
    coordinates2.append((x, y, z))

magnitude2 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates2:
    sum_of_squares = x**2 + y**2 + z**2
    magnitude2.append(math.sqrt(sum_of_squares))

# # 计算误差
value_to_subtract2 = 60
print("magnitude2 is:", magnitude2)
magnitude2 = [40.02845564173242, 50.86709418522841, 45.95501554937819, 72.29823582267123, 62.3026992098621, 59.392192545693064, 86.48872023710074, 37.92067613279418, 49.10255504587811, 71.2850132639127, 51.89730774314026, 39.62118685374973, 64.1288228799571, 56.58117962312144]
print("num is",len(magnitude2))
x2_subtracted_squared = [(x - value_to_subtract2)*0.1 for x in magnitude2]
sum_of_squares2 = sum([num ** 2 for num in x2_subtracted_squared])

ave2 = math.sqrt(sum_of_squares2 / len(magnitude2))
print("第二组数据误差：", ave2)

coordinates3 = []
with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\leifour.txt", "r") as file:
    lines = file.readlines()

for line in lines:
    x, y, z = map(float, line.strip().split(','))
    coordinates3.append((x, y, z))

magnitude3 = []

# 遍历坐标列表，对每个坐标点进行计算
for x, y, z in coordinates3:
    sum_of_squares3 = x**2 + y**2 + z**2
    magnitude3.append(math.sqrt(sum_of_squares3))

print("magnitude3 is  计算的真实值:", magnitude3)
value_to_subtract3 = 250
x3_subtracted_squared = [(x - value_to_subtract3)*0.1 for x in magnitude3]
sum_of_squares3 = sum([num ** 2 for num in x3_subtracted_squared])

ave3 = math.sqrt(sum_of_squares3 / len(magnitude3))
print("第三组数据误差：", ave3)

ave_all = (ave + ave2 + ave3) / 3

print("总的误差：", ave_all)


d = math.sqrt(11915.543846401346)
print(d)

