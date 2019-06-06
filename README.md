# Simple Distribution Computation via TCP
---

To accelerate the training speed on *rcssserver3d*, we set up a simple distribution computation platform. 
In order to deploy your tasks, you just need to do as follows:

#### Set up Servant Computation Node
1. create an account called *optimization* on each servant computer
2. open ssh port, add leader computer's public key to `~/.ssh/authorized_keys`
3. set up the environment that your task need

#### Edit the Configuration Files
1. edit `manifest.py`
```python
_host_port = {
    # here we set the hosts name, hosts IP, hosts TCP port
    'your_host_name': ('123.123.123.123', 2333),
    'your_host_name2': ('123.123.123.124', 2333),
    ......
}
```
There may be other options that you need to reedit in your task
2. edit `hosts.conf`, add your servant hosts into *HOSTS* and set your total number of your hosts

3. edit `server.py`, alter the *eva* function that you need to solve

4. edit `clean.sh`, set up your cleaning rules. Be carefull to deal with your important files.


#### Deploy Tasks into Sercant Nodes via Shell Scripts
```sh
./cmd_push.sh setup *ip or hostname* # set up one node
./cmd_push.sh setup-all # set up all nodes
``
#### Kick off Tasks
1. first start servant nodes by `./cmd_push.sh start`
2. run `python3 cma_es_dc.py`

#### Check the State of Servant Nodes
- simply you can use `./cmd_push.sh inspect` to check whether errors or exceptions occurred during server running. Also you can change the error catching key word in `cmd_push.sh`
- Sometime you may need to check the exact running state on servant node, you can just use
    - `./cmd_push.sh open *ip addr*` to open one terminal for servant node
    - `./cmd_push.sh open-all` to open terminals for all servant nodes
```bash
./cmd_push.sh start

#### File Interaction
- To get file from servant nodes
    - execute `./file_push.sh fetch *filename*` to fetch files renamed with prefix of their IP, an example may be as follows
    ```
    192.168.1.114-walkout  192.168.1.142-walkout  192.168.1.177-walkout
    192.168.1.137-walkout  192.168.1.145-walkout
    ```
- To push files from local to all servant nodes
    `./file_push.sh *filename*`

#### Clean Mess
execute `./cmd_push.sh clean` to clean all messes your task created, clean rules can be altered by editing the `clean.sh` file

#### Result Plot
- You can plot the result by `python3 result_plot.py`

python3 cma_es_dc.py # You'd better run this command in other terminal
```
