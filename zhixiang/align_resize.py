import cv2
import numpy as np
from openni import openni2

def u16_to_u8(depth_image):
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(depth_image)
    print("picture", min_val, max_val, min_loc, max_loc)
    alpha = 255 / (max_val - min_val)
    beta = -min_val
    result = ((depth_image + beta) * alpha).astype(np.uint8)
    
    return result

save_path = r"C:\Users\Administrator\Desktop\camera_test_data\zhixiang\\"
dframe_data = cv2.imread(r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\data1.png', cv2.IMREAD_UNCHANGED)
frame = cv2.imread(r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\data1.jpg', cv2.IMREAD_UNCHANGED)#
depth_image = cv2.imread(r'C:\Users\Administrator\Desktop\camera_test_data\zhixiang\data1.png', 0)
#frame = cv2.resize(frame, (960, 600), interpolation=cv2.INTER_AREA)
# depth_image = cv2.imread(r"test.png", cv2.IMREAD_ANYDEPTH)
# depth_image = u16_to_u8(dframe_data)
# depth_image = 255 - depth_image
#cv2.imwrite('depth_image', depth_image)
#dframe_data = cv2.resize(dframe_data, (1920, 1080), interpolation=cv2.INTER_AREA)

# rgb相机的内参矩阵(旋转矩阵 平移矩阵)
fx = 432.4203796386719 * 1920 / 960
fy = 432.4203796386719 * 1080 / 600
cx = 936.9318237304688 * 1920 / 960
cy = 328.924560546875 * 1080 / 600
#      相机坐标系到图像坐标系    [[fx, s, x0] [0 fy y0] [0 0 1]]
RK_rgb = np.array([(fx, 0, cx), (0, fy, cy), (0, 0, 1)])

dfx = 970.2671508789062
dfy = 970.2671508789062
dcx = 477.4331970214844
dcy = 210.4376983642578
# 深度相机的内参矩阵

RK_dep = np.array([(dfx, 0, dcx), (0, dfy, dcy), (0, 0, 1)])
#TK_dep = np.array([-0.0148581, -8.0544e-05, 2.60393e-05])
 
# rgb相机的外参矩阵(旋转矩阵 平移矩阵)     世界坐标系到相机坐标系
R_rgb = np.array([(9.9965566e-01, -3.0814363e-03, -2.6058486e-02), (9.0469641e-04,9.9653786e-01, -8.3135419e-02), ( 2.6224444e-02,  8.3083212e-02,9.9619752e-01)])
T_rgb = np.array([-195.59442 ,  -35.571407, -297.95428])
 
# 深度相机的外参矩阵
R_dep = np.array([(9.9965566e-01, -3.0814363e-03, -2.6058486e-02), (9.0469641e-04,9.9653786e-01, -8.3135419e-02), ( 2.6224444e-02,  8.3083212e-02,9.9619752e-01)])
T_dep = np.array([-195.59442 ,  -35.571407, -297.95428])
 
Rir_rgb = R_rgb @ np.linalg.inv(R_dep)            # 两个相机坐标系之间的变换矩阵       
Tir_rgb = T_rgb-R_rgb@np.linalg.inv(R_dep)@T_dep 
R = RK_rgb@Rir_rgb@np.linalg.inv(RK_dep)                   # 像素点之间的变换关系矩阵
T = RK_rgb@Tir_rgb
 
result = np.ones((dframe_data.shape[0], dframe_data.shape[1], 3), dtype=np.uint8)*255
# print(result.shape)
for row in range(dframe_data.shape[0]):       # 600
    for col in range(dframe_data.shape[1]):    # 960
        depth_value = dframe_data[row, col]           # 获取深度值  [行列--高宽]
        #print(depth_value)
        if depth_value != 0 and depth_value != 65535:
            # 投影到彩色坐标系上的坐标
            uv_depth = np.array([col, row, 1])      # 齐次坐标
            uv_color = depth_value * np.dot(R, uv_depth) + T                      # Z_rgb*p_rgb=R*Z_ir*p_ir+T;; (除以1000，是为了从毫米变米)   深度坐标系下的其次标点加上旋转平移获得rgb坐标系下的点
            #print("uv_color is:", uv_color, '\n', uv_color.shape)                # 三数据元组
            #print(uv_color[0],'  ', uv_color[1], '  ',uv_color[2])
            X = int(uv_color[0] / uv_color[2])                                   # 高 宽   z
            Y = int(uv_color[1] / uv_color[2])                                   # # // Z_rgb*p_rgb -> p_rgb 
            # 除以齐次坐标的最后一个元素获得像素值   
            if 0 <= X < frame.shape[1] and 0 <= Y < frame.shape[0]:    # x < 1920  y < 1080
                result[row, col] = frame[Y,X]             # rgb值
                #print(frame[Y,X], '\n', result[row, col], "frame yx************************* result row col")
            else:
                result[row, col] = [0, 0, 0]

cv2.imshow('Region on RGB Image', result)
cv2.resizeWindow("Region on RGB Image", 960, 540)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite(save_path+'result.jpg', result)
#cv2.imwrite(save_path+'\src_depth.png', dpt)
#cv2.imwrite(save_path+'\color_depth.png', depth_colormap)
cv2.imwrite(save_path+'\rgb.png', frame)   