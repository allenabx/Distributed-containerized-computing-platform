#!/usr/bin/python3
import cma
import atexit
import socket
import sys
import random
from time import sleep
import pickle
import os
import json
from thread_task import Task
from manifest import *


clients = {
    h: socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for h in HOST
}
temp_pool = []
solved_solutions = []
solved_result = []


if __name__ == '__main__':
    # load cma-es generator object
    pkl = '_saved-cma-object.pkl'
    if pkl in os.listdir('.'):
        es = pickle.load(open(pkl, 'rb'))
        print('load pickle object from ', pkl)
    else:
        es=cma.CMAEvolutionStrategy(
            VECTOR_LENGTH*[1.0],
            SIGMA0,
            {
                'maxiter':MAX_ITER_NUM, 
                'popsize':POP_SIZE, 
                'bounds': BOUND
            })


    @atexit.register
    def store_data():
        """dump objects into file when program exits"""
        #print('atexit module register works, exit...')
        pickle.dump(es, open(pkl, 'wb'))
#        json.dump(record, open(PARAMS_RECORD_FILE_NAME, 'w'), indent=4, separators=(',', ': '))
        print('data has been dumped into ', pkl)
        
        
    pool_capacity = len(HOST)
    pc = pool_capacity
    batch = 0
    iteration =0
    try:
        while True:
            iteration += 1
            solutions = es.ask()
            # if not convert to list, `numpy.ndarray` will occur errors!
            solutions = [list(_) for _ in solutions]
            
            temp_pool = solutions[-pc:]
            solutions = solutions[:-pc]
            thread_pool = [
                Task((e, PORT[i]), temp_pool[i])
                for i, e in enumerate(HOST)
            ]
            for t in thread_pool:
                t.start()
            sleep(2)
            while not batch == POP_SIZE:
                print('This is iteration', iteration, 
                ', {}/{}({:.2f}%) completed'.format(batch, POP_SIZE, 100*batch/POP_SIZE)
                )
                
                for t in thread_pool:
                    if not t.isAlive():
                        if solutions:
                            temp_pool.append(solutions.pop())
                            new_thread = Task(
                                t.addr,
                                temp_pool[-1]
                            )
                            new_thread.start()
                            thread_pool.append(new_thread)
                        elif temp_pool:
                            try:
                                used = [
                                    k.param_list
                                    for k in thread_pool
                                    if k.isAlive()
                                ]
                                
                            except ValueError as e:
                                print('get value error in used', len(thread_pool), len(temp_pool))
                                break
                            # ERROR: `in` for ndarray alter `==` function
                            candidate = [
                                k for k in temp_pool if k not in used
                            ]
                            if candidate:
                                new_thread = Task(
                                    t.addr,
                                    random.choice(temp_pool)
                                )
                                new_thread.start()
                                thread_pool.append(new_thread)
                        try:
                            if t.feedback:
                                print('got feedback!')
                                print('received ', t.feedback)
                                if t.param_list in temp_pool:
                                    solved_solutions.append(t.param_list)
                                    solved_result.append(t.feedback['fitness'])
                                    with open(PARAMS_RECORD_FILE, 'a') as f:
                                        print(*(t.feedback['params']), t.feedback['distance'], sep=',', file=f)
                                    temp_pool.remove(t.param_list)
                                    batch += 1
                                else:
                                    print('repeated feedback, abandon...')
                            else:
                                print("feedback is none!")
                        
                        except AttributeError:
                            with open('hpc.log', 'a') as log:
                                print('iteration', iteration,
                                    'batch', batch, 'on ', t.addr,
                                     '\nthread feedback is illegal!',
                                     file=log)
                        except Exception as e:
                            with open('hpc.log', 'a') as log:
                                print('iteration', iteration,
                                    'batch', batch, '\n',
                                     e, '\nthread may not terminated properly...',
                                     file=log)
                            # sys.exit(2)
                        print('remove thread ', t.thread_number)
                        # remove dead thread and add new thread
                        thread_pool.remove(t)                      
                    else:
                        print('thread ', 
                            *[(_.thread_number, _.addr[0])
                            for _ in thread_pool
                            if _.isAlive()],
                             'is running', end='\r')
                sleep(UPDATE_FREQUENCY)    # once threads start, may need not to update frequently ?
            else:
                if thread_pool:
                    with open('hpc.log', 'a') as log:
                        print('iteration', iteration,
                            'batch', batch, '\n',
                             'assertion error, thread_pool is not empty...',
                             '[', *[t.thread_number for t in thread_pool], ']',
                             file=log)
                if temp_pool:
                    with open('hpc.log', 'a') as log:
                        print('iteration', iteration,
                            'batch', batch, '\n',
                             'assertion error, temp_pool is not empty...',
                             '[', *[t.thread_number for t in temp_pool], ']',
                             file=log)
#                assert not thread_pool
#                assert not temp_pool
                es.tell(solved_solutions, solved_result)
                store_data()    # store after each batch finished
                solved_solutions.clear()
                solved_result.clear()
                batch = 0
    except KeyboardInterrupt as e:
        
        print('\nreceive terminated signal, exit...\nPlease wait...')
        for c in clients.values():
            c.close()
        #store_data()
        sys.exit(1)
    
