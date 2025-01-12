# 启动nginx 容器
docker run -d -p 80:80 --name nginx nginx
# 查看启动容器
docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS                NAMES
aa294dd139ba   nginx     "/docker-entrypoint.…"   21 seconds ago   Up 21 seconds   0.0.0.0:80->80/tcp   nginx
# 查看启动容器的进程
docker inspect --format '{{.State.Pid}}' aa294dd139ba
9723
# 查看进程详情
ps -ef | grep 9723
# 查看进程的命名空间
lsns -task 9723
# 进入容器的命名空间
sudo nsenter -t 9723 -n mount
