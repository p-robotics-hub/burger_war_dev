#!/bin/bash -eu
#
# USAGE: $0 [amd64|armhf|arm64]
#
# ref: https://docs.docker.com/engine/install/ubuntu/ 
# docker-compose version
DC_VERSION=1.27.4

#--------------------------------------
# Parameters
#--------------------------------------
ARCH=${1:-amd64}

case ${ARCH} in
  amd64 | armhf | arm64 ) ;;
  * ) echo "${ARCH} is invalid architecture!"
      echo "You must specified amd64 or armhf or arm64"
      exit 1
esac


#--------------------------------------
# Functions
#--------------------------------------
err_exit(){
  echo $1
  exit 1
}

#--------------------------------------
# Set up the repository
#--------------------------------------
# Update the apt package index and install packages

if !(type "docker" > /dev/null 2>&1); then
  # when not installed docker
  echo "#------------------------------------------------------------------"
  echo "# Start install docker"
  echo "#------------------------------------------------------------------"
  sudo apt-get update
  sudo apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg-agent \
      software-properties-common


  # Add Docker’s official GPG key
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo apt-key fingerprint 0EBFCD88 \
      | grep "9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88" \
      || err_exit "apt-key verify failed"

  # Use the following command to set up the stable repository
  sudo add-apt-repository \
      "deb [arch=${ARCH}] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) \
      stable"

  #--------------------------------------
  # Install Docker Engine
  #--------------------------------------
  # Install the latest version of Docker Engine and containerd
  sudo apt-get update
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io

  # Add user group docker
  sudo usermod -aG docker $USER
else
  echo "#------------------------------------------------------------------"
  echo "# Already installed docker, skip install process"
  echo "#------------------------------------------------------------------"
fi

#--------------------------------------
# Install Docker Compose
#--------------------------------------
if !(type "docker-compose" > /dev/null 2>&1); then
  echo "#------------------------------------------------------------------"
  echo "# Start install docker-compose"
  echo "#------------------------------------------------------------------"
  sudo curl -L "https://github.com/docker/compose/releases/download/${DC_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
else
  echo "#------------------------------------------------------------------"
  echo "# Already installed docker-compose, skip install process"
  echo "#------------------------------------------------------------------"
fi

