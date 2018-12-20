#!/usr/bin/env python3
#Author : even <stuffhello@icloud.com>
#Amber的主要控制脚本，
#[1] 生成所有hadoop集群共有的/etc/hosts文件
#[2] 所有的hadoop的配置文件 /etc/slave
#[3] 配置集群之间计算机的ssh免密
#[4] 创建容器


import os
import sys 


HOST_LIST = []





def config_container_sshd(ContainerName,UserName,UserPassword,RootPassword):

	print("["+ContainerName+"]Moving sshd_config_file to system path and set root password")
	os.system("docker exec -d -u root " + ContainerName + " /home/" + UserName + "/amber/container/sshd_config.sh " + UserName + " " + RootPassword)
	#print("["+ContainerName+"]Success");

	print("["+ContainerName+"]Start /usr/sbin/sshd -D")
	os.system("docker exec -d -u root " + ContainerName + " /usr/sbin/sshd -D")

	print("["+ContainerName+"]Moving hosts_file to system path")
	os.system("docker exec -d -u root " + ContainerName + " /home/" + UserName + "/amber/container/hosts_config.sh " + UserName)
	#print("["+ContainerName+"]Success");



	


	return 

def config_container_ssh(ContainerName,UserName,UserPassword,RootPassword):
	print("["+ContainerName+"]Config root ssh to other servers")
	os.system("docker exec -d -u root " + ContainerName + " /home/" + UserName + "/amber/container/ssh_to_other_servers.sh " + UserName + " " + RootPassword)
	#print("["+ContainerName+"]Success");

	print("["+ContainerName+"]Config hadoop user ssh to other servers")
	os.system("docker exec -u " + UserName + " " + ContainerName +" /home/" + UserName + "/amber/container/ssh_to_other_servers.sh " + UserName + " " + UserPassword)

	print("["+ContainerName+"]Config hadoop")
	os.system("docker exec -d -u " + UserName + " " + ContainerName + " /home/" + UserName + "/amber/container/hadoop_config.sh")

	return 

#create_container()	创建一个容器
#ContainerName 		容器的名称，同时也是容器内的hostname
#NetName			Hadoop集群的子网名称
#IpAddress			分配给这个容器的ip地址
#UserName			用来运行hadoop和amber的用户名
def create_container(ContainerName,NetName,IpAddress,UserName):


	global HOST_LIST

	print("Create container : " + ContainerName)
	abslute_dir_path = os.path.dirname(os.path.realpath(__file__))
	print("-v " + abslute_dir_path + ":/home/" + UserName + "/amber" + " ")

	os.system(
		"docker run -dt " +
		"--name " + ContainerName + " " +

		"-v " + abslute_dir_path + ":/home/" + UserName + "/amber" + " " +


		"--hostname " + ContainerName + " " +
		"--network " + NetName + " " +
		"--ip " + IpAddress + " " +
		"ssh-setup"
	)

	HOST_LIST += [IpAddress + "	" + ContainerName + "\n"]

	return
def create_hadoop_net(NetName):

	print("Create " + NetName + " .....")

	os.system(
		"docker network create " +
		"--subnet=172.20.0.0/16 " +
		NetName
	)

	return




#
#
#
#
def create_hosts_file():


	global HOST_LIST

	abslute_dir_path = os.path.dirname(os.path.realpath(__file__))

	templete = open(abslute_dir_path + "/config/hosts.temp",mode="r")
	hosts_file = open(abslute_dir_path + "/config/hosts",mode="w")
	server_ip_list = open(abslute_dir_path + "/config/server_ip_list",mode="w")
	slaves_list = open(abslute_dir_path + "/config/hadoop_etc/slaves",mode="w")

	templete_str = templete.readlines()
	templete_str += HOST_LIST

	for line in iter(templete_str):
		if line[0] == '#': continue
		hosts_file.write(line)
		#print(line);

	for line in iter(HOST_LIST):
		server_ip_list.write(line)
		#print(line);

	for line in iter(HOST_LIST):
		ipAndName = line.split()
		print(ipAndName)
		if ipAndName[1] != "master":
			slaves_list.write(ipAndName[1] + "\n")







	templete.close()
	hosts_file.close()
	server_ip_list.close()	
	slaves_list.close()

def config_hadoop(ContainerName):
	pass



if __name__ == "__main__":

	RootPassword = "hadoop_root"
	UserPassword = "hadoop_admin"

	create_hadoop_net("hadoop_net")
	
	



	create_container("master","hadoop_net","172.20.0.10","hadoop_admin")
	for namei in range(1,5):
		create_container("slave"+str(namei),"hadoop_net","172.20.0.1"+str(namei),"hadoop_admin")	




	create_hosts_file()
	
	config_container_sshd("master","hadoop_admin",UserPassword,RootPassword)
	for namei in range(1,5):
		config_container_sshd("slave"+str(namei),"hadoop_admin",UserPassword,RootPassword)	
		
	config_container_ssh("master","hadoop_admin",UserPassword,RootPassword)
	for namei in range(1,5):
		config_container_ssh("slave"+str(namei),"hadoop_admin",UserPassword,RootPassword)











	exit(0)
