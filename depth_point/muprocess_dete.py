import numpy as np
import cv2
import time
import os
import sys
from multiprocessing import Queue, Process, freeze_support
from DkamSDK import *
from io import BytesIO
import math
import requests
from detect import detect_tea_fun
# 使用两个进程分别去处理
def get_picture(res_queue):
    '''
    采集保存数据
    '''
    # 获取当前相机红外和rgb的宽高
    camera_ret = 0
    camera_num = DiscoverCamera()
    print("camera_num=", camera_num)
    # 相机排序
    if camera_num > 0:
        camera_sort = CameraSort(0)
        print("camera_sort=", camera_sort)
    for i in range(camera_num):
        print("IP:", CameraIP(i))
        if CameraIP(i) == b'192.168.40.78':
            camera_ret = i
    camera_obj1 = CreateCamera(camera_ret)
    # 连接相机
    connect = CameraConnect(camera_obj1)
    print("connect=", connect)
    save_path = ".\data"
    if connect == 0:
        rgb = PhotoInfoCSharp()
        gray = PhotoInfoCSharp()
        point = PhotoInfoCSharp()
        width_gray = new_intArray(0)
        height_gray = new_intArray(0)
        getwidth = GetCameraWidth(camera_obj1, width_gray, 0);  # 获取红外宽
        getheight = GetCameraHeight(camera_obj1, height_gray, 0);  # 获取红外高
        width = intArray_getitem(width_gray, 0)
        height = intArray_getitem(height_gray, 0)
        print("Width=%d, height=%d" % (width, height))

        width_rgb = new_intArray(0)
        height_rgb = new_intArray(0)
        getrgbwidth = GetCameraWidth(camera_obj1, width_rgb, 1);  # 获取rgb宽
        getrgbheight = GetCameraHeight(camera_obj1, height_rgb, 1);  # 获取rgb高
        width_RGB = intArray_getitem(width_rgb, 0)
        height_RGB = intArray_getitem(height_rgb, 0)
        print("Width_rgb=%d, height_rgb=%d" % (width_RGB, height_RGB))

        point_num = width * height * 6
        pointpixel = bytes(point_num)

        gray_num = width * height
        graypixel = bytes(gray_num)

        rgb_num = width_RGB * height_RGB * 3
        rgbpixel = bytes(rgb_num)

        depth = np.zeros((width_RGB*height_RGB), dtype=np.uint16)
        depth = depth.astype(np.int32).astype(np.int16)

        # 软触发模式，连续拍照
        tirggerMode1 = SetTriggerMode(camera_obj1, 0)  # 红外触发
        #print("tirggerMode=", tirggerMode1)

        SetRGBTriggerMode(camera_obj1, 0)  # rgb触发

        # 开启数据流通道
        stream_point = StreamOn(camera_obj1, 1)
        print("stream_point=", stream_point)

        stream_gray = StreamOn(camera_obj1, 0)
        print("stream_gray=", stream_gray)

        stream_RGB = StreamOn(camera_obj1, 2)
        print("stream_RGB=", stream_RGB)
        # 开始接受数据
        acquistion = AcquisitionStart(camera_obj1)
        print("acquistion=", acquistion)

        FlushBuffer(camera_obj1, 0)
        FlushBuffer(camera_obj1, 1)
        FlushBuffer(camera_obj1, 2)
        i = 1
        while True:
            path = os.path.join(save_path, str(i))
            print(path)
            str_name = path.encode('utf-8') 
            pcd_name = str_name + b"_point.pcd"
            gray_name = str_name + b"_gray.bmp"
            rgb_name = str_name + b"_rgb.bmp"
            merge_point = str_name + b"_merge.pcd"
            depth_name = str_name + b"_depth.png"     # 开始执行线程

            # 采集保存点云
            capturePoint = CaptureCSharp(camera_obj1, 1, point, pointpixel, point_num)
            #print("capture_Pointimage: ", capturePoint)
            savepcd = SavePointCloudToPcdCSharp(camera_obj1, point, pointpixel, point_num, pcd_name)
            #print("save pcd=", savepcd)

            # 采集保存RGB
            captureRGB = CaptureCSharp(camera_obj1, 2, rgb, rgbpixel, rgb_num)
            savergb = SaveToBMPCSharp(camera_obj1, rgb, rgbpixel, rgb_num, rgb_name)
            # print("save rgb=", savergb)
            
            # 和rgb大小相同的点云数据（rgb画幅的空间）
            xyz_data = PhotoInfoCSharp()
            xyz_data_num = rgb.pixel_height * rgb.pixel_width * 6
            xyz_data_pixel = np.zeros(xyz_data_num, dtype=np.int8).tobytes()

            ## 点云向RGB对齐
            fushionrgb = Fusion3DToRGBWithOutDistortionCSharp(camera_obj1, rgb, rgbpixel, rgb_num, point,
                                            pointpixel, point_num, xyz_data, xyz_data_pixel, xyz_data_num)
            #print("Fusion3DToRGBCSharp:", fushionrgb)
            # 保存点云数据
            savepcd = SavePointCloudToPcdCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, merge_point)
            xyz_np = np.zeros((width_RGB * height_RGB * 3), dtype=np.float32)
            # 将点云的数据从char类型转换为float数据类型
            Convert3DPointFromCharToFloatCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, xyz_np)
            #print(str(i) + "----融合成功")
            # 保存深度图
            savedepth = SaveDepthToPngCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, depth_name)
            #print("save Depth=", savedepth)

            # 获取点云z平面的数据  其实就是深度图
            status = GetCloudPlaneZCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, depth)
            depthImage = depth.reshape(height_RGB, width_RGB)
            #print("sucessful get picture!!!!!!!!!!!!!!!!")
            RawdataToRgb888CSharp(camera_obj1, rgb, rgbpixel, rgb_num)
            nparr = np.frombuffer(rgbpixel, np.uint8)
            image = nparr.reshape(height_RGB,width_RGB, 3)
            print("图像采集成功" + str(i))
            res_queue.put([image, depthImage, xyz_np, rgbpixel])
            i += 1

          # 关闭流通道
        streamoff_gray = StreamOff(camera_obj1, 0)
        #print("streamoff_gray=", streamoff_gray)

        streamoff_point = StreamOff(camera_obj1, 1)
        #print("streamoff_point=", streamoff_point)

        streamoff_rgb = StreamOff(camera_obj1, 2)
        #print("streamoff_rgb=", streamoff_rgb)
        # 断开相机
        disconnect = CameraDisconnect(camera_obj1)
        #print("disconnect=", disconnect)
        DestroyCamera(camera_obj1)   

def threading_detect_func(res_queue):
    #print("进入检测函数！！！！！！！！！！！！")
    while True:
        if not res_queue.empty():
            print('从队中获取图像')
            image, depthImage, xyz_np, rgbpixel = res_queue.get(timeout=1)
            detect_tea_fun(image, depthImage, xyz_np, rgbpixel)
        else:
            print("队列为空，等待数据...")

if __name__ == "__main__":
    #freeze_support()
    # 注册信号处理函数
    res_queue = Queue()

    pr_det = Process(target=get_picture, args=(res_queue,))       # 线程2是采集
    pr_det.daemon=True
    pr_det.start()   

    pr_cap = Process(target=threading_detect_func, args=(res_queue,))       # 线程1 处理
    pr_cap.daemon=True
    pr_cap.start()  
    while True:
        None