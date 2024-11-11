import cv2
import numpy as np

# 假设我们有一个RGB图像路径
rgb_image_path = r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\data\data1.jpg'

# 加载RGB图像
rgb_image = cv2.imread(rgb_image_path)

# 假设我们有一些UV坐标，这些坐标是以0到1的比例给出的
# 例如，我们有一个UV坐标表示纹理图像上的一个矩形区域
uv_coords = np.array([[0.1, 0.1], [0.1, 0.9], [0.9, 0.9], [0.9, 0.1]])

# 获取图像的尺寸
height, width, _ = rgb_image.shape

# 将UV坐标转换为图像的像素坐标
pixel_coords = (uv_coords * np.array([width, height])).astype(int)

# 绘制矩形区域，这里我们使用多边形填充功能
# 创建一个空的mask
mask = np.zeros((height, width), dtype=np.uint8)

# 创建一个白色的画布
white_image = np.ones((height, width, 3), dtype=np.uint8) * 255

# 绘制多边形
cv2.fillConvexPoly(mask, pixel_coords, 1)

# 将mask转换为3通道格式
mask3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# 使用mask提取RGB图像的对应区域
region = rgb_image * mask3ch

# 将提取的区域绘制到白色画布上
white_image[mask3ch==1] = region[mask3ch==1]

# 显示结果
cv2.imshow('Region on RGB Image', white_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
