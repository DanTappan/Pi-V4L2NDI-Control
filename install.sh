# /usr/bin/env bash
#
# Install v4l2ndi package on a Raspberry Pi

# In case we are updating: shut down the running version
sudo systemctl stop v4l2ndi

# Prerequisites
sudo apt update -y && sudo apt upgrade -y
sudo apt-get install v4l-utils

# Run lplassman script to install v4l2ndi
# for now, use my fork of the code
(
sudo rm -f /usr/bin/v4l2ndi
git clone https://github.com/DanTappan/V4L2-to-NDI.git
cd V4L2-to-NDI
sudo bash ./easy-install-rpi-aarch64.sh
)

#
# if you want to be appropriately paranoid, run pyinstaller on Pu-V42NDI-Control.spec
# to make sure that the executable matches the sources before running this script
#
sudo mkdir -p /etc/v4l2ndi
sudo cp dist/V4L2NDI-Control /etc/v4l2ndi
sudo chmod +x /etc/v4l2ndi/V4L2NDI-Control

# install run script. This is a separate shell script to make it easier to change
# parameters
sudo cp run_v4l2ndi /etc/v4l2ndi
sudo chmod +x /etc/v4l2ndi/run_v4l2ndi

sudo cp v4l2ndi.service /etc/systemd/system
sudo systemctl enable v4l2ndi
sudo systemctl start v4l2ndi


