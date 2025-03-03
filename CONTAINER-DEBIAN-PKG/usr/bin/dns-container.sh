#!/bin/bash

function start() {
    # Check if it's up the podman internal interface (the gw of the containers), otherwise wait for 10 seconds (3 attempts).
    gwIp=$(podman network inspect podman --format  "{{range .Subnets}}{{.Gateway}}{{end}}")
    for _ in $(seq 1 3); do
        if ping -c 1 -w 1 $gwIp; then
            break
        else
            echo "Interface $gwIp still down."
        fi
        sleep 10
    done

    podman start dns
}

function stop() {
    podman stop -t 15 dns
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

        restart)
            stop
            start
            ;;

        *)
            echo $"Usage: $0 {start|stop|restart}"
            exit 1
esac

exit 0
