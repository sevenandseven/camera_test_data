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

        # get extrinsics
        extrinsics = dev.get_property(cs.CS_PROPERTY_DEVICE_EXTRINSICS, cs.Extrinsics)

        # get Intrinsics
        intrinsics = stream.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)

        # get Intrinsics RGB
        intrinsics_rgb = streamRgb.get_property(cs.CS_PROPERTY_STREAM_INTRINSICS, cs.Intrinsics)

        # get range of depth
        depthRange = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_RANGE, cs.DepthRange)
        print('DepthRang:', depthRange.min, depthRange.max)

        # set range of depth
        dr = cs.DepthRange(120, 500)
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_RANGE, dr)

        # set auto exposure off
        stream.set_property(_openni2.ONI_STREAM_PROPERTY_AUTO_EXPOSURE, ctypes.c_uint32(0))
        # get exposure value
        exposure = stream.get_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, ctypes.c_uint32)
        exposure = exposure.value + 100
        stream.set_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, exposure)
        print('Get exposure:', exposure)

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

        # get depth unit for real distance
        dhsc = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_SCALE, ctypes.c_float)
        print('get depth scale:', dhsc.value)

        # get trigger mode 0-off 1-external trigger mode 2-software trigger mode
        trMode = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_TRIGGER_MODE, ctypes.c_int)
        print('trigger mode:', trMode.value)

        # get min contrast value (remove where fringe contrast below this value)
        algcont = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_CONTRAST_MIN, ctypes.c_int)
        print('algorithmContrast min:', algcont.value)

        # get frame time
        frTime = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_FRAMETIME, ctypes.c_float)
        print('get frame time:', frTime.value)

        stream.set_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, 5000);
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_FRAMETIME, 7000)
        print('set frame time:', 7000)

        pc = []
        for count in range(10):
            frame = stream.read_frame()
            frameRgb = streamRgb.read_frame()

            rgbMap1 = cs.generateRGBFrame1(frame, intrinsics, extrinsics, intrinsics_rgb, mode.resolutionY, mode.resolutionX)

            print("count is %d" % count)
        stream.stop()

        pct = open3d.geometry.PointCloud()
        pct.estimate_normals(search_param=open3d.geometry.KDTreeSearchParamHybrid(radius=0.01, max_nn=10))
        pct.points = open3d.utility.Vector3dVector(pc)

        open3d.visualization.draw_geometries([pct], window_name="Open3d", point_show_normal=True)
    else:
        print("Device does not have depth sensor!")
    dev.close()
