# -*- coding: utf-8 -*-
import os
#需要引入PIL的Image类，终端分别输入pip3 install pillow和pip install image即可
from PIL import Image
import numpy as np

# 从文件夹取处理图片
def read_document(documet_path):
    img_dir = os.listdir(file_path)
    # print(img_dir)
    # print(len(img_dir))
    for i in range(len(img_dir)):
        #获取初始图片名作为id
        id = img_dir[i].split('.')[0]
        img = Image.open(path_img + '/' + img_dir[i])
        size_img = img.size
        #print(size_img)
        # 准备将图片切割成4张小图片,这里后面的2是开根号以后的数，比如你想分割为9张，将2改为3即可
        weight = int(size_img[0] // 3)
        height = int(size_img[1] // 3)
        window_ratios = []
        pixel_num = []
        shape_win = []
        for j in range(3):
            for k in range(3):
                box = (weight * k, height * j, weight * (k + 1), height * (j + 1))
                non_zero_pixels = np.sum(box)
                region = img.crop(box)
                #输出路径
                region.save('.\image''{}-{}{}.png'.format(id, j, k))
                region_np = np.array(region)
                # 计算非零像素的数量
                non_zero_pixels = np.sum(region_np > 0)
                
                # 计算非零像素所占的百分比
                total_pixels = region_np.size
                ratio_non_zero = (non_zero_pixels / total_pixels)
                window_ratios.append(ratio_non_zero)
                pixel_num.append(non_zero_pixels)
                shape_win.append(total_pixels)

        print(window_ratios)  # 显示每个窗口的比例结果
        rate_all = sum(pixel_num) / sum(shape_win)
        print(rate_all)

def read_file(file_path):
    img = Image.open(path_img + '/' + img_dir[i])
    size_img = img.size
    #print(size_img)
    # 准备将图片切割成4张小图片,这里后面的2是开根号以后的数，比如你想分割为9张，将2改为3即可
    weight = int(size_img[0] // 3)
    height = int(size_img[1] // 3)
    window_ratios = []
    pixel_num = []
    shape_win = []
    for j in range(3):
        for k in range(3):
            box = (weight * k, height * j, weight * (k + 1), height * (j + 1))
            non_zero_pixels = np.sum(box)
            region = img.crop(box)
            #输出路径
            region.save('.\image''{}-{}{}.png'.format(id, j, k))
            region_np = np.array(region)
            # 计算非零像素的数量
            non_zero_pixels = np.sum(region_np > 0)
            
            # 计算非零像素所占的百分比
            total_pixels = region_np.size
            ratio_non_zero = (non_zero_pixels / total_pixels)
            window_ratios.append(ratio_non_zero)
            pixel_num.append(non_zero_pixels)
            shape_win.append(total_pixels)

    print(window_ratios)  # 显示每个窗口的比例结果
    rate_all = sum(pixel_num) / sum(shape_win)
    print(rate_all)





doc_path = r"C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\cacula\src_image"
doc_file(file_path)
