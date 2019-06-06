#!/bin/bash

source ./hosts.conf

case "$1" in
# how we start nodes
"start")

    COMMAND="$3 $INTERPRETER server.py"
    echo $BASE_CMD
    for host in $HOSTS 
    do
        echo "execute script on" $host
        COMMAND="$BASE_CMD;$COMMAND"

         #echo "running command\n" $COMMAND "\non $host"
        ssh -tt $user@$host "$COMMAND" & #> /dev/null

    done
    # running on local
    echo "start leader node"
#    $3 $INTERPRETER server.py &
    ;;
# how we stop nodes
"stop")
    # HERE WE SET HOW TO STOP SERVICE ON SERVANT NODES
    KILL_SRV="ps -ef|grep server.py|awk '{print \$2}'|xargs kill -9"
#    KILL_SRV="ps -ef|grep server.py|awk '{print \$2}'|xargs kill -9;killall $INTERPRETER\
#    ps -ef|grep rcssserver3d|awk '{print \$2}'|xargs kill -9; killall -2 agentspark"
    COMMAND="$BASE_CMD;$KILL_SRV"
    for host in $HOSTS
    do
        # echo "running command\n" $COMMAND "\non $host"
#        if [ "$host" = "$LEADER" ]
#        then
#            echo "stop leader node"
#            
#        else
            echo "stop service on" $host
            ssh -tt $user@$host "$COMMAND" & #> /dev/null
#        fi
    done
    # running on local
    
#    ps -ef|grep server.py|awk '{print $2}'|xargs kill -9
#    ps -ef|grep cma_es_hpc.py|awk '{print $2}'|xargs kill -2
#    #ps -ef|grep server.py|awk '{print $2}'|xargs kill -9
#    killall -9 rcssserver3d agentspark
    ;;
# how we clean mess
"clean")
    COMMAND="./clean.sh"
    for host in $HOSTS
    do
        echo "clean mess on" $host
        COMMAND="$BASE_CMD;$COMMAND"
        # echo "running command\n" $COMMAND "\non $host"
        ssh -tt $user@$host "$COMMAND" & #> /dev/null
    done
    ./clean.sh
    ;;
    
# how we sync files
"sync")
    for file in $SYNC_FILES
    do
        ./file_push.sh $file
    done
    ;;

# set up certain distribution task
"setup")
    COMMAND="cd ..;rm CMakeCache.txt;cmake .;make -j8"
    echo "set up task directory on" $2
    ./file_push.sh setup $2
    COMMAND="$BASE_CMD;$COMMAND"
    # echo "running command\n" $COMMAND "\non $host"
    ssh -tt $user@$2 "$COMMAND" & #> /dev/null
    ;;
   
# set up all the distribution task
"setup-all")
    # HERE WE SET HOW TO BUILD TASK CODE
#    COMMAND="cd ..;rm CMakeCache.txt;cmake .;make -j8"
    for host in $HOSTS
    do
        echo "set up task directory on" $host
        ./file_push.sh setup $host
        COMMAND="$BASE_CMD;$COMMAND"
        # echo "running command\n" $COMMAND "\non $host"
        ssh -tt $user@$host "$COMMAND" & #> /dev/null

    done
    ;;
     
# check whether errors occured on server
"inspect")
    ./file_push.sh fetch server.log
    cat 3d0* | grep -i exception
    ;;

# open all servant terminals
"open-all")
    for host in $HOSTS
    do
        gnome-terminal -x bash -c "ssh -tt optimization@$host 'cd hpc/$TASK_DIR/optimization;/bin/bash'" &
    done
    ;;

# open certain servant terminal
"open")
    gnome-terminal -x bash -c "ssh optimization@$2 \"$3\"" &
    ;;

# execute other commands  
*)
    COMMAND="$1"
    for host in $HOSTS
    do
        echo "execute script on" $host
        COMMAND="$BASE_CMD;$COMMAND"

        # echo "running command\n" $COMMAND "\non $host"
        ssh -tt $user@$host "$COMMAND" & #> /dev/null

    done
    ;;
esac






