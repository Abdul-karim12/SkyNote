#!/bin/bash
dnf update -y
dnf install -y docker

systemctl enable docker
systemctl start docker

docker pull abdul324/cloud-app:latest
docker run -d -p 80:5000 abdul324/cloud-app:latest
