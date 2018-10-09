import threading
import json
import socket
import time
import tools
import node
import check
import http.client
import log


class Experiment(object):
    def __init__(self, experiment_id, group_id, setting):
        self.experiment_id = experiment_id
        self.experiment_group = group_id
        self.experiment_monitor = Experiment_Monitor(experiment_id, group_id, setting)
        self.experiment_monitor.setDaemon(True)
        self.experiment_file_name = ''
        self.experiment_dir = setting.experiment_dir
        self.setting = setting

    @log.log_info(logger='experiment')
    def get_state(self):
        return self.experiment_monitor.ack_node

    @log.log_info(logger='experiment')
    def set_experiment_file_name(self, file_name):
        self.experiment_file_name = file_name

    @log.log_info(logger='experiment')
    def get_experiment_file_name(self):
        return self.experiment_file_name

    @log.log_info(logger='experiment')
    def set_experiment_dir(self, path):
        self.experiment_dir = path

    @log.log_info(logger='experiment')
    def get_experiment_dir(self):
        return self.experiment_dir

    @log.log_info(logger='experiment')
    def init(self):
        tools.remove_files(self.experiment_dir)
        tools.make_dirs(self.experiment_dir)
        tools.make_file(self.setting.command_log)
        if check.check_file_exist(self.setting.command_log):
            tools.empty_file(self.setting.command_log)

        log.logger_experiment.info('unzipping file ' + self.experiment_file_name)
        tools.unzip(self.experiment_file_name, self.experiment_dir)
        ack_data = {'state': 0}
        return ack_data

    @log.log_info(logger='experiment')
    def start(self):
        if not self.experiment_monitor.is_running():
            self.experiment_monitor.start()
        ack_data = {'state': 0}
        return ack_data

    @log.log_info(logger='experiment')
    def stop(self):
        self.experiment_monitor.stop()
        ack_data = {'state': 0}
        return ack_data

    @log.log_info(logger='experiment')
    def reset(self):
        self.init()
        self.experiment_monitor.clear()
        self.setting.experiment = False
        ack_data = {'state': 0}
        return ack_data

    @log.log_info(logger='experiment')
    def clear(self):
        self.experiment_monitor.stop()
        tools.remove_files(self.experiment_dir)
        tools.remove_files(self.experiment_file_name)
        tools.remove_file(self.setting.command_log)
        self.setting.experiment = False
        ack_data = {'state': 0}
        return ack_data


class Experiment_Monitor(threading.Thread):
    def __init__(self, experiment_id, group_id, setting):
        super(Experiment_Monitor, self).__init__()
        self.experiment_id = experiment_id
        self.node_id = experiment_id[0:4]
        self.group_id = group_id
        self.stopped = False
        self.ack_node = node.Node.node_list[self.node_id]()
        self.setting = setting
        self.running = False
        self.report_retry_count = 0

    @log.log_info(logger='experiment')
    def check_experiment_progress(self):
        current_node = node.Node.node_list[self.node_id]()
        if current_node.items() - self.ack_node.items():
            diff_node = current_node.items() - self.ack_node.items()

            # item[0] : node number
            # item[1] : node state
            for item in diff_node:
                if item[1]:
                    node_data = {"node": item[0],
                                 "succeed": item[1],
                                 "timestamp": int(time.time())}
                    threading.Thread(target=self.report_http, args=(node_data,
                                                                    self.setting.web_server_ip,
                                                                    self.setting.report_url,
                                                                    self.setting.web_server_port)).start()
                    # self.report_http(node_data,
                    #                  self.setting.web_server_ip,
                    #                  self.setting.report_url,
                    #                  self.setting.web_server_port)
            for n in current_node:
                if current_node[n]:
                    self.ack_node[n] = True
            if check.check_dictionary_all_true(self.ack_node):
                if self.node_id == '0201' or self.node_id == '0202':
                    self.stop()
                else:
                    node_data = {"node": 9,
                                 "succeed": True,
                                 "timestamp": int(time.time())}
                    threading.Thread(target=self.report_http, args=(node_data,
                                                                    self.setting.web_server_ip,
                                                                    self.setting.report_url,
                                                                    self.setting.web_server_port)).start()
                    self.stop()

    def run(self):
        self.running = True
        self.clear()
        print('Experiment_Monitor is running')
        print('Experiment_Monitor ack_node', self.ack_node)
        while not self.stopped:
            time.sleep(1)
            self.check_experiment_progress()

    @log.log_info(logger='experiment')
    def stop(self):
        self.setting.experiment = False
        self.stopped = True
        return True

    @log.log_info(logger='experiment')
    def is_running(self):
        return self.running

    @log.log_info(logger='experiment')
    def is_stopped(self):
        return self.stopped

    @log.log_info(logger='experiment')
    def clear(self):
        for n in self.ack_node:
            self.ack_node[n] = False

    @log.log_info(logger='experiment')
    def report(self, node_data):
        try:
            send_json = {'device_id': '1',
                         'function_id': '40',
                         'group_id': self.group_id,
                         'experiment_id': self.experiment_id,
                         'data': json.dumps(node_data)
                         }
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect(self.setting.web_socket_server)
            send_socket.send(json.dumps(send_json).encode('utf-8'))
        except Exception as e:
            print(e, 'report failed')

    @log.log_info(logger='experiment')
    def report_all(self):
        try:
            send_json = {'device_id': '1',
                         'function_id': '40',
                         'group_id': self.group_id,
                         'experiment_id': self.experiment_id,
                         'data': json.dumps(self.ack_node)
                         }
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            send_socket.connect(self.setting.web_socket_server)
            send_socket.send(json.dumps(send_json).encode('utf-8'))
        except Exception as e:
            print(e, 'report failed')

    @log.log_info(logger='experiment')
    def report_http(self, node_data, target_host, target_url, target_port=80):
        try:
            send_json = {'device_id': '1',
                         'function_id': '40',
                         'group_id': self.group_id,
                         'experiment_id': self.experiment_id,
                         'data': json.dumps(node_data)
                         }
            log.logger_experiment.info('HTTPConnecting to ' + str(target_host) +
                                       str(target_port))
            connection = http.client.HTTPConnection(target_host, port=target_port)
            log.logger_experiment.info('HTTPConnected ' + str(target_host) +
                                       str(target_port))
            payload = json.dumps(send_json).encode('utf-8')
            log.logger_experiment.info('payload ' + str(payload))
            connection.request("POST", target_url, payload)
            log.logger_experiment.info('reported to '
                                       + str(target_host)
                                       + str(target_port)
                                       + target_url)
        except Exception as e:
            log.logger_experiment.error(str(e) + ' report failed')
            log.logger_experiment.info('Retry')
            self.report_http()
