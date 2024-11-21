import numpy as np
import open3d as o3d
from PIL import Image
import cv2

def depth_to_point_cloud(depth_map, fx, fy, cx, cy):
    # h, w = depth_map.shape
    points = []
    for v in range(1944 ):
        for u in range(2592):
            Z = depth_map[v, u] *0.05 
            X = (u - cx) * Z / fx
            Y = (v - cy) * Z / fy
            pixel_value = np.array([X, Y, Z])  
            point1 = np.linalg.inv(R_rgb) @ (pixel_value - T_rgb)                # mm单位
            points.append(point1)
            print("该点的坐标是1：", point1)
    return np.array(points)

depth_path = r'C:\Users\Administrator\Desktop\code\camera_test_data\zhiwei\data\1_depth.png'
depth_map = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
fx = 2.172816e+03
cx = 1.343087e+03
fy = 2.172372e+03
cy = 1.047689e+03

R_rgb = np.array([(9.980746e-01, -4.239562e-03, 6.188033e-02), (4.186324e-03, 9.999908e-01, 9.899716e-04), (-6.188395e-02, -7.290143e-04, 9.980831e-01)])
T_rgb = np.array([-1.162578e+02, 1.719343e-01, -8.648727e+00])

points = depth_to_point_cloud(depth_map, fx, fy, cx, cy)
print(points)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)
o3d.io.write_point_cloud('./output.ply', pcd)

# show video
vis = o3d.visualization.Visualizer()
vis.create_window()        
        #time.sleep(10)
for count in range(100000000):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    #vis.clear_geometries()
    vis.add_geometry(pcd)
    vis.run() 
    vis.destroy_window()
# o3d.io.write_point_cloud("./output.pcd", pcd)


