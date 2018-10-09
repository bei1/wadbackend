import threading
import time

# node = {1: False,
#         2: False,
#         3: False}
#
# def count():
#     global node
#     for n in node:
#         node[n] = True
#         time.sleep(1)
#         print(node[n], threading.current_thread().name)
#
#
# t = threading.Thread(target=count)
# t.start()
#
# print('continue')
#
# for s in range(5):
#     print('getdata', node, threading.current_thread().name)
#     time.sleep(1)


def check_experiment_progress(experiement_id, ack_node):
    for n in ack_node:
        ack_node[n] = True
    return ack_node

class Experiment_Monitor(threading.Thread):
    ack_node = {'node1': False,
                'node2': False,
                'node3': False,
                'node4': False,
                'node5': False}

    def __init__(self, experiement_id, thread_num=0, timeout=1.0):
        super(Experiment_Monitor, self).__init__()
        self.experiement_id = experiement_id
        self.thread_num = thread_num
        self.stopped = False
        self.timeout = timeout

    def run(self):
        while not self.stopped:
            time.sleep(1)
            self.ack_node = check_experiment_progress(self.experiement_id, self.ack_node)

    def stop(self):
        self.stopped = True

    def isStopped(self):
        return self.stopped

exp = Experiment_Monitor(1)
exp.start()

for i in range(6):
    print(exp.ack_node)
    time.sleep(2)
    if i == 2:
        exp.stop()
        print('stopped')
        exp.join()
        break


