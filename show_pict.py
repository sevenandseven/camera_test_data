# -*- coding: utf-8 -*-
# @File   : pointcloud_display.py
# @Date   : 2020/07/14
# @Author : PengLei
# @Mail   : penglei@chishine3d.com
# @bref   : This is a point cloud sample.
import ctypes
from openni import openni2
from openni import _openni2
import numpy as np
import cv2
import open3d
import csdevice as cs
import struct
import threading
import time
from PIL import Image
from io import BytesIO
import requests

if __name__ == '__main__':
    openni2.initialize()
    dev = openni2.Device.open_any()

    if dev.has_sensor(openni2.SENSOR_DEPTH) and dev.has_sensor(openni2.SENSOR_COLOR):
        stream = dev.create_stream(openni2.SENSOR_DEPTH)
        streamRgb = dev.create_stream(openni2.SENSOR_COLOR)

        # get and set video mode
        sensor_info = stream.get_sensor_info()
        sensor_infoRgb = streamRgb.get_sensor_info()
        curMode = None
        for i in range(len(sensor_info.videoModes)):
            mode = sensor_info.videoModes[i]
            print(mode.pixelFormat)
            print(mode.resolutionX)
            print(mode.resolutionY)
            print(mode.fps)
            if mode.resolutionX == 960:
                curMode = mode
            print("深度图像分辨率",mode.resolutionX)
            print("深度图像分辨率", mode.resolutionY)
        if curMode is not None:
            stream.set_video_mode(curMode)

        curMode = None
        for i in range(len(sensor_infoRgb.videoModes)):
            mode = sensor_infoRgb.videoModes[i]
            print(mode.pixelFormat)
            print(mode.resolutionX)
            print(mode.resolutionY)
            print(mode.fps)
            if mode.resolutionX == 1920:
                curMode = mode

        if curMode is not None:
            streamRgb.set_video_mode(curMode)

        # start stream
        stream.start()
        streamRgb.start()
        extrinsics = dev.get_property(cs.CS_PROPERTY_DEVICE_EXTRINSICS, cs.Extrinsics)
        print('Extrinsics(rotation = %r, translation = %r)' % (np.array(extrinsics.rotation), np.array(extrinsics.translation)))
        r = np.array(extrinsics.rotation)
        t = np.array(extrinsics.translation)
        print("旋转矩阵：", r)
        print("平移矩阵：", t)
        # get Intrinsics
        intrinsics = stream.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)
        print("深度相机fx , fy , cx, cy", (intrinsics.fx, intrinsics.fy, intrinsics.cx, intrinsics.cy, intrinsics.width))
        distort = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DISTORT,cs.Distort)
        print("distort:k1:","{:.2f}".format(distort.k1) , ",k2:","{:.2f}".format(distort.k2), " k3:","{:.2f}".format(distort.k3))
        # get Intrinsics RGB
        intrinsics_rgb = streamRgb.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)
        print("彩色相机fx , fy , cx, cy", intrinsics_rgb.fx, intrinsics_rgb.fy, intrinsics_rgb.cx, intrinsics_rgb.cy, intrinsics_rgb.width, intrinsics_rgb.height)
        print("intrinsics_rgb.width, intrinsics_rgb.height:", intrinsics_rgb.width, intrinsics_rgb.height)
        # get range of depth
        depthRange = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_RANGE, cs.DepthRange)
        print('DepthRang:', depthRange.min, depthRange.max)

        stream.set_property(_openni2.ONI_STREAM_PROPERTY_AUTO_EXPOSURE, ctypes.c_uint32(0))
        # get exposure value
        exposure = stream.get_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, ctypes.c_uint32)
        exposure = exposure.value + 100

        # set HDR mode
        # stream.set_property(cs.CS_PROPERTY_STREAM_EXT_HDR_MODE, ctypes.c_uint32(2))
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_HDR_MODE, ctypes.c_uint32(0))
        # get current HDR mode
        hdr_mode = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_HDR_MODE, ctypes.c_ulong)
        print('Get HDR_MODE:', hdr_mode.value)

        # get HdrScaleSetting
        hdrss = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_HDR_SCALE_SETTING, cs.HdrScaleSetting)
        print(
            'Get HdrScaleSetting:\nhighReflectModeCount:%d\nhighReflectModeScale:%d\nlowReflectModeCount:%d\nlowReflectModeScale:%d\n'
            % (hdrss.highReflectModeCount, hdrss.highReflectModeScale, hdrss.lowReflectModeCount,
               hdrss.lowReflectModeScale))

        # get all params of HDR
        hdrexp = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_HDR_EXPOSURE, cs.HdrExposureSetting)
        print('Get HdrExposureSetting count =', hdrexp.count)
        for param in hdrexp.param:
            print('exposure = {},gain = {}'.format(param.exposure, param.gain))
        # set range of depth
        dr = cs.DepthRange(120, 1500)
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_RANGE, dr)
        # get depth unit for real distance
        dhsc = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_SCALE, ctypes.c_float)
        print('get depth scale:', dhsc.value)

        # get trigger mode 0-off 1-external trigger mode 2-software trigger mode
        trMode = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_TRIGGER_MODE, ctypes.c_int)
        print('trigger mode:', trMode.value)

        # get frame time
        frTime = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_FRAMETIME, ctypes.c_float)
        print('get frame time:', frTime.value)

        stream.set_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, 4000)
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_FRAMETIME, 7000)
        print('set frame time:', 7000)
        while True:
            frame = stream.read_frame()
            frameRgb = streamRgb.read_frame()
            if frame.videoMode.pixelFormat == _openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM:
                depthScale = 0.1
            elif frame.videoMode.pixelFormat == _openni2.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM:
                depthScale = 1.0
            
            dframe_data = np.array(frame.get_buffer_as_uint16()).reshape([frame.height, frame.width])
            fx = intrinsics.fx * frame.width / intrinsics.width
            fy = intrinsics.fy * frame.height / intrinsics.height
            cx = intrinsics.cx * frame.width / intrinsics.width
            cy = intrinsics.cy * frame.height / intrinsics.height
            color_data = np.array(frameRgb.get_buffer_as_triplet()).reshape([frameRgb.height, frameRgb.width, 3])
            R = color_data[:, :, 0]
            G = color_data[:, :, 1]
            B = color_data[:, :, 2]
            color_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
            align = cs.align_data(frame, color_data)
            #print("rgb map1", rgbMap1)
            # pc = cs.generatePointCloud(frame, intrinsics)
            # print("方法一生成的点云是：", pc.shape)

            # image = Image.fromarray(align)  
            # print(type(image))
            # img_io = BytesIO()  
            # image.save(img_io, format='JPEG')  
            # img_io.seek(0)
            # print(type(img_io))
            # print(img_io)

            # get_api = requests.post("http://192.168.10.132:10021/api/stream_xy", files={'image':('test.jpg', img_io)})

            # if get_api.status_code == 500:
            #     d_x = 0
            #     d_y = 0
            #     d_z = 0
            #     x = 0
            #     y = 0
            # else:  
            #     inf_re =  get_api.json()
            #     for cls in inf_re["result"]:
            #         if cls["cls_name"] == "tea can":
            #             x = int(cls["center_x"])
            #             y = int(cls["center_y"]) 
            #             print(x,y)
            # if x!=0 or y ！= 0:
            #     sum = 0
            #     d_x = 0
            #     d_y = 0
            #     d_z = 0         
            #     for i in range(x-2,x+2):
            #         for j in range(y-2,y+2):
            #             if i < 0 or i > 960 or j < 0 or j > 600:
            #                 dis_z = 0
            #                 dis_x = 0         
            #                 dis_y = 0
            #             else:
            #                 dis_z =  frame[j,i] * depthScale
            #                 dis_x =  (j - cx) * z / fx
            #                 dis_y = (i - cy) * z / fy  
            #                 print(dis_z)
            #                 if dis_z > 0:
            #                     sum += 1   
            #                 d_x += dis_x
            #                 d_y += dis_y
            #                 d_z += dis_z
            #             print("有效点个数：", sum)

            #     if sum != 0:
            #         d_x = d_x / sum
            #         d_y = d_y / sum
            #         d_z = d_z / sum
            #     else:
            #         d_x = 0
            #         d_y = 0
            #         d_z = 0
            #     font = cv2.FONT_HERSHEY_SIMPLEX
            #     font_scale = 2
            #     font_color = (255, 255, 255)
            #     thickness = 3
            #     if d_x and d_y and d_z is not None:
            #         text = f'({d_x:.4f}, {d_y:.4f}, {d_z:.4f})'
            #     else:
            #         text = f'({d_x}, {d_y}, {d_z:.4f})'
            #     text_position = (x, y)
            #     color_data = color_data.copy()
            #     color_data = cv2.putText(color_data, text, text_position, font, font_scale, 65524, thickness)
            #     cv2.circle(color_data, (x,y), 20, (255,255,255))
            #     align = cv2.putText(align, text, text_position, font, font_scale, 65524, thickness)
            #     cv2.circle(align, (x,y), 20, 65536)
            #     # pct = open3d.geometry.PointCloud()
            #     # pct.estimate_normals(search_param=open3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=10))
            #     # pct.points = open3d.utility.Vector3dVector(pc)
            #     # open3d.visualization.draw_geometries([pct], window_name="Open3d", point_show_normal=True)

            #     cv2.namedWindow("align rgb", cv2.WINDOW_NORMAL)
            #     cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
            #     cv2.namedWindow("rgb", cv2.WINDOW_NORMAL)
            #     cv2.resizeWindow("align rgb", 960, 540)
            #     cv2.resizeWindow("depth", 960, 540)
            #     cv2.resizeWindow("rgb", 960, 540)
            #     cv2.imshow('align rgb', align)
            #     cv2.imshow('depth', dframe_data)
            #     #cv2.circle(co_rg, (x,y), 20, 65536)
            #     #cv2.imshow('rgb new', co_rg)
            #     cv2.imshow('rgb', color_data)
            #     cv2.waitKey(0)

            # else:
            #     print("object is not detect")
        stream.stop()

    else:
        print("Device does not have depth sensor!")
    dev.close()
