

docker stop $(docker ps -qa) && docker rm $(docker ps -aq)
docker network rm hadoop_net
