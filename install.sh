# /usr/bin/env bash
#
# Install v4l2ndi package on a Raspberry Pi
#

# Prerequisites
sudo apt update -y && sudo apt upgrade -y

git clone https://github.com/lplassman/V4L2-to-NDI.git
(cd V4L2-to-NDI

sudo bash ./easy-install-rpi-aarch64.sh
)

if [ ! -d /etc/v4l2ndi ]; then
    sudo mkdir /etc/v4l2ndi
fi

sudo cp dist/V4L2NDI-Control /etc/v4l2ndi
sudo chmod +x /etc/v4l2ndi/V4L2NDI-Control

sudo cp v4l2ndi.service /etc/systemd/system
sudo systemctl enable v4l2ndi
sudo systemctl start v4l2ndi


