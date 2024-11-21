from PIL import Image

# 打开彩色图像和深度图
color_image_path = r'C:\Users\Administrator\Desktop\camera_test_data\data_1\39_rgb.bmp'
depth_image_path = r'C:\Users\Administrator\Desktop\camera_test_data\data_1\39_depth.png'
color_image = Image.open(color_image_path)
depth_image = Image.open(depth_image_path)

# 确保两个图像的尺寸相同
if color_image.size != depth_image.size:
    raise ValueError("彩色图像和深度图的尺寸必须相同")

# 将深度图转换为RGB模式，以便我们可以叠加彩色图像
depth_image = depth_image.convert('RGB')

# 使用Image.blend()方法将彩色图像和深度图叠加
# alpha参数控制叠加的强度，这里设置为0.5表示两个图像各占一半
alpha = 0.7
overlay_image = Image.blend(color_image, depth_image, alpha)          # # blend_img = img1 * (1 – 0.3) + img2* alpha

# 显示结果
overlay_image.show()

# 保存叠加后的图像
overlay_image.save('.\overlayed_image.jpg')
