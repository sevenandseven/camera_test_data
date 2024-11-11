
from DkamSDK import *
import numpy as np
import time
import os
import cv2

def Test_all():
    '''
    查询相机
    显示局域网内相机ip
    '''
    # 发现局域网内相机
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
    '''
    连接相机
    '''
    camera_obj1 = CreateCamera(camera_ret)
    # 连接相机
    connect = CameraConnect(camera_obj1)
    print("connect=", connect)
    save_path = ".\data"
    if connect == 0:
        '''
        设置相机
        获取相机宽高
        设置相机模式（连续 触发）
        '''
        # 获取当前相机红外和rgb的宽高
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

        rgb_cloud = np.zeros((width * height * 6), dtype=np.float32)  # 融合数据大小
        image_cloud = np.zeros((width * height * 6), dtype=np.float32)  # 融合数据大小
        gray_cloud = np.zeros((width * height * 6), dtype=np.float32)

        tirggerMode1 = SetTriggerMode(camera_obj1, 1)  # 红外触发
        #print("tirggerMode=", tirggerMode1)

        SetRGBTriggerMode(camera_obj1, 1)  # rgb触发

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
        '''
        设置相机触发帧数
        '''
        para = CameraParameter()
        print(para)
        i = 1
        while True:
            triggerCount = SetTriggerCount(camera_obj1)
            rgbTrigcout=SetRGBTriggerCount(camera_obj1)
            #print("triggerCount:", triggerCount)
            path = os.path.join(save_path, str(i))
            str_name = path.encode('utf-8') 
            pcd_name = str_name + b"_point.pcd"
            gray_name = str_name + b"_gray.bmp"
            rgb_name = str_name + b"_rgb.bmp"
            gray_cloud_name = str_name + b"_gray_cloud.txt"
            rgb_cloud_name = str_name + b"_rgb_cloud.txt"
            merge_point = str_name + b"_merge.pcd"
            depth_name = str_name + b"_depth.png"
            #print(pcd_name, "pcd name is")
            '''
            采集保存数据
            '''
            # 采集保存点云
            capturePoint = CaptureCSharp(camera_obj1, 1, point, pointpixel, point_num)
            #print("capture_Pointimage: ", capturePoint)
            savepcd = SavePointCloudToPcdCSharp(camera_obj1, point, pointpixel, point_num, pcd_name)
            #print("save pcd=", savepcd)

            # 采集保存红外
            capturegray = CaptureCSharp(camera_obj1, 0, gray, graypixel, gray_num)
            #print("capture_Gray: ", capturegray)
            savebmp = SaveToBMPCSharp(camera_obj1, gray, graypixel, gray_num, gray_name)
            print("save gray=", savebmp)

            # 采集保存RGB
            captureRGB = CaptureCSharp(camera_obj1, 2, rgb, rgbpixel, rgb_num)
            #print("capture RGB=", captureRGB)
            savergb = SaveToBMPCSharp(camera_obj1, rgb, rgbpixel, rgb_num, rgb_name)
            print("save rgb=", savergb)
            
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
            Convert3DPointFromCharToFloatCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, xyz_np)
            print("融合成功")
            # savepcd1 = SavePointCloudToPcdCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, filter_name)
            # print("save pcd fushion To RGB=", savepcd1)
            # 是以点云为基准重排rgb
            # FusionImageTo3DCSharp(camera_obj1, rgb, rgbpixel, rgb_num, point,pointpixel, point_num, image_cloud)
            # savergb = SaveToBMPCSharp(camera_obj1, rgb, rgbpixel, rgb_num, merge_rgb_name)
            # print("save rgb=", savergb)
        
            # 点云滤波
            # FilterPointCloudCSharp(camera_obj1, point, pointpixel, point_num, 1)
            # savefilter = SavePointCloudToPcdCSharp(camera_obj1, point, pointpixel, point_num,
            #                                         filter_name)
            # print("save Filter Point=", savefilter)
            # 保存深度图
            savedepth = SaveDepthToPngCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, depth_name)
            print("save Depth=", savedepth)

            '''
            数据融合和保存
            '''

            # 点云和红外融合
            FusionImageTo3DCSharp(camera_obj1, gray, graypixel, gray_num, point, pointpixel,
                                    point_num, gray_cloud)  # 数据融合
            savegray_cloud = SavePointCloudWithImageToTxtCSharp(camera_obj1, point, pointpixel,
                                                                point_num, gray_cloud, gray_cloud_name)
            print("save Gray_cloud=", savegray_cloud)

            # 点云和RGB融合
            FusionImageTo3DCSharp(camera_obj1, rgb, rgbpixel, rgb_num, point, pointpixel,
                                    point_num, rgb_cloud)  # 数据融合
            savergb_cloud = SavePointCloudWithImageToTxtCSharp(camera_obj1, point, pointpixel, point_num,
                                                                rgb_cloud, rgb_cloud_name)
            print("save RGB_cloud=", savergb_cloud)
            # cv2.imshow('gray',savegray_cloud)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            i += 1

        '''
        关闭通道
        断开相机
        '''

        # 关闭流通道
        streamoff_gray = StreamOff(camera_obj1, 0)
        print("streamoff_gray=", streamoff_gray)

        streamoff_point = StreamOff(camera_obj1, 1)
        print("streamoff_point=", streamoff_point)

        streamoff_rgb = StreamOff(camera_obj1, 2)
        print("streamoff_rgb=", streamoff_rgb)
        # 断开相机
        disconnect = CameraDisconnect(camera_obj1)
        print("disconnect=", disconnect)

        DestroyCamera(camera_obj1)
    # 关闭流通道
    streamoff_gray = StreamOff(camera_obj1, 0)
    print("streamoff_gray=", streamoff_gray)

    streamoff_point = StreamOff(camera_obj1, 1)
    print("streamoff_point=", streamoff_point)

    streamoff_rgb = StreamOff(camera_obj1, 2)
    print("streamoff_rgb=", streamoff_rgb)
    # 断开相机
    disconnect = CameraDisconnect(camera_obj1)
    print("disconnect=", disconnect)

    DestroyCamera(camera_obj1)

if __name__ == "__main__":
    Test_all()

