import socket
import threading
import json
import setting
import log
import experiment
import task


def new_task(task_socket, task_address, setting):
    log.logger_wad.info("Accept new connection from %s:%s..." % task_address)
    setting.web_server_ip = task_address[0]

    data = b''
    task_socket.settimeout(1)
    while True:
        try:
            buffer = task_socket.recv(setting.receive_buffsize)
            if buffer:
                data += buffer
                log.logger_wad.info('receiving :' + str(data))
            else:
                log.logger_wad.info('receive data completed :' + str(data))
                task_socket.setblocking(1)
                break
        except Exception as e:
            task_socket.setblocking(1)
            log.logger_wad.info('receive data completed :' + str(data))
            log.logger_wad.error(str(e))
            break

    received_json = json.loads(data.decode('utf-8'))

    if (not setting.experiment) \
            and ('experiment_id' in received_json.keys()) \
            and ('group_id' in received_json.keys()):
        log.logger_wad.info('experiment not found, creating ...')
        setting.experiment = experiment.Experiment(received_json['experiment_id'],
                                                   received_json['group_id'], setting)
        log.logger_wad.info('create experiment succeed')
    else:
        log.logger_wad.info('experiment exist')

    if 'function_id' in received_json.keys():
        command = received_json['function_id']
        if command in task.Task.TASK_LIST:
            log.logger_wad.info('execute function:' + str(command))
            ack_data = task.Task.TASK_LIST[command](received_json, setting.experiment, setting)
            if ack_data:
                ack_json = json.dumps({'device_id': received_json['device_id'],
                                       'function_id': received_json['function_id'],
                                       'group_id': received_json['group_id'],
                                       'data': ack_data})
                task_socket.send(ack_json.encode('utf-8'))
                log.logger_wad.info('ack sent:' + str(ack_json))
            else:
                log.logger_wad.error('ack_data not found')
        else:
            log.logger_wad.error('function_id not in list')
    else:
        log.logger_wad.error('function_id not found')

    task_socket.close()


# main function
if __name__ == '__main__':
    log.logger_wad.info('Welcome to Wireless Attacking & Defence BackEnd')
    setting = setting.Setting()
    log.logger_wad.info('Load Setting Completed')
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(setting.server_socket)
    server.listen()
    log.logger_wad.info('Listen on ' + str(setting.server_socket[0])
                           + ':' + str(setting.server_socket[1]))
    while True:
        socket_in, socket_address = server.accept()
        new_task_thread = threading.Thread(target=new_task,
                                           args=(socket_in, socket_address, setting))
        new_task_thread.start()
