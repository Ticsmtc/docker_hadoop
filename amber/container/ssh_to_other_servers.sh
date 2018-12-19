#!/bin/bash

#echo $(cat ../config/server_ip_list);



ssh_to_server(){
  echo $1;
  echo setting ssh from $(hostname) to $1 ......
  expect -c "
  	set timeout -1;
  	spawn ssh-copy-id $1;
  	expect {
  		*password* {send -- $2\r;exp_continue;}
      *(yes/no)?* {send -- yes\r;exp_continue;}
  		eof {exit 0;}
  	}
  "
}



echo ssh-keygen .....
expect -c "
	set timeout -1;
	spawn ssh-keygen;
	expect {

		*:* { send -- \r;exp_continue; }
		*Overwrite\ (y/n)?* { send -- n\r; exp_continue; }
		eof { exit 0; }
	}
"



echo servers to config ....;
for addr in $(cat /home/$1/amber/config/server_ip_list); do
  echo [$(hostname) to $addr] .......;
  ssh_to_server $addr $2;
done;
