#!/bin/bash

source ./hosts.conf
#HOST_NUM=3
INPUT=$1
OUTPUT=$2


#CUR_TASK=$(basename $BASE_DIR)

case "$1" in
"fetch")
    for host in $HOSTS
    do
        echo "fetch file <$2> from $host"
        scp -r optimization@$host:~/roboucp3d/$TASK_DIR/optimization/$2 $host-$2
    done
    ;; 
"setup")
    COPY_PATH=hpc/
#    for ((i=1;i<=$HOST_NUM;i++)); do
    COMMAND="if [ -d hpc ] ; then echo; else mkdir hpc; fi;$BASE_CMD"
    ssh -tt optimization@$2 "$COMMAND" &
    sleep 1
    echo "copy task directory <$TASK_DIR> to" $2
    # rsync -av -e ssh --exclude='../CMakeFiles' $BASE_DIR optimization@$2:$COPY_PATH
    scp -r $BASE_DIR optimization@$2:$COPY_PATH
#    done
    ;;
*)
    for host in $HOSTS
    do
        echo "copy file <$1> to" $host
        scp -r $INPUT optimization@$host:~/hpc/$TASK_DIR/optimization/$1
    done
    ;;
esac
