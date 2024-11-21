import cv2
import numpy as np
from PIL import Image
import os

output_folder = '.\image'
if not os.path.exists(output_folder):
        os.makedirs(output_folder)
image_path = r"C:\Users\Administrator\Desktop\collect_date_all\0.png"
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)         # cv2.IMREAD_UNCHANGED
height,width = image.shape
## 重新定义窗口大小，确保它们能够整除图像的尺寸
window_width = width // 5
window_height = height // 2

# 步长等于窗口大小
stride_x = window_width
stride_y = window_height

# 计算需要多少步才能覆盖整个图像
num_steps_x = (width - window_width) // stride_x + 1
num_steps_y = (height - window_height) // stride_y + 1

print("每个方向需要滑动：",num_steps_x, num_steps_y)

# # 确保窗口滑动次数为10次
assert num_steps_x * num_steps_y == 10                 #"The chosen window size and stride do not result in 10 windows."

# 初始化一个列表来记录每个窗口的比例
window_ratios = []
pixel_num = []
shape_win = []
# 滑动窗口并计算每个窗口的比例
for i in range(num_steps_y):
    for j in range(num_steps_x):
        # 确定窗口的起始位置
        x_start = j * stride_x
        y_start = i * stride_y

        # 确保窗口不超出图像边界
        x_end = min(x_start + window_width, width)
        y_end = min(y_start + window_height, height)
        x_start = max(x_start, 0)
        y_start = max(y_start, 0)

        # 提取窗口
        window = image[y_start:y_end, x_start:x_end]
        print(type(window), window.shape)
        # 将窗口转换为PIL图像
        pil_window = Image.fromarray(window)

        # 生成文件名并保存图像
        filename = f"window_{i}_{j}.png"
        pil_window.save(os.path.join(output_folder, filename))

        # # 计算像素值大于0的像素数量
        non_zero_pixels = np.sum(window > 0)

        # 计算比例
        ratio = non_zero_pixels / (window.shape[0] * window.shape[1])
        print(non_zero_pixels, window.shape[0] * window.shape[1])
        window_ratios.append(ratio)
        pixel_num.append(non_zero_pixels)
        shape_win.append(window.shape[0] * window.shape[1])

print(window_ratios)  # 显示每个窗口的比例结果

rate_all = sum(pixel_num) / sum(shape_win)
print(rate_all)