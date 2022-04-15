%post
#!/bin/bash

printf "\n* Container postinst...\n" | tee -a /dev/tty

printf "\n* Building podman image...\n" | tee -a /dev/tty
cd /usr/lib/dns

# Build container image.
buildah bud -t dns . | tee -a /dev/tty

printf "\n* The container will start in few seconds.\n\n" | tee -a /dev/tty

function containerSetup()
{
    wallBanner="RPM automation-interface-dns-container post-install configuration message:\n"
    cd /usr/lib/dns

    # Grab the host timezone.
    timeZone=$(timedatectl show| awk -F'=' '/Timezone/ {print $2}')

    # Obtain the ip address of the gateway of the default podman internal networks.
    podmanGw=`podman network inspect podman | grep gateway | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'`
    if [ -z "$gw" ]; then
        podmanNet=`podman network inspect podman | grep subnet  | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+'`
        podmanGw=`echo $podmanNet | sed -r 's/\.[0-9]+$/\.1/'`
    fi

    # First container run: associate name, bind ports, define init process, ...
    podman run --name dns -p ${podmanGw}:8300:8300/tcp -p ${podmanGw}:8301:8301/tcp -p ${podmanGw}:8302:8302/tcp -p ${podmanGw}:8500:8500/tcp -p ${podmanGw}:8600:8600/tcp -dt localhost/dns /sbin/init # bind HOST ports.

    printf "$wallBanner Starting Container Service on HOST..." | wall -n
    systemctl daemon-reload

    systemctl start automation-interface-dns-container # (upon installation, container is already run).
    systemctl enable automation-interface-dns-container

    printf "$wallBanner Set the timezone of the container to be the same as the host timezone..." | wall -n
    podman exec dns bash -c "timedatectl set-timezone $timeZone"

    # syslog-ng seems going into a catatonic state while updating a package: restarting the whole thing.
    if dpkg -l | grep automation-interface-log | grep -q ^ii; then
        if systemctl list-unit-files | grep -q syslog-ng.service; then
            systemctl restart syslog-ng || true # on host.
            podman exec dns systemctl restart syslog-ng # on this container.
        fi
    fi

    printf "$wallBanner Restarting all the container services dependant on this Consul server agent on HOST..." | wall -n
    dnsImageId=$(podman ps | grep dns | awk '{print $1}')
    otherImagesId=$(podman ps | awk '{print $1}' | grep -iv CONTAINER | grep -v $dnsImageId || true)
        if [ -n "$otherImagesId" ]; then
        echo "Restarting images: $otherImagesId"
        # Calling "restart" directly can be too fast, this avoid the "bind: address already in use" error.
        podman stop $otherImagesId
        podman start $otherImagesId
    fi

    printf "$wallBanner Installation completed." | wall -n
}

systemctl start atd

{ declare -f; cat << EOM; } | at now
containerSetup
EOM

exit 0
