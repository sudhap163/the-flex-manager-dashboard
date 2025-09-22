#!/bin/bash

dnf install sqlite-devel -y
dnf install epel-release -y
dnf install python3.13 -y
python3.13 -m pip install -r requirements.txt