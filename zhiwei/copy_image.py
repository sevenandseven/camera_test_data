import os
import shutil

# 指定要搜索的文件夹路径
source_folder = r'C:\Users\Administrator\Desktop\camera_test_data\data'
# 指定目标文件夹路径
destination_folder = r'C:\Users\Administrator\Desktop\camera_test_data\rgb_data'
# 指定要搜索的字符串
search_string = 'rgb.bmp'

# 确保目标文件夹存在
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for filename in os.listdir(source_folder):
    # 检查文件名是否包含指定的字符串
    if search_string in filename:
        source_file_path = os.path.join(source_folder, filename)
        # 构建目标文件的完整路径
        destination_file_path = os.path.join(destination_folder, filename)
        # 复制文件
        shutil.copy2(source_file_path, destination_file_path)
        print(f'文件已复制: {source_file_path} -> {destination_file_path}')