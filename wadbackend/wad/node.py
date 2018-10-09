import check
import log


# format:
# method_name : experiment_<experiment_id>_node
# return_value : {<noede_number>: <node_check_funtion>}


@log.log_info(logger='node')
def experiment_0202_node():
    return {1: check.check_interface('wlan0mon'),
            2: check.check_command_log('aireplay')}
    # return {1: True}


@log.log_info(logger='node')
def experiment_0203_node():
    return {1: check.check_interface('wlan0mon'),
            2: check.check_command_log('mdk3')}


@log.log_info(logger='node')
def experiment_0301_node():
    return {1: check.check_interface('ap0')
               or check.check_interface_master('wlan0')
               or check.check_command_log('./create_ap'),
            2: check.check_fish(interface='ap0')
               or check.check_fish(interface='wlan0')
               or check.check_fish(interface='wlan1')}


@log.log_info(logger='node')
def experiment_0302_node():
    return {1: check.check_interface('ap0')
               or check.check_interface_master('wlan0')
               or check.check_command_log('./create_ap'),
            2: check.check_fish(interface='ap0')
               or check.check_fish(interface='wlan0')
               or check.check_fish(interface='wlan1')
            }


class Node(object):
    node_list = {'0202': experiment_0202_node,
                 '0203': experiment_0203_node,
                 '0301': experiment_0301_node,
                 '0302': experiment_0302_node}
