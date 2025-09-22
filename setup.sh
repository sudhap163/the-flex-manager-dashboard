#!/bin/bash

dnf update -y
dnf groupinstall "Development Tools" -y
dnf install openssl-devel libffi-devel bzip2-devel wget -y
dnf install sqlite-devel -y

wget https://www.python.org/ftp/python/3.13.3/Python-3.13.3.tgz # Replace 'x' with the latest patch version
tar -xf Python-3.13.3.tgz
cd Python-3.13.3/

./configure --enable-optimizations --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib"
make -j $(nproc) # Use all available CPU cores for faster compilation
make altinstall

python3.13 --version
pip3.13 --version

cd ../
pip3.13 install -r requirements.txt