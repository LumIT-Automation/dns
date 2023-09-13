FROM docker.io/amd64/debian:bookworm
LABEL AUTOMATION_CONTAINER_IMAGE="dns"
EXPOSE 8300/tcp
EXPOSE 8301/tcp
EXPOSE 8302/tcp
EXPOSE 8500/tcp
EXPOSE 8600/tcp

ADD PACKAGE /
ADD bootstrap.sh /
ADD hashicorp-archive-keyring.gpg /etc/apt/trusted.gpg.d/
ADD hashicorp.list /etc/apt/sources.list.d/

# RUN ["/bin/bash", "/bootstrap.sh"]
