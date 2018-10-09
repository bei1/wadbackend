import hashlib
from PIL import Image
import io
import base64
import os, tempfile, subprocess
import shutil
import log


@log.log_info(logger='tools')
def call_md5(data):
    file_to_md5 = data
    md5_file = hashlib.md5(file_to_md5)
    md5 = md5_file.hexdigest()
    return md5


@log.log_info(logger='tools')
def screenshot(bbox=None):
    f, file = tempfile.mkstemp('.jpg')
    os.close(f)
    subprocess.call(['gnome-screenshot', '-f', file])
    im = Image.open(file)
    im.load()
    os.unlink(file)
    if bbox:
        im = im.crop(bbox)
    return im


@log.log_info(logger='tools')
def screenshot_str():
    im = screenshot()
    test_screenshot = io.BytesIO()
    im.save(test_screenshot, 'jpg')
    test_screenshot.seek(0)
    base64_img = base64.encodebytes(test_screenshot.read())  # bytesio to bytes
    stringio_screenshot = base64_img.decode()  # bytes to str
    return stringio_screenshot


@log.log_info(logger='tools')
def check_file_exist(File):
    return os.path.exists(File)


@log.log_info(logger='tools')
def unzip(file, target_dir, format='zip'):
    print("unzipping " + file + " to " + target_dir)
    shutil.unpack_archive(file, target_dir, format)


@log.log_info(logger='tools')
def remove_files(target_dir):
    shutil.rmtree(target_dir, ignore_errors=True)


@log.log_info(logger='tools')
def remove_file(target_file):
    os.remove(target_file)


@log.log_info(logger='tools')
def make_file(file='/usr/local/share/wadbackend/logs/command.log'):
    process = os.popen('touch ' + file + ' && chmod 666 ' + file)
    process.close()


@log.log_info(logger='tools')
def empty_file(target_file='/usr/local/share/wadbackend/logs/command.log'):
    process = os.popen('echo begin > ' + target_file)
    process.close()


@log.log_info(logger='tools')
def make_dirs(path):
    os.makedirs(path, exist_ok=True)


@log.log_info(logger='tools')
def json_get(json, json_key):
    if json_key in json.keys():
        return json[json_key]
    else:
        return False
