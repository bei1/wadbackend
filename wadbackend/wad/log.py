import logging
import logging.handlers
import logging.config
import sys
import os
import setting

setting = setting.Setting()
LOG_DIR = setting.log_dir


def file_logger(logger_name, log_file=None, logger_type=setting.logger_type):
    console_handler = logging.StreamHandler(sys.stdout)
    logger_format = '%(asctime)s - t%(thread)d - %(levelname)s - %(name)s - %(message)s'
    formatter = logging.Formatter(logger_format)
    console_handler.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    if logger_type == 1:
        logger.addHandler(console_handler)
    elif logger_type == 2:
        file_handler = logging.handlers.RotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    elif logger_type == 0:
        file_handler = logging.handlers.RotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


def log_info(*args, logger='console'):
    def _decorated(decorated_function):
        def __inner(*args, **kwargs):
            if logger in LOGGER_LIST:
                try:
                    result = decorated_function(*args, **kwargs)
                    LOGGER_LIST[logger].info('function: ' + str(decorated_function.__name__) +
                                             ' result: ' + str(result))
                    return result
                except Exception as e:
                    LOGGER_LIST[logger].error('function: ' + str(decorated_function.__name__) +
                                              ' error: ' + str(e))

        return __inner

    return _decorated


if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

logger_console = file_logger('console', logger_type=1)
logger_wad = file_logger('wad', LOG_DIR + 'wad.log')
logger_experiment = file_logger('experiment', LOG_DIR + 'experiment.log')
logger_node = file_logger('node', LOG_DIR + 'node.log')
logger_task = file_logger('task', LOG_DIR + 'task.log')
logger_tools = file_logger('tools', LOG_DIR + 'tools.log')
logger_check = file_logger('check', LOG_DIR + 'check.log')
logger_config = file_logger('config', LOG_DIR + 'config.log')
logger_setting = file_logger('setting', LOG_DIR + 'setting.log')

LOGGER_LIST = {'console': logger_console,
               'wad': logger_wad,
               'experiment': logger_experiment,
               'node': logger_node,
               'task': logger_task,
               'tools': logger_tools,
               'check': logger_check,
               'config': logger_config,
               'setting': logger_setting
               }
