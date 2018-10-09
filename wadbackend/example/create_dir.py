import os

PATH = './test_dir/leaf_dir/'
FILE = 'test.txt'
DATA = 'This is test file'

# 递归创建目录, exist_ok 为 True，如果目录存在不会报错
os.makedirs(PATH, exist_ok=True)

# 创建目录
os.mkdir(PATH+"single_dir/")

# 写一个 test 文件
output = open(PATH+FILE, "wb")
output.write(DATA.encode("utf-8"))
output.close()