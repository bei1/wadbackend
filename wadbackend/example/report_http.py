import http.client
import json
import time


def report_http(node_data, target_host, target_url, headers=None):
    send_json = {'device_id': '1',
                 'function_id': '40',
                 'group_id': 346,
                 'experiment_id': '020201',
                 'data': json.dumps(node_data)
                 }
    connection = http.client.HTTPConnection(target_host, port=8080)
    payload = json.dumps(send_json).encode('utf-8')
    connection.request("POST", target_url, payload)
    respose = connection.getresponse()
    data = respose.read()
    f = open('./a.html', 'wb')
    f.write(data)
    f.close()
    print(data)

node_data = {"node": 1,
             "succeed": True,
             "timestamp": int(time.time())}

report_http(node_data, '192.168.0.149', '/Experiment/Status1.do')
