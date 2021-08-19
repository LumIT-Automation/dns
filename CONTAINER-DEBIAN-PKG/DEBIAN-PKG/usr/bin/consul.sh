#!/bin/bash

set -e

function start() {
    # Start the Consul server agent.
    # Bind to *the* interface available within the container.
    /usr/bin/consul agent -server -bootstrap -config-dir=/etc/consul.d/ -data-dir=/var/lib/consul/
}

function stop() {
    /usr/bin/consul leave
}

function reload() {
    /usr/bin/consul reload
}

function restart() {
    stop
    sleep 1
    start
}

case $1 in
        start)
            start
            ;;

        stop)
            stop
            ;;

        reload)
            reload
            ;;

        restart)
            stop
            start
            ;;

        *)
            echo $"Usage: $0 {start|stop|reload|restart}"
            exit 1
esac

exit 0
