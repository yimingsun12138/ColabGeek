#!/usr/bin/bash

# get parameter
user_name=$1
installation_path=$2

# install the latest 64-bit Miniconda installer
mkdir -p $installation_path/miniconda3
cd $installation_path/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $installation_path/miniconda3/miniconda.sh
bash $installation_path/miniconda3/miniconda.sh -b -u -p $installation_path/miniconda3
rm -rf $installation_path/miniconda3/miniconda.sh

# initialize Miniconda
$installation_path/miniconda3/bin/conda init --all
echo "conda deactivate" >> /home/$user_name/.bashrc
