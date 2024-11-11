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

def mask_rgbd(d4d,rgb, th=0):
    """
    Overlays images and uses some blur to slightly smooth the mask
    (3L ndarray, 3L ndarray) -> 3L ndarray
    th:= threshold
    """
    mask = d4d.copy()
    #mask = cv2.GaussianBlur(mask, (5,5),0)
    idx =(mask>th)
    mask[idx] = rgb[idx]
    return mask

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
            mode.resolutionX = 1920
            mode.resolutionY = 1200
            if mode.resolutionX == 1920:
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

        ## IMPORTANT: ALIGN DEPTH2RGB (depth wrapped to match rgb stream)
        dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
        # dev.set_depth_color_sync_enabled(True) # synchronize the streams
        #dev.set_image_registration_mode(openni2.IMAGE_REGISTRATION_DEPTH_TO_COLOR)
        # get extrinsics
       
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

        # # get min contrast value (remove where fringe contrast below this value)
        # algcont = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_CONTRAST_MIN, ctypes.c_int)
        # print('algorithmContrast min:', algcont.value)

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

            dmap = np.array(frame.get_buffer_as_uint16()).reshape([frame.height, frame.width])
            color_data = np.array(frameRgb.get_buffer_as_triplet()).reshape([frameRgb.height, frameRgb.width, 3])
            R = color_data[:, :, 0]
            G = color_data[:, :, 1]
            B = color_data[:, :, 2]
            color_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
            #dmap = np.fromstring(frame.get_buffer_as_uint16()).reshape([frame.height, frame.width])
            d4d = np.uint8(dmap.astype(float) *255/ 2**12-1) # Correct the range. Depth images are 12bits
            d4d = 255 - cv2.cvtColor(d4d,cv2.COLOR_GRAY2RGB)
            #cs.align_data(frame, color_data)
            rgbd  = mask_rgbd(d4d,rgb)
            canvas = np.hstack((d4d,rgb,rgbd))
            cv2.imshow('depth || rgb', canvas )
            cv2.waitkey(0)
        stream.stop()

    else:
        print("Device does not have depth sensor!")
    dev.close()
