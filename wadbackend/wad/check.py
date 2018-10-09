import os
import tools
import log


@log.log_info('check')
def check_interface(interface):
    exist = tools.check_file_exist('/sys/class/net/' + interface)
    return exist


@log.log_info('check')
def check_dictionary_all_true(dictionary):
    count = 0
    flag = False
    for n in dictionary:
        if dictionary[n]:
            count += 1
        if count == len(dictionary):
            flag = True
        else:
            flag = False
    return flag


@log.log_info('check')
def check_command_log(target, command_log='/usr/local/share/wadbackend/logs/command.log'):
    process = os.popen("cat " + command_log + " | cut -d ']' -f 2 | grep '^ "
                       + target + "' | tail -n 10")
    output = process.read()
    output = output.strip()
    process.close()

    if target == 'aireplay':
        if '-0' in output and '-a' in output and '-c' in output and 'wlan0mon' in output:
            return True
        else:
            return False
    elif target == 'mdk3':
        if ' a' in output and '-a' in output and 'wlan0mon' in output:
            return True
        else:
            return False
    elif target == './create_ap':
        if 'eth0' in output:
            return True
        else:
            return False


@log.log_info('check')
def check_fish(create_path='/usr/local/share/create_ap/', interface='wlan0'):
    process = os.popen(create_path + 'create_ap --list-client ' + interface)
    output = process.read()
    output = output.strip()
    process.close()
    sum = 0
    for i in range(0, len(output)):
        str = output[i:]
        if (str.find('MAC') == 0):
            sum += 1
        else:
            continue
    if sum >= 1:
        return True
    else:
        return False


@log.log_info(logger='check')
def check_interface_master(interface='wlan0'):
    process = os.popen('iwconfig ' + interface)
    output = process.read()
    output = output.strip()
    process.close()
    if 'Mode:Master' in output:
        return True
    else:
        return False
