FROM docker.io/amd64/debian:buster
EXPOSE 8300/tcp
EXPOSE 8301/tcp
EXPOSE 8302/tcp
EXPOSE 8500/tcp
EXPOSE 8600/tcp

ADD PACKAGE /
ADD bootstrap.sh /

RUN ["/bin/bash", "/bootstrap.sh"]
