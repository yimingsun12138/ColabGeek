#!/usr/bin/bash

# go to temp installation path
cd /tmp/$1

# install
apt install gdebi-core -y
wget https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2024.09.0-375-amd64.deb
gdebi -n rstudio-server-2024.09.0-375-amd64.deb

# config Rstudio server port
temp_var="www-port=$2"
echo $temp_var > /etc/rstudio/rserver.conf

# restart Rstudio server
rstudio-server restart
