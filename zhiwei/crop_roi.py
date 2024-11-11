from PIL import Image

# 打开一个图像文件
image_path = r'C:\Users\Administrator\Desktop\camera_test_data\data_1\39_rgb.bmp'
image = Image.open(image_path)
image_path2 = r'C:\Users\Administrator\Desktop\camera_test_data\data_1\39_depth.png'
image2 = Image.open(image_path2)

# 设置要裁剪的区域的坐标
# (left, upper, right, lower)
crop_area = (850, 1100, 1000, 1350)
# 裁剪图像
cropped_image = image.crop(crop_area)
cropped_image.show()

cropped_image2 = image2.crop(crop_area)
# 显示裁剪后的图像
cropped_image2.show()

# 保存裁剪后的图像
cropped_image.save(r'C:\Users\Administrator\Desktop\camera_test_data\cropped_rgb2_image.jpg')
# 保存裁剪后的图像
cropped_image.save(r'C:\Users\Administrator\Desktop\camera_test_data\cropped_depth2_image.jpg')
