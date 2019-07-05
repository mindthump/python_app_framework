#!/usr/bin/env bash

# RUN AS SUDO

# This can easily fail as a shell script.
# It needs work, or...
# * incorporate into Dockerfile -- FAIL so far :(
# * implement in Ansible/Chef/Puppet

apt-get update
apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
usermod -a -G docker $USER

echo "(LOGOUT NOW)"