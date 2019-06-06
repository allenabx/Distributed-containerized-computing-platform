import socket
#from run_params import readParams
_host_port = {
    'robocup3d-XPS-8920': ('192.168.210.1', 2234),
   # '3d01': ('192.168.1.137', 2974),
    #'3d02': ('192.168.1.114', 2974),
    #'3d03': ('192.168.1.177', 2974),
    #'3d04': ('192.168.1.142', 2974)
#    , 'robocup05': ('192.168.1.128', 2974)
}
UI_HOST = "http://192.168.1.156:8652"

# CONST VARIABLES
WALK_RESULT_FILE_NAME='walkout'
#PARAMS_RECORD_FILE_NAME='params-record.json'
PARAMS_RECORD_FILE_NAME='params-record.json'
PARAMS_RECORD_FILE = 'walk-record.txt'
#std_list, params_names = readParams()
std_list = [2 for i in range(5)]
VECTOR_LENGTH = len(std_list)
MAX_ITER_NUM = 20
POP_SIZE = 20
SIGMA0 = 1
BOUND = [-2., 2.]
UPDATE_FREQUENCY = 0.1

# host: local, 01, 02, 03,
HOST = [v[0] for k, v in _host_port.items()]
PORT = [v[1] for k, v in _host_port.items()]
ADDR = _host_port[socket.gethostname()]

BUFFSIZE=4096
