#!/usr/bin/python
import threading
import json
from time import sleep
import socket
import requests
from manifest import *

#def wrt():
#    os.system('touch test.log')


#atexit.register(wrt)
#while True:
#    pass


class Task(threading.Thread):
    total_thread_number = 0
    def __init__(self, addr, param_list):
        threading.Thread.__init__(self)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.param_list = param_list
        self.thread_number = Task.total_thread_number
        print('create task thread {} with'.format(self.thread_number), self.addr)
        Task.total_thread_number += 1
        
    def run(self):
        try_times = 1
        while True:
            try:
                self.socket.connect(self.addr)
                print('send task request')
            except Exception as e:
                # self.socket.close()
#                print('error occured at ', self.addr)
                if try_times < 50:
                    try_times += 1
                    continue
                else:
                    break
            
                
            data = json.dumps(list(self.param_list))

            response = requests.get(UI_HOST + '/flow/insert',
                                    params={'cid': 1, 'param': str(data), 'result': '', 'lable': '',
                                            'fstate': 1})

            #print(response.json())
            fid = response.json()
            # print(data)
            self.socket.send(data.encode())
            
            print('waiting for feedback...')
            # TODO: ALWAYS BLOCK IN HERE
            feedback = self.socket.recv(4096).decode()
            self.socket.close()
            if not feedback:
                print('receive nothing!\nwaiting...')
            else:
                feedback = json.loads(feedback)
                self.feedback = feedback
                #print('receive message successfully!')
                print('returned fitness is ', feedback['fitness'])

                res = requests.get(UI_HOST + '/flow/updateResult',
                                        params={'fid': fid, 'result':feedback['fitness'] })

                print(res.json())

                self.socket.close()
                break
            
            
      
if __name__ == '__main__':
    t = Task(1, 2)
    print(t.isAlive())  
