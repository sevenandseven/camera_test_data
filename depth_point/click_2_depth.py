import cv2
import numpy as np

#[(fx, 0, cx), (0, fy, cy), (0, 0, 1)]
#[(1.432607e+03, 0, 6.480221e+02), (0, 1.432464e+03, 5.235400e+02), (0, 0, 1)]
# 鼠标回调函数

# rgb相机内参 [(1.343087e+03 0 1.343087e+03) (0 2.172372e+03 1.047689e+03) (0 0 1)]
# 外参  [9.980746e-01 6.188033e-02 4.186324e-03 9.999908e-01 9.899716e-04 -6.188395e-02 9.980831e-01]
# # t [9.980831e-01 1.719343e-01 -8.648727e+00]
# fx = 1.432607e+03 
# cx = 6.480221e+02
# fy = 1.432464e+03
# cy = 5.235400e+02

# cfx = 1.343087e+03
# ccx = 1.343087e+03
# cfy = 2.172372e+03
# ccy = 1.047689e+03

# 深度相机
fx = 1.432607e+03 * 2592 / 1244
fy = 1.432464e+03 * 1944 / 1024
cx = 6.480221e+02 * 2592 / 1244
cy = 5.235400e+02 * 1944 / 1024
# 上一次点击的坐标
last_click = None
click_count = 0

# 加载图片
image_path = input("输入图片路径：")
depth = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

# x 是鼠标点击处的列索引（宽度方向），y 是行索引（高度方向）    （u,v）坐标值
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # 检测到鼠标左键点击
        # 获取点击位置的像素值
        #pixel_value = image[y, x]
        global last_click  # 使用全局变量来保存上一次点击的坐标
        x = int(x)
        y = int(y)
        z = depth[y,x]*0.05                 # mm单位
        print(z)
        # 转换到相机坐标系下
        
        # X = depth * (u - cx) / fx
        # Y = depth * (v - cy) / fy
        coox = (x-cx) * z / fx          # 换算到mm   宽
        print(coox)
        cooy = (y-cy) * z / fy           # 高
        print(cooy)

        d_x = 0
        d_y = 0
        d_z = 0
        sum = 0
        if coox or cooy or z == 0:
            print("点击数据无效：通过查找邻域点计算")
            for i in range(x-4,x+4):
                for j in range(y-4,y+4):
                    dis_z = depth[y,x]*0.05
                    dis_x = (x-cx) * z / fx 
                    dis_y = (y-cy) * z / fy
                    print(dis_x, dis_y, dis_z)
                    if dis_z > 0:
                        sum += 1   
                    d_x += dis_x
                    d_y += dis_y
                    d_z += dis_z
            if sum != 0:
                coox = d_x / sum
                cooy = d_y / sum
                z = d_z / sum
            else:
                print("找到的邻域点无效")

        pixel_value = [coox, cooy, z]
        print(f"点击位置 ({x}, {y}) 的坐标值为: {pixel_value}")
        
        # 绘制一个红色的圆点
        cv2.circle(depth, (x, y), 3, (255, 255, 255), -1)

        # 在旁边显示坐标
        text = f"({x}, {y})"
        cv2.putText(depth, text, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
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
                    f.write(f"{dx} {dy} \n")

            # 更新上一次点击的坐标
            last_click = pixel_value
        else:
            last_click = pixel_value

cv2.namedWindow('depth Image')

# 将鼠标回调函数绑定到窗口
cv2.setMouseCallback('depth Image', mouse_callback)

# 显示图片
while True:
    cv2.imshow('depth Image', depth)
    
    # 按 'q' 键退出循环
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# 关闭所有窗口
cv2.destroyAllWindows()
