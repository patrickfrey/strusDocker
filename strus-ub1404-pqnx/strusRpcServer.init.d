#!/bin/bash
#
# Init file for strus RPC server
#
# description: strus RPC server
# processname: strusRpcServer

RETVAL=0
PROG="strusRpcServer"
OPTIONS=
PIDFILE=/var/run/$PROG.pid
STORAGE='path=/srv/strus/storage;cache=1G'
USER=strus
CMD="nohup strusRpcServer -c -s '$STORAGE' -p 7181 &"

runlevel=$(set -- $(runlevel); eval "echo \$$#" )

start_error()
{
	echo "failed to start $PROG"
}

start()
{
        echo -n "Starting $PROG: "
        sudo su - $USER -c "$CMD"
        [ "$?" = 0 ] && ( touch /var/lock/strusRpcServer; ps -fe | grep $PROG | grep $STORAGE | awk '{print $2}' > $PIDFILE )
}

stop()
{
        echo -n $"Stopping $PROG: "
        kill `cat $PIDFILE`
        RETVAL=$?
        [ "$RETVAL" = 0 ] && rm -f /var/lock/strusRpcServer && rm -f $PIDFILE
        echo
}

case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        restart)
                stop
                start
                ;;
        status)
                if [ -f $PIDFILE ]; then
                        PID=`cat $PIDFILE`
                        kill -0 $PID
                        if [ "$?" == "0" ]; then 
                                echo "$PROG is running PID $PID"
                        else
                                echo "$PROG is not running, but pidfile exists"
                        fi
                else
                        echo "$PROG is not running"
                fi
                ;;
        *)
                echo $"Usage: $0 {start|stop|restart|status}"
                RETVAL=1
esac
exit $RETVAL

