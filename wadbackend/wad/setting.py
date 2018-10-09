class Setting(object):
    localhost = '0.0.0.0'
    localhost_port = 8000
    server_socket = (localhost, localhost_port)
    receive_buffsize = 1024

    web_server_ip = '192.168.0.149'
    web_server_port = 8080
    web_socket_server = (web_server_ip, 8000)
    report_url = '/Experiment/Status1.do'
    screenshot_url = '/Experiment/UploadImg.do'

    # storage_path = './wad/'
    # experiment_dir = './root/wad/'
    storage_path = '/usr/local/share/wadbackend/downloads/'
    experiment_dir = '/root/wad/'

    experiment = False

    device_type = 1

    logger_type = 0
    # log_dir = '../logs/'
    # command_log = '../logs/command.log'
    log_dir = '/usr/local/share/wadbackend/logs/'
    command_log = '/usr/local/share/wadbackend/logs/command.log'
