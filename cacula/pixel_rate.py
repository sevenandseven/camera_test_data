import cv2
import numpy as np

depth_image = r"C:\Users\Administrator\Desktop\collect_date_all\0.png"
depth = cv2.imread(depth_image, cv2.IMREAD_UNCHANGED)

sum = 0
for v in range(0,depth.shape[0]):
    for u in range(depth.shape[1]):
        z = depth[v,u]*0.05                 # cm单位
        if z > 0:
            sum += 1

rate = sum / (depth.shape[0] * depth.shape[1])
print(depth.shape[0], depth.shape[1])
print(rate)