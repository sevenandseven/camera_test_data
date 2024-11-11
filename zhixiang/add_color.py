import cv2
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# 给深度图像添加伪色域
# 读取图像
img = cv2.imread('.\data\data10.png', cv2.IMREAD_GRAYSCALE)  # 假设输入图像为灰度图
print(img)
if img is None:
    print("图像未找到！")
    exit()

# 定义所有22种色板
colormaps = [
    cv2.COLORMAP_AUTUMN, cv2.COLORMAP_BONE, cv2.COLORMAP_JET, cv2.COLORMAP_WINTER,
    cv2.COLORMAP_RAINBOW, cv2.COLORMAP_OCEAN, cv2.COLORMAP_SUMMER, cv2.COLORMAP_SPRING,
    cv2.COLORMAP_COOL, cv2.COLORMAP_HSV, cv2.COLORMAP_PINK, cv2.COLORMAP_HOT,
    cv2.COLORMAP_PARULA, cv2.COLORMAP_MAGMA, cv2.COLORMAP_INFERNO, cv2.COLORMAP_PLASMA,
    cv2.COLORMAP_VIRIDIS, cv2.COLORMAP_CIVIDIS, cv2.COLORMAP_TWILIGHT,
    cv2.COLORMAP_TWILIGHT_SHIFTED, cv2.COLORMAP_TURBO, cv2.COLORMAP_DEEPGREEN
]

# 准备显示图像
fig, axes = plt.subplots(4, 6, figsize=(15, 10))  # 4x6 的子图网格（总共22张图像）

