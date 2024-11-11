import requests
def get_result_xy():
        get_api = requests.post("http://192.168.10.132:10021/api/stream_xy", files={'image': open(r"C:\Users\Administrator\Desktop\camera_test_data\data\3_rgb.bmp", 'rb')})
        if get_api.status_code == 200:
            result =  get_api.json()
            return result
        else:  
            print(f"Failed to get response, status code: {get_api.status_code}")

x = get_result_xy()
import cv2
# x = {'file_name': '1_rgb', 
# 'result': [{'cls_name': 'watering can', 'center_x': 1135.5, 'center_y': 824.5, 'conf': 0.46}, 
# {'cls_name': 'book', 'center_x': 820.5, 'center_y': 1031.5, 'conf': 0.82}, 
# {'cls_name': 'tea can', 'center_x': 931.5, 'center_y': 699.0, 'conf': 0.83}]}
print(type(x["result"]))
re = x["result"]
for cls in x["result"]:
    print(cls, '\n')
    if cls["cls_name"] == "tea can":
        x = int(cls["center_x"])
        y = int(cls["center_y"]) 
        print(x)
        print(y)
depth = cv2.imread(r"C:\Users\Administrator\Desktop\camera_test_data\data\3_depth.png", cv2.IMREAD_UNCHANGED)             # 表示读取原图, 不进行任何改变
# center_x center_y  是水平方向和垂直方向[列 行]        python获取数据是[行，列]
z = depth[y,x] * 0.05
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 4
font_color = (255, 255, 255)
thickness = 5
text = f'({x}, {y}, {z})'
text_position = (x + 10, y)
img_bgr = cv2.putText(depth, text, text_position, font, font_scale, 65524, thickness)
cv2.circle(depth, (x,y), 10, 65524)
cv2.imshow("depth_picture", depth)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(z)