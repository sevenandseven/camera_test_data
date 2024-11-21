# import csv
# with open("guaqi_z.txt", 'r') as f:
#     reader = csv.reader(f)
#     # 遍历每一行
#     for row in reader:
#         # 假设Z坐标在最后一列
#         data = row[-1].replace('z=','')
#         #print(data, type(data))
#         z_coordinate = float(data)
#         print(z_coordinate)


# with open("test.txt", 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         data = float(row[-1]) - 10
#         z_coordinate = float(data)
#         print(z_coordinate)


import csv
sum = 0
i = 0
with open("test.txt", 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        data = float(row[-1])
        z_coordinate = abs(data)
        print(z_coordinate)
        i += 1
        sum += z_coordinate
    average = sum/i
print(average)