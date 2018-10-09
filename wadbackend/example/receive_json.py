import socket
import json
import base64
import io
from PIL import Image
import time



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 65533))
server.listen()
sock, addr = server.accept()

print(addr, "connected, receiving file")

# data = sock.recv(1024)
# while True:
#     buffer = sock.recv(1024)
#     if buffer:
#         data += buffer
#     else:
#         break

data = b''
# sock.settimeout(1)
while True:
    print(sock.recv(1024))
    # example:
    #     buffer = sock.recv(1024)
    #     if buffer:
    #         data += buffer
    #     else:
    #         sock.setblocking(1)
    #         break
    # except Exception as e:
    #     # print(e)
    #     sock.setblocking(1)
    #     break

sock.close()
data = data.decode('utf-8')

img_base64 = Image.open(io.BytesIO(base64.decodebytes(json.loads(data)['screenshot'].encode())))
img_base64.show()


# print(json.loads(data))
