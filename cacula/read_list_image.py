import os
import numpy as np
import cv2

path = r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\image2"

window_ratios = []
pixel_num = []
shape_win = []
for img in os.listdir(path):
    image_path = os.path.join(path, img)
    pic = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    spatio = np.sum(pic > 0)
    all_pix = (pic.shape[0] * pic.shape[1])
    pixel_num.append(spatio)
    shape_win.append(all_pix)
    ratios = spatio / all_pix
    window_ratios.append(ratios)

all_pixel = sum(pixel_num) / sum(shape_win)
print("所有像素占比:", all_pixel)
print(window_ratios)

