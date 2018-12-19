#当正常使用的时候，就作为
#FROM debian 
FROM debian-update
MAINTAINER Even <stuffhello@icloud.com>


RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata


#add hadoop user and hadoop group 
RUN groupadd hadoop
RUN useradd -ms /bin/bash hadoop_admin -g hadoop
RUN usermod -G users hadoop_admin


#为了让速度变快，先将这些作为debian-update镜像进行拓展，加快开发速度
#RUN apt-get update



#install package
RUN apt-get install tcl tk expect -y
RUN apt-get install -y openssh-server screen 



#change root password
RUN echo root:hadoop_root | chpasswd

#change hadoop_admin password
RUN echo hadoop_admin:hadoop_admin | chpasswd


#hadoop operations
USER hadoop_admin
WORKDIR /home/hadoop_admin



#finish
CMD /bin/bash













