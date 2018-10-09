import socket
import json
import time

send_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
send_socket.connect(('localhost', 8000))
send_json = {'file_url': 'http://img.zcool.cn/community/01263d560504bc6ac7251df8a1bc9f.jpg',
             'device_id': 0,
             'file_name': 'test.jpg',
             'file_size': 30453192,
             'file_name_len': len('test.jpg'),
             'function_id': 0x00000001}

send_socket.send(json.dumps(send_json).encode('utf-8'))
print('sent')
data = send_socket.recv(1024).decode('utf-8')
print(json.loads(data))
send_socket.close()

