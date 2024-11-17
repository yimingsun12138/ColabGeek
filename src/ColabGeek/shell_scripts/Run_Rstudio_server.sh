#!/usr/bin/bash

# get parameter
installation_path=$1
Rstudio_server_port=$2

# go to temp installation path
cd /tmp/$installation_path

# install Rstudio server
wget https://s3.ap-east-1.amazonaws.com/mrdoge-s3-bucket/share/resource_for_download/rstudio_server_for_Google_Colab.deb -O /tmp/$installation_path/rstudio_server.deb
gdebi -n /tmp/$installation_path/rstudio_server.deb

# configure Rstudio server port
echo "www-port=$Rstudio_server_port" > /etc/rstudio/rserver.conf

# restart Rstudio server
rstudio-server restart
