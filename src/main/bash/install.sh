#!/bin/bash
# Set up the environment.
# Most work tools will be installed in the cloud, but the cli and emacs are nice to have
apt install awscli bzip2 emacs ess libcurl4-openssl-dev libssl-dev -y
wget \
    https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    --no-check-certificate

bash Miniconda3-latest-Linux-x86_64.sh -p ~/miniconda3 -b
echo 'PATH=$HOME/miniconda3/bin:$PATH' >> $HOME/.bashrc
. ~/.bashrc
rm  Miniconda3-latest-Linux-x86_64.sh

conda install jupyter -y
