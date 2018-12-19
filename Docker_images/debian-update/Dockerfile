FROM debian
MAINTAINER Even <stuffhello@icloud.com>


RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata



RUN apt-get update
RUN apt-get install openssh-server -y
RUN apt-get install tcl tk expect -y






#生成一个debian-update镜像备用，以免作为测试的镜像总是需要更新，非常麻烦。
