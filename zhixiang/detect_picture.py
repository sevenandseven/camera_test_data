from openni import openni2
import numpy as np
import cv2
import requests
from openni import _openni2
import csdevice as cs
from openni import _openni2 as c_api
IMAGE_REGISTRATION_DEPTH_TO_COLOR = c_api.OniImageRegistrationMode.ONI_IMAGE_REGISTRATION_DEPTH_TO_COLOR
from io import BytesIO
from PIL import Image
import os

if __name__ == "__main__":
    # 初始化相机
    openni2.initialize()
    dev = openni2.Device.open_any()
    print(dev.get_device_info())
    depth_stream = dev.create_stream(openni2.SENSOR_DEPTH)
    sensor_info = depth_stream.get_sensor_info()
    curMode = None
    for i in range(len(sensor_info.videoModes)):
        mode = sensor_info.videoModes[i]
        print(mode.pixelFormat)
        print(mode.resolutionX)
        print(mode.resolutionY)
        print(mode.fps)

        mode.resolutionX = 1920
        mode.resolutionY = 1200
        if mode.resolutionX == 1920:
            curMode = mode
    print(curMode,'\n', "**************")
    if curMode is not None:
        depth_stream.set_video_mode(curMode)
    
    color_stream = dev.create_stream(openni2.SENSOR_COLOR)
    sensor_info = color_stream.get_sensor_info()      
    for videoMode in sensor_info.videoModes:
        if videoMode.pixelFormat == _openni2.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888:
            color_stream.set_video_mode(videoMode)
            break
    # 彩色图和深度图对齐   深度图像彩色图对齐
    #re = dev.is_image_registration_mode_supported(IMAGE_REGISTRATION_DEPTH_TO_COLOR)
    # print(re, "**************")
    dev.set_image_registration_mode(True)
    # 帧同步
    dev.set_depth_color_sync_enabled(True)

    depth_stream.start()
    color_stream.start()
    cv2.namedWindow('depth')
    # cv2.setMouseCallback('depth', mousecallback)
    capture_flag = 0
    current_working_directory = os.getcwd()
    base_path = os.path.join(current_working_directory, 'data')
    count = 1
    intrinsics = depth_stream.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)
    # r = np.array(extrinsics.rotation)
    # t = np.array(extrinsics.translation)
    #print("深度相机外参：", r, '\n', t)
    c_intrinsics = color_stream.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)
    # c_extrinsics = dev.get_property(cs.CS_PROPERTY_DEVICE_EXTRINSICS,cs.Extrinsics)
    # c_r = np.array(c_extrinsics.rotation)
    # c_t = np.array(c_extrinsics.translation)
    # print("彩色相机外参：", c_r, '\n', c_t)
    

    while True:
        # 获取深度图像
        frame = depth_stream.read_frame()
        color = color_stream.read_frame()
        fx = intrinsics.fx * frame.width / intrinsics.width
        fy = intrinsics.fy * frame.height / intrinsics.height
        cx = intrinsics.cx * frame.width / intrinsics.width
        cy = intrinsics.cy * frame.height / intrinsics.height
        print("深度相机内参：", fx, fy, cx, cy)
        c_fx = c_intrinsics.fx * color.width / c_intrinsics.width
        c_fy = c_intrinsics.fy * color.height / c_intrinsics.height
        c_cx = c_intrinsics.cx * color.width / c_intrinsics.width
        c_cy = c_intrinsics.cy * color.height / c_intrinsics.height
        print("彩色相机内参：", c_fx, c_fy, c_cx, c_cy)
        # 转换数据格式  转换为numpy数组
        #dframe_data = np.array(frame.get_buffer_as_triplet()).reshape([frame.height, frame.width, 2])
        dframe_data = np.array(frame.get_buffer_as_uint16()).reshape([frame.height, frame.width])
        #print("深度图像的高宽分别是：", frame.height, frame.width)
        color_data = np.array(color.get_buffer_as_triplet()).reshape([color.height, color.width, 3])
        R = color_data[:, :, 0]
        G = color_data[:, :, 1]
        B = color_data[:, :, 2]
        color_data = np.transpose(np.array([B, G, R]), [1, 2, 0])

        # dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        # dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')
        if frame.videoMode.pixelFormat == _openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM:
            depthScale = 0.1
        elif frame.videoMode.pixelFormat == _openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM:
            depthScale = 1.0

        dim_gray = cv2.convertScaleAbs(dframe_data, alpha=0.17)
        #对深度图像进行一种图像的渲染，目前有11种渲染方式，大家可以逐一去试下
        depth_colormap = cv2.applyColorMap(dim_gray, 2)  # 有0~11种渲染的模式
        # buffer = BytesIO()
        print(type(color_data))
        cv2.imwrite(base_path+str(count)+".png",dframe_data)
        cv2.imwrite(base_path+str(count)+".jpg",color_data)
        count = count + 1
        # # 将数组写入BytesIO对象
        # buffer.write(color_data.tobytes())
        image = Image.fromarray(color_data)  
        print(type(image))
        img_io = BytesIO()  
        image.save(img_io, format='JPEG')  
        img_io.seek(0)
        # rgbpixel = color_data.tobytes()
        print(type(img_io))
        print(img_io)
        cv2.imshow('depth', depth_colormap)
        cv2.imshow('color', color_data)
        print("RGB图像的高宽分别是：", color_data.shape)

        key = cv2.waitKey(30)
        if int(key) == ord('q'):
            break
        if int(key) == ord('r'):
            capture_flag =1
        if capture_flag==1:
            name = str(count).zfill(8)
 
    depth_stream.stop()
    color_stream.stop()
    dev.close()