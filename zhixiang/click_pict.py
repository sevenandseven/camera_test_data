import cv2

# 定义鼠标回调函数
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 获取点击的图像和另一张图像
        img1, img2 = param
        # 获取两张图像上对应点的RGB值
        b1, g1, r1 = img1[y, x]
        b2, g2, r2 = img2[y, x]
        # 打印RGB值
        print(f"Image 1 RGB at ({x}, {y}): ({r1}, {g1}, {b1})")
        print(f"Image 2 RGB at ({x}, {y}): ({r2}, {g2}, {b2})")

# 加载图像
img1 = cv2.imread(r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\result.jpg', cv2.IMREAD_UNCHANGED)
img2 = cv2.imread(r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\data\1_rgb.bmp', cv2.IMREAD_UNCHANGED)

# 检查图像是否加载成功
if img1 is None or img2 is None:
    print("Error loading images")
    exit()

# 将图像转换为RGB格式
# img1 = cv2.cvtColor(img1, cv2.IMREAD_UNCHANGED)
# img2 = cv2.cvtColor(img2, cv2.IMREAD_UNCHANGED)

# 创建窗口
cv2.namedWindow('Image 1')
cv2.namedWindow('Image 2')

# 设置鼠标回调函数
cv2.setMouseCallback('Image 1', click_event, param=(img1, img2))
cv2.setMouseCallback('Image 2', click_event, param=(img2, img1))

# 显示图像
while True:
    cv2.imshow('Image 1', img1)
    cv2.imshow('Image 2', img2)
    
    # 按下ESC键退出循环
    if cv2.waitKey(20) & 0xFF == 27:
        break

# 关闭所有窗口
cv2.destroyAllWindows()
