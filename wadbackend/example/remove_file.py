import shutil
import os

PATH = './test_dir'
FILE = './test_dir/leaf_dir/test.txt'

# 删除文件，不可以是目录
#os.remove(FILE)

# 删除目录，目录必须为空
#os.rmdir(PATH)

# 递归删除目录，目录必须为空
#os.removedirs(PATH)

# 递归删除目录，包括目录下文件，必须指定目录
shutil.rmtree(PATH, ignore_errors=True)

