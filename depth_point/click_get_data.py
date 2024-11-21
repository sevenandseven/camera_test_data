import cv2
import numpy as np

# 该款相机是先将点云与rgb图对齐到相同的分辨率情况  点云在转换到rgb坐标系下  应用点云生成深度图
# 现在要从与rgb对齐的depth图恢复到点云上，  需要先使用rgb相机的内参进行相机坐标系下的转换  在使用外参矩阵进行点云恢复

#[(fx, 0, cx), (0, fy, cy), (0, 0, 1)]

fx = 2.172816e+03
cx = 1.343087e+03
fy = 2.172372e+03
cy = 1.047689e+03

# 上一次点击的坐标
last_click = None
click_count = 0

R_rgb = np.array([(9.980746e-01, -4.239562e-03, 6.188033e-02), (4.186324e-03, 9.999908e-01, 9.899716e-04), (-6.188395e-02, -7.290143e-04, 9.980831e-01)])
T_rgb = np.array([-1.162578e+02, 1.719343e-01, -8.648727e+00])

# 加载图片
image_path = input("输入图片路径：")
image = cv2.imread(image_path)
# 创建伪彩色映射
# colored_depth = cv2.applyColorMap((image * 255).astype(np.uint8), cv2.COLORMAP_JET)
# # 显示伪彩色深度图
# cv2.imshow('Image', colored_depth)

depth_image = image_path.replace(".bmp", ".png")
depth_image = depth_image.replace("rgb", "depth")
depth = cv2.imread(depth_image, cv2.IMREAD_UNCHANGED)

# x 是鼠标点击处的列索引（宽度方向），y 是行索引（高度方向）
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 检测到鼠标左键点击
        # 获取点击位置的像素值
        #pixel_value = image[y, x]
        global last_click  # 使用全局变量来保存上一次点击的坐标
        x = int(x)
        y = int(y)
        z = depth[y,x]*0.05                 # cm单位
        if z == 0:  # 如果深度值为0，则忽略此次点击
            return
        print(z)
        # 转换到相机坐标系下
        coox = (x-cx) * z / fx          # 换算到mm
        print(coox)
        cooy = (y-cy) * z / fy
        print(cooy)
        pixel_value = np.array([coox, cooy, z])
        #point = (pixel_value - T_rgb) @ np.linalg.inv(R_rgb)
        point1 = np.linalg.inv(R_rgb) @ (pixel_value - T_rgb)
        print("该点的坐标是1：", point1)
        print(f"点击位置 ({x}, {y}) 的坐标值为: {point1}")

        # d_x = 0
        # d_y = 0
        # d_z = 0
        # sum = 0
        # if coox or cooy or z == 0:
        #     print("点击数据无效：通过查找邻域点计算")
        #     for i in range(x-50,x+50):
        #         for j in range(y-50,y+50):
        #             dis_z = depth[y,x]*0.05
        #             dis_x = (x-cx) * z / fx 
        #             dis_y = (y-cy) * z / fy
        #             print(dis_x, dis_y, dis_z)
        #             if dis_z > 0:
        #                 sum += 1   
        #             d_x += dis_x
        #             d_y += dis_y
        #             d_z += dis_z
        #     if sum != 0:
        #         coox = d_x / sum
        #         cooy = d_y / sum
        #         z = d_z / sum
        #     else:
        #         print("找到的邻域点无效")

        
        # 绘制一个红色的圆点
        cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

        # 在旁边显示坐标
        text = f"({x}, {y})"
        cv2.putText(image, text, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
         # 计算坐标差值
        # 更新点击次数
        global click_count
        click_count += 1
        if click_count % 2 == 0:
            if last_click is not None:
                dx = coox - last_click[0]
                dy = cooy - last_click[1]
                dz = z - last_click[2]
                print(f"与上一点的坐标差值: ({dx}, {dy}, {dz})")
                with open('distance_pixel.txt', 'a') as f:
                    f.write(f"{dx} {dy} {dz}\n")

                with open('test_record.txt', 'a', encoding='utf-8') as f:
                    f.write(f"点击位置 ({x}, {y}) 的坐标值为 {dx} {dy} {dz} \n")
            # 更新上一次点击的坐标
            last_click = point1
        else:
            last_click = point1

# 创建窗口
cv2.namedWindow('Image')
cv2.namedWindow('depth Image')
cv2.resizeWindow('Image', 1296, 972)
cv2.resizeWindow('depth Image', 1296, 972)

# 将鼠标回调函数绑定到窗口
cv2.setMouseCallback('Image', mouse_callback)

# 显示图片
while True:
    cv2.imshow('Image', image)
    cv2.imshow('depth Image', depth)
    
    # 按 'q' 键退出循环
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# 关闭所有窗口
cv2.destroyAllWindows()
