import cv2

img = cv2.imread(r"C:\Users\Administrator\Desktop\camera_test_data\data\1_rgb.bmp")
depth = cv2.imread(r"C:\Users\Administrator\Desktop\camera_test_data\data\1_depth.png")
print(type(img))
#cv2.rectangle(img, (400,200), (700,500), (255,0,0))
point = (931, 699)
cv2.circle(img, point, 10, 63353)
cv2.circle(depth, point, 10, 63353)
cv2.imshow("picture", img)
cv2.imshow("depth_picture", depth)
cv2.waitKey(0)
cv2.destroyAllWindows()