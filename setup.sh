#!/bin/bash

dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y
dnf install sqlite-devel -y
dnf install epel-release -y
dnf install python3.13 -y
python3.13 -m pip install -r requirements.txt