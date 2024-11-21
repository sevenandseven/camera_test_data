# 假设我们有一个文本文件，其中包含两列图像数据，我们将读取这些数据，计算偶数列和奇数列的差值，并对差值进行平方。
# Y坐标的误差
# 为了演示，我将创建一个示例数据集
import numpy as np

with open(r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\leione.txt", "r") as file:
    lines = file.readlines()

# 提取每一行的第一列数据
first_column_data = [line.split(",")[2].strip() for line in lines]
print(first_column_data)
print(len(first_column_data))

# 分别获得奇数列和偶数列的数值  对应位置数值相减
# 提取偶数位置的数值
# even_index_values = [int(first_column_data[i]) for i in range(0, len(first_column_data), 2)]
# print(even_index_values)
# # 提取奇数位置的数值
# odd_index_values = [int(first_column_data[i]) for i in range(1, len(first_column_data), 2)]
# print(odd_index_values)

# # 计算两个列表中对应位置数值的差
# differences = [even - odd for even, odd in zip(even_index_values, odd_index_values)]

# # 计算两个对应位置数值差的平方
# squared_differences = [diff ** 2 for diff in differences]

# print(squared_differences)

# 第一组数据y坐标的误差
y1 = [1, 36, 16, 36, 4, 36, 0, 196, 100, 64, 16, 1, 9, 4, 4, 36, 4, 25, 1, 9, 0, 25, 9, 16, 1, 0, 1, 9, 16, 81, 49, 36, 9, 1, 4, 1, 0, 16, 1, 16, 16, 1, 9, 9, 4, 36, 0, 1, 4, 1, 1, 1, 4, 1, 1, 9, 9, 4]

# 第二组数据y坐标的误差
y2 = [4, 16, 1, 1, 0, 0, 4, 16, 4, 4, 1, 1, 9, 16, 9, 1, 4, 9, 1, 1, 0, 0, 4, 4, 36, 1, 64, 0, 121, 1, 1, 49, 1, 9, 1, 1, 25, 4, 9, 4, 4, 0, 4, 16, 1, 4, 9, 1, 16, 4, 4, 9, 1, 64, 9, 49, 16, 36, 1, 25, 9]

y3 = [900, 36, 16, 1, 16, 25, 4, 1, 49, 144, 1, 36, 49, 169, 0, 64]