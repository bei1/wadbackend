import urllib.request
import json
import os

import time
import tools
import log
import requests


# funtion_id = 50
# 从服务器拉取文件
@log.log_info(logger='task')
def task_receive_files(received_json, experiment, setting):
    file_url = received_json['data']['file_url']
    file_name = received_json['data']['file_name']

    if not os.path.exists(setting.storage_path):
        tools.make_dirs(setting.storage_path)
    file = os.path.join(setting.storage_path, file_name)
    experiment.set_experiment_file_name(file)

    download_url = "http://" + setting.web_server_ip + ":" + str(setting.web_server_port) + file_url
    file_data = urllib.request.urlopen(download_url).read()

    print('downloading file from' + download_url)
    output = open(file, "wb")
    output.write(file_data)
    output.close()
    print('download file', file)

    file_md5 = tools.call_md5(file_data)
    ack_data = json.dumps({"file_name": file_name,
                           "check": file_md5})

    print('task_receive_files ack_data:', ack_data)
    return ack_data


# funtion_id =
# 查询配置信息并且报告给服务器
@log.log_info(logger='task')
def task2(received_json, experiment):
    pass


# funtion_id = 20
# 执行服务器配置信息指令
@log.log_info(logger='task')
def task_execute_command(received_json, experiment, setting):
    state = {'state': -1}
    if tools.json_get(received_json['data'], 'init'):
        state = experiment.init()
    elif tools.json_get(received_json['data'], 'start'):
        state = experiment.start()
    elif tools.json_get(received_json['data'], 'stop'):
        state = experiment.stop()
    elif tools.json_get(received_json['data'], 'reset'):
        state = experiment.reset()
    elif tools.json_get(received_json['data'], 'clear'):
        state = experiment.clear()
    ack_data = json.dumps(state)
    print('task_execute_command ack_data:', ack_data)
    return ack_data


# funtion_id = 40
# 查询实验进度实验结果报告给服务器
@log.log_info(logger='task')
def task_report_result(received_json, experiment, setting):
    node = experiment.get_state()
    ack_data = json.dumps(node)
    return ack_data


# funtion_id = 60
# 截图并且发送
@log.log_info(logger='task')
def task_screenshot(received_json, experiment, setting):
    image = tools.screenshot()
    ack_data = json.dumps({"state": 0})
    url = 'http://' + setting.web_server_ip + \
          ':' + str(setting.web_server_port) + setting.screenshot_url
    body = {'group_id': tools.json_get(received_json['group_id']),
            'experiment_id': tools.json_get(received_json['experiment_id']),
            'timestamp': int(time.time()),
            'screenshot_id': tools.json_get(received_json['screenshot_id'])}
    response = requests.post(url, data=body, files=image)
    log.logger_task.info('upload screenshot response ' + str(response))
    return ack_data


class Task(object):
    TASK_LIST = {'50': task_receive_files,
                 '20': task_execute_command,
                 '40': task_report_result,
                 '60': task_screenshot}
