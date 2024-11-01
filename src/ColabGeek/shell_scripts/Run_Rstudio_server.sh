#!/usr/bin/bash

# go to temp installation path
cd /tmp/$1

# install
apt install gdebi-core -y
wget https://s3.ap-east-1.amazonaws.com/mrdoge-s3-bucket/share/resource_for_download/rstudio_server_for_Google_Colab.deb -O /tmp/$1/rstudio_server.deb
gdebi -n /tmp/$1/rstudio_server.deb

# config Rstudio server port
temp_var="www-port=$2"
echo $temp_var > /etc/rstudio/rserver.conf

# restart Rstudio server
rstudio-server restart
