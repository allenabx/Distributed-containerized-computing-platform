#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import json
#from run_params import *
import time
from manifest import *


def eva(ind):
    #global record
    paramList = [e*ind[i] for i, e in enumerate(std_list)]
    distance = sum([(_)**2 for i, _ in enumerate(paramList)])
#    distance = run(paramList, 2, '../paramfiles/optimizing.txt')
    print('distance fitness: ', distance)
    result = {
        'params': paramList,
        'distance': distance,
        'fitness': distance
    }
    with open('walkout', 'a') as f:
        print(*paramList, distance, file=f)
    return result
        
        
def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    

if __name__ == '__main__':
    cmaes_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    cmaes_server.bind(ADDR)
    cmaes_server.listen(5)
    task_num = 0
    log = open('server.log', 'a')
    
    while True:
        try:
            
            print('listenning on ', ADDR)
            print(timestamp(), 'Wait for connection ...', file=log)
            cmaes_client, addr = cmaes_server.accept()
            print("Connection from :",addr, file=log)
            data = cmaes_client.recv(BUFFSIZE).decode()
            print('received', data, file=log)
            # TODO:condition that receive data is none
            if data:
                data_ = json.loads(data)
                print('server received data, processing...')
                send = json.dumps(eva(data_))
                cmaes_client.send(send.encode())
                print('server send data ', send, file=log)
                print('Task {} is done!'.format(task_num), file=log)
        except Exception as e:
            print(e, '\ncatch ERROR, task {} unfinished,'
            ' close socket...'.format(task_num), file=log)
        cmaes_client.close()
        print('close socket', file=log)
        task_num += 1
        if task_num % 10 == 0:
            log.flush()
