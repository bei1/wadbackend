from PIL import ImageGrab
from PIL import Image
import io
import base64

im = ImageGrab.grab()
test_screenshot = io.BytesIO()
im.save(test_screenshot, 'jpeg')
test_screenshot.seek(0)

base64_img = base64.encodebytes(test_screenshot.read()) # bytesio to bytes

stringio_screenshot = base64_img.decode()  #  bytes to str

print(stringio_screenshot)

bytes_screenshot = stringio_screenshot.encode()  # str to bytes

bytesio_screenshot = io.BytesIO(base64.decodebytes(bytes_screenshot))  # bytes to bytesio

img = Image.open(bytesio_screenshot)
img.show()

# print(type(im.tobytes()))

