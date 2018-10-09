import time
import threading
import subprocess


def check():
    global count
    count += 1
    print('new_thread count: ', count)
    time.sleep(1)
    return count


count = 0

d = {1: 1,
     2: check()}

for i in range(10):
    # c = {1: 1,
    #     2: check()}
    c = d
    print(c)
