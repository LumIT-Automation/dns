%preun
#!/bin/bash

printf "\n* Container prerm...\n"

if getenforce | grep -q Enforcing;then
    echo -e "\nWarning: \e[32mselinux enabled\e[0m.  The image/container may \e[32mnot be cleaned\e[0m at the end of the process.\n"
fi

# $1 is the number of time that this package is present on the system. If this script is run from an upgrade and not
if [ "$1" -eq "0" ]; then
    printf "\n* Cleanup...\n" 

    if podman ps | awk '{print $2}' | grep -Eq '\blocalhost/dns(:|$)'; then
        podman stop -t 5 dns &
        wait $! # Wait for the shutdown process of the container.
    fi
    
    if podman images | awk '{print $1}' | grep -q ^localhost/dns$; then
        buildah rmi --force dns
    fi
    
    # Be sure there is not rubbish around.
    if podman ps --all | awk '{print $2}' | grep -E '\blocalhost/dns(:|$)'; then
        cIds=$( podman ps --all | awk '$2 ~ /^localhost\/dns(:|$)/ { print $1 }' )
        for id in $cIds; do
            podman rm -f $id
        done
    fi
fi

exit 0

