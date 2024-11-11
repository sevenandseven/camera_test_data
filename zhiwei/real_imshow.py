
from DkamSDK import *
import numpy as np
import time
import os
import cv2
from io import BytesIO
import math
import requests

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

        depth = np.zeros((width_RGB*height_RGB), dtype=np.uint16)
        depth = depth.astype(np.int32).astype(np.int16)

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
            print(str(i) + "----融合成功")
            # 保存深度图
            savedepth = SaveDepthToPngCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, depth_name)
            print("save Depth=", savedepth)

            # 获取点云z平面的数据  其实就是深度图
            status = GetCloudPlaneZCSharp(camera_obj1, xyz_data, xyz_data_pixel, xyz_data_num, depth)
            depthImage = depth.reshape(height_RGB, width_RGB)
            print(len(rgbpixel))
            get_api = requests.post("http://192.168.10.132:10021/api/stream_xy", files={'image':('test.jpg', rgbpixel)})
            print(get_api)
            if get_api.status_code == 500:
                d_x = 0
                d_y = 0
                d_z = 0
                tem_z = 0
                x = 0
                y = 0
            else:  
                inf_re =  get_api.json()
                for cls in inf_re["result"]:
                    if cls["cls_name"] == "tea can":
                        x = int(cls["center_x"])
                        y = int(cls["center_y"]) 
                        print(x,y)
            #print(rgbpixel)
            #image_stream = BytesIO(pointpixel)           # 将bytes对象包装成一个文件对象
            # 使用OpenCV的imdecode函数从文件对象中读取图像  第二个参数cv2.IMREAD_UNCHANGED表示读取图像包括alpha通道（如果有的话）
            #RawdataToRgb888CSharp(camera_obj, raw_data_info, xyz, pixel_size)
            RawdataToRgb888CSharp(camera_obj1, rgb, rgbpixel, rgb_num)
            nparr = np.frombuffer(rgbpixel, np.uint8)
            image = nparr.reshape(height_RGB,width_RGB, 3)
            # depthImage = depthImage.copy()
            image = image.copy()
            sum = 0
            d_x = 0
            d_y = 0
            tem_z = 0
            d_z = 0
            po_sum = 0
            for i in range(x-2,x+2):
                for j in range(y-2,y+2):
                    dis_z = depthImage[j,i]*0.05
                    dis_x = xyz_np[3*(j*rgb.pixel_width+i)+0]          # 换算到cm
                    dis_y = xyz_np[3*(j*rgb.pixel_width+i)+1]
                    tem_a = xyz_np[3*(j*rgb.pixel_width+i)+2]
                    print(dis_z, tem_a)
                    if dis_z > 0:
                        sum += 1   
                    d_x += dis_x
                    d_y += dis_y
                    d_z += dis_z
                    tem_z += tem_a
            print("有效点个数：", sum)
            if sum != 0:
                d_x = d_x / sum
                d_y = d_y / sum
                d_z = d_z / sum
                tem_z = tem_z / sum
            else:
                d_x = 0
                d_y = 0
                d_z = 0
                tem_z = 0
            #cv2.rectangle(image, (300,500), (500, 700), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2
            font_color = (255, 255, 255)
            thickness = 3
            print(tem_z)
            if d_x and d_y and d_z is not None:
                text = f'({d_x:.4f}, {d_y:.4f}, {d_z:.4f}, {tem_z:.4f})'
            else:
                text = f'({d_x}, {d_y}, {d_z:.4f}, {tem_z:.4f})'
            text_position = (x - 100, y-50)
            # img_bgr = cv2.putText(depthImage, text, text_position, font, font_scale, 65524, thickness)
            # cv2.circle(depthImage, (x,y), 20, 65536)
            img_bgr = cv2.putText(image, text, text_position, font, font_scale, 65524, thickness)
            cv2.circle(image, (x,y), 20, 65536)
            #image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # 同一个窗口显示需要转换成相同通道的图像
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # combined_image = np.hstack((image, depthImage))
            if image is not None and image.size > 0:
                cv2.namedWindow("image_picture", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("image_picture", 1296, 972)
                BGRimage=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
                #print(type(BGRimage))
                cv2.imshow("image_picture", BGRimage)
                # cv2.namedWindow("depth_picture", cv2.WINDOW_NORMAL)
                # cv2.resizeWindow("depth_picture", 1296, 972)
                # cv2.imshow("depth_picture", depthImage)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("无法从字节流中读取图像或图像尺寸为0！")

            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            with open('corr_distance.txt', 'a') as f:
                result = f"time: {now_time}, corrdinates: x={d_x}, y={d_y}, z={d_z}\n"
                f.write(result)
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

