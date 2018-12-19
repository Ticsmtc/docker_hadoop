#!/bin/bash

#Author : even <stuffhello@icloud.com>
#用来配置sshd 的 配置文件 和启动sshd 进程 ，还有生成ssh密钥

echo Moving sshd_config to /etc/ssh/sshd_config .....
cp /home/$1/amber/config/sshd_config /etc/ssh/sshd_config

echo Setting the root password .....
expect -c "
	set timeout -1;
	spawn passwd root;
	expect {
		*password* {send -- $2\r;exp_continue;}
		eof {exit 0;}

	}
"
echo mkdir /run/sshd
mkdir -p /run/sshd


echo Exit Bash
