#!/bin/bash
apt install -y r-base-core ess git gdebi-core docker.io

sudo su - \
     -c "R -e \"install.packages('shiny', repos='https://cran.rstudio.com/')\""

wget https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.7.907-amd64.deb
gdebi shiny-server-1.5.7.907-amd64.deb -y
rm shiny-server-1.5.7.907-amd64.deb

git clone https://github.com/rstudio/shiny-examples.git
cd shiny-examples
cp -R 086* 000-crypto-map

wget \
    https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    --no-check-certificate
bash Miniconda3-latest-Linux-x86_64.sh -p ~/miniconda3 -b
echo 'PATH=$HOME/miniconda3/bin:$PATH' >> $HOME/.bashrc
. ~/.bashrc
rm  Miniconda3-latest-Linux-x86_64.sh

pip install -y docker
conda install -y boto3
