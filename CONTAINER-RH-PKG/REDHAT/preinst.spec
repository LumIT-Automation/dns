%pre
#!/bin/bash

if getenforce | grep -q Enforcing;then
    echo -e "\n* Warning: \e[32mselinux enabled\e[0m. To install this package please temporary disable it during the installation (setenforce 0), then re-enable it.\n"
    exit 1
fi

printf "\n* Container preinst...\n"
printf "\n* Cleanup...\n"

# If there is a revp container already, stop it in 5 seconds.
if podman ps | awk '{print $2}' | grep -Eq '\blocalhost/dns(:|\b)'; then
    podman stop -t 5 dns &
    wait $! # Wait for the shutdown process of the container.
fi

if podman images | awk '{print $1}' | grep -q ^localhost/dns$; then
    buildah rmi --force dns
fi

# Be sure there is not rubbish around.
if podman ps --all | awk '{print $2}' | grep -E '\blocalhost/dns(:|\b)'; then
    cIds=$( podman ps --all | awk '$2 ~ /^localhost\/dns/ { print $1 }' )
    for id in $cIds; do
        podman rm -f $id
    done
fi

exit 0

