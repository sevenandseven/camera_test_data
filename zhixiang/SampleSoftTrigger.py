# -*- coding: utf-8 -*-
# @File   : depthimage_display.py
# @Date   : 2020/07/14
# @Author : PengLei
# @Mail   : penglei@chishine3d.com
# @bref   : This is a depth stream sample.
#           press Key 'q' to exit the sample
#           press Key '1' to increase gain
#           press Key '2' to decrease gain
import ctypes
from openni import openni2
from openni import _openni2
import csdevice as cs
import numpy as np
import cv2
import threading
import time

triggerIndex = 0
#独立的获取数据的函数
def fun(stream):
    global triggerIndex
    lastIndex = triggerIndex
    while True:
        frame = stream.read_frame() 
        
        #仅当触发信号改变后获取的第一帧图片有效。
        if lastIndex == triggerIndex:
            print('lastIndex equals triggerIndex:',lastIndex)
            continue
        lastIndex =  triggerIndex
        print('lastIndex',lastIndex)
        if frame.height > 0:
            print('frame.height:',frame.height,'frame.width:', frame.width)
            frame_data = np.array(frame.get_buffer_as_uint16()).reshape([frame.height, frame.width])
            cv2.imshow('depth', frame_data)
        key = int(cv2.waitKey(10))
        if key == KEY_q:
            return
        if key == KEY_sub:
            gain = stream.get_property(_openni2.ONI_STREAM_PROPERTY_GAIN, ctypes.c_uint32)
            gain = gain.value - 1
            stream.set_property(_openni2.ONI_STREAM_PROPERTY_GAIN, gain)
        if key == KEY_add:
            gain = stream.get_property(_openni2.ONI_STREAM_PROPERTY_GAIN, ctypes.c_uint32)
            gain = gain.value + 1
            stream.set_property(_openni2.ONI_STREAM_PROPERTY_GAIN, gain)
    
if __name__ == '__main__':
    KEY_q = 0x71
    KEY_add = 0x31
    KEY_sub = 0x32
    
    openni2.initialize()
    dev = openni2.Device.open_any()

    if dev.has_sensor(openni2.SENSOR_DEPTH) :

        stream = dev.create_stream(openni2.SENSOR_DEPTH)
        #sensor_info = stream.get_sensor_info()
        #stream.set_video_mode(sensor_info.videoModes[len(sensor_info.videoModes)-1])
        stream.start()

         # get distort
        distort = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_DISTORT,cs.Distort)
        print("distort:k1:","{:.2f}".format(distort.k1) , ",k2:","{:.2f}".format(distort.k2), " k3:","{:.2f}".format(distort.k3));

        dr = cs.DepthRange(50, 2000)
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_DEPTH_RANGE, dr)

        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_FRAMETIME, 13000)
        stream.set_property(_openni2.ONI_STREAM_PROPERTY_EXPOSURE, 12000);
        stream.set_property(_openni2.ONI_STREAM_PROPERTY_GAIN, 1)
        
        #get trigger mode 0-off 1-external trigger mode 2-software trigger mode
        trMode = stream.get_property(cs.CS_PROPERTY_STREAM_EXT_TRIGGER_MODE, ctypes.c_int)
        print ('trigger mode:',trMode.value)
	    #set trigger model is software trigger
        trMode.value = 2
        stream.set_property(cs.CS_PROPERTY_STREAM_EXT_TRIGGER_MODE, trMode.value);

        t1 = threading.Thread(target=fun, args=(stream,))
        t1.start()
        
        while True:
        
            #do softTrigger()
            #global triggerIndex
            triggerIndex = triggerIndex + 1
            stream.set_property(cs.CS_PROPERTY_STREAM_EXT_SOFT_TRIGGER,ctypes.c_uint32(0))
  
            time.sleep(1)
                
        stream.stop()
    else:
        print("Device does not have depth sensor!")
    dev.close()
