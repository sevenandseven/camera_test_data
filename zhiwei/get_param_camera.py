
from DkamSDK import *
#发现局域网内的相机
camera_num = DiscoverCamera()
print("camera_num=", camera_num)
#对局域网内的相机进行排序
if camera_num > 0:
    camera_sort = CameraSort(0)
    print("camera_sort=", camera_sort)
camera_ret = 0
for i in range(camera_num):
    print("IP:", CameraIP(i))
    if CameraIP(i) == b'192.168.40.78':
        camera_ret = i
camera_obj1 = CreateCamera(camera_ret)
#连接相机
connect = CameraConnect(camera_obj1)
print("connect=", connect)
if connect == 0:  
	# 获取相机内参
    kc=new_floatArray(5)
    kk=new_floatArray(9)
    # （0:红外 1:RGB    2:红外   2 双目相机适用   
    #  CMOS的畸变参数（K1K2P1P2K3）    K1 K2K3:径向畸变参数      P1 P2 :切向畸变参数     fx fy：焦距    cx cy：主点
    print("GetCamInternelParameter:",GetCamInternelParameter(camera_obj1,0,kc,kk))
    for i in range(5):
        print("kc:%e" %floatArray_getitem(kc,i))
    for n in range(9):
        print("kk:%e" %floatArray_getitem(kk, n))
    delete_floatArray(kc)
    delete_floatArray(kk)
     # 获取外参         R: 当前CMOS相对于红外CMOS坐标系的旋转矩阵       当前CMOS相对于红外CMOS坐标系的平移向量
    R = new_floatArray(9)
    T = new_floatArray(3)
    print("GetCamExternelParameter:",GetCamExternelParameter(camera_obj1,0,R,T))
    for j in range(0,9):
        print("R:%e" % floatArray_getitem(R, j))
    for m in range(0,3):
        print("T:%e" % floatArray_getitem(T, m))
    delete_floatArray(R)
    delete_floatArray(T)
    #断开相机
    disconnect = CameraDisconnect(camera_obj1)
    print("disconnect=", disconnect)

    DestroyCamera(camera_obj1)
	
