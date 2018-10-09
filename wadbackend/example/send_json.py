import socket
import json
from PIL import ImageGrab
import io
import base64

im = ImageGrab.grab()
test_screenshot = io.BytesIO()
im.save(test_screenshot, 'png')
test_screenshot.seek(0)
base64_img = base64.encodebytes(test_screenshot.read())
base64_img_str = base64_img.decode()

send_emmbed_json = json.dumps({'hello': 'world',
                               'hahah': 123})
send_json = {'nihao': 'hi',
             'yo': 'hey',
             'ack_data': send_emmbed_json,
             'screenshot': base64_img_str}

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect(('localhost', 65533))
send_socket.send(json.dumps(send_json).encode('utf-8'))
send_socket.shutdown(1)
# send_socket.close()