# 遍历所有色板并应用伪彩色
for i, colormap in enumerate(colormaps):
    # 生成伪彩色图像
    pseudo_color_img = cv2.applyColorMap(img, colormap)
    
    # 将 BGR 转换为 RGB（因为 OpenCV 默认是 BGR 而 Matplotlib 是 RGB）
    pseudo_color_img = cv2.cvtColor(pseudo_color_img, cv2.COLOR_BGR2RGB)
    
    # 在子图中显示图像
    ax = axes[i // 6, i % 6]  # 找到对应的子图位置
    ax.imshow(pseudo_color_img)
    ax.set_title(f'Colormap {i+1}')
    ax.axis('off')  # 不显示坐标轴

# 删除多余的空白子图
for j in range(len(colormaps), 24):  # 24 = 4x6
    fig.delaxes(axes[j // 6, j % 6])

# 调整布局并显示   根据测试结果选择色板
plt.tight_layout()
plt.show()
plt.savefig('pseudo_color.png')

def strong_layering(img,layer):
    """
    强分层法
    :param img: 输入灰度图像
    :param layer: 灰度级数分层数
    :return:伪彩色增强图像(ndim=2)
    """
    w,h = img.shape[:2]
    img_color = np.zeros((w,h),dtype=np.uint8)
 
    for row in range(w):
        for col in range(h):
            interval = 256//layer #分层的灰度级数间隔
            I_layer = img[row][col]//interval#像素所在层数(0-layer)
            img_color[row][col] = I_layer*interval
 
    return img_color


def color_enhence(img):
    """
    灰度级彩色变换    伪彩色增强(根据图像灰度值进行伪彩色划分)
    :param img: 输入灰度图像
    :return img_color:伪彩色增强图像(ndim=2)
    """
    w,h = img.shape
    img_color = np.zeros((w,h,3)) # 0:R // 1:G //2::B
 
    for row in range(w):
        for col in range(h):
            I_gray = img[row][col]
            if I_gray>=0 and I_gray<64:  # (0-64)
                img_color[row][col][0]=0
                img_color[row][col][1]=I_gray*4
                img_color[row][col][2]=255
            elif I_gray>=64 and I_gray<128:  # (64-128)
                img_color[row][col][0] = 0
                img_color[row][col][1] = 255
                img_color[row][col][2] = (128-I_gray)*4-1
            elif I_gray>=128 and I_gray<192:  # (64-192)
                img_color[row][col][0] = (I_gray-128)*4
                img_color[row][col][1] = 255
                img_color[row][col][2] = 0
            else:  # (192-255)
                img_color[row][col][0] = 255
                img_color[row][col][1] = (192-I_gray)*4-1
                img_color[row][col][2] = 0
 
    return img_color


#理想滤波器
def filter(img,mode,radius,radius2=None):
    """
    理想滤波器(mask生成器)
    :param img: 输入图像(频率域)
    :param mode: low_pass:低通 / high_pass：高通 / band_pass 带通
    :param radius: 带通内径/高低通半径
    :param radius2: 带通外径
    :return: filter/mask
    """
    w,h = img.shape[:2]
    mid_row = w//2
    mid_col = h//2 #中心点
    filter = np.ones((w,h),dtype=np.uint8)
    if mode=='low_pass':
        for row in range(w):
            for col in range(h):
                distance = (np.sqrt((mid_row-row)**2+(mid_col-col)**2))
                if distance<=radius:
                    filter[row][col] = 1
                else:
                    filter[row][col] = 0
        return filter
    elif mode=='high_pass':
        for row in range(w):
            for col in range(h):
                distance = (np.sqrt((mid_row-row)**2+(mid_col-col)**2))
                if distance<=radius:
                    filter[row][col] = 0
                else:
                    filter[row][col] = 1
        return filter
    elif mode == 'band_pass':
        for row in range(w):
            for col in range(h):
                distance = (np.sqrt((mid_row-row)**2+(mid_col-col)**2))
                if distance>=radius and distance<=radius2:
                    filter[row][col] = 1
                else:
                    filter[row][col] = 0
        return filter ##
 
def frequency_transform(img,radius,radius2):
    """
    频率域变换颜色
    :param img: 输入灰度图像
    :param radius: 滤波器内径(带通滤波器high)
    :param radius2: 滤波器外径(带通滤波器low)
    :return: 伪彩色增强图像(ndim=3)
    """
    img = np.float32(img)
    w,h = img.shape
    img_dft = cv.dft(img,flags=cv.DFT_COMPLEX_OUTPUT)
    img_dft_shift = np.fft.fftshift(img_dft)
    """生成滤波器"""
    filter_low_pass = filter(img,"low_pass",radius=radius)
    filter_band_pass = filter(img,"band_pass",radius=radius,radius2=radius2)
    filter_high_pass = filter(img,"high_pass",radius=radius2)
    """增加滤波器的维度(复制二维升三维)"""
    filter_low_pass = np.expand_dims(filter_low_pass,2).repeat(2,2)
    filter_band_pass = np.expand_dims(filter_band_pass, 2).repeat(2, 2)
    filter_high_pass = np.expand_dims(filter_high_pass, 2).repeat(2, 2)
    """滤波为三个频率分量"""
    img_dft_low = filter_low_pass * img_dft_shift
    img_dft_band = filter_band_pass * img_dft_shift
    img_dft_high = filter_high_pass * img_dft_shift
    """ishift"""
    img_dft_low_ishift = np.fft.ifftshift(img_dft_low)
    img_dft_band_ishift = np.fft.ifftshift(img_dft_band)
    img_dft_high_ishift = np.fft.ifftshift(img_dft_high)
    """idft"""
    img_idft_low = cv.idft(img_dft_low_ishift)
    img_idft_band = cv.idft(img_dft_band_ishift)
    img_idft_high = cv.idft(img_dft_high_ishift)
    """各个频率映射到RGB颜色"""
    img_low = cv.magnitude(img_idft_low[:,:,0],img_idft_low[:,:,1])
    img_band = cv.magnitude(img_idft_band[:,:,0],img_idft_band[:,:,1])
    img_high = cv.magnitude(img_idft_high[:,:,0],img_idft_high[:,:,1])
    img_color = np.zeros((w,h,3),dtype=np.float32)
    img_color[:,:,0]= img_low
    img_color[:,:,1] = img_band
    img_color[:,:,2] = img_high
 
    """灰度直方图均衡化"""
    img_color = cv.convertScaleAbs(img_color)
    img_color_R = cv.equalizeHist(img_color[:,:,0]) #三通道分别直方图均衡化
    img_color_G = cv.equalizeHist(img_color[:,:,1])
    img_color_B = cv.equalizeHist(img_color[:,:,2])
    img_color_equal = cv.merge((img_color_R,img_color_G,img_color_B))
    return img_color_equal

 
# img = cv.imread("test.png")
# img_gary = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
# plt.figure("color_enhance")
# plt.subplot(131);plt.title("gray_to_RGB")
# plt.imshow(color_enhence(img_gary));plt.axis('off');
# plt.subplot(132);plt.title("strong_level")
# plt.imshow(strong_layering(img_gary,8));plt.axis('off');
# plt.subplot(133);plt.title("freaquence_RGB")
# plt.imshow(frequency_transform(img_gary,10,20));plt.axis('off');
# plt.show()
# plt.savefig("three_method.png")



# import cv2
# import os

# # 定义文件夹路径
# input_folder = r'F:\Code\Pythonc64_gray'  # 灰度图像文件夹路径
# output_folder = r'F:\Code\Pythonc64_gray_pseudo_color'  # 伪彩色图像保存路径

# # 如果输出文件夹不存在，则创建
# if not os.path.exists(output_folder):
# 	os.makedirs(output_folder)

# # 遍历文件夹中的所有图片
# for filename in os.listdir(input_folder):
# 	if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.bmp'):  # 支持常见图像格式
# 		# 读取灰度图像
# 		gray_image_path = os.path.join(input_folder, filename)
# 		gray_image = cv2.imread(gray_image_path, cv2.IMREAD_GRAYSCALE)

# 		# 应用伪彩色（热红外风格的铁红颜色）
# 		# colored_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_JET)  # COLORMAP_JET 可以生成铁红效果
# 		# colored_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_AUTUMN)
# 		colored_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_PLASMA)
# 		# colored_image = cv2.applyColorMap(gray_image, cv2.COLORMAP_INFERNO)

# 		# 保存伪彩色图像
# 		output_image_path = os.path.join(output_folder, 'colored_' + filename)
# 		print(filename)
# 		cv2.imwrite(output_image_path, colored_image)

# print("所有灰度图像已转换为伪彩色并保存。")

