# V4L2NDI-Control

A front-end to run [v4l2ndi](https://github.com/lplassman/V4L2-to-NDI) on a single-board-computer, such as a Raspberry Pi, to connect USB or 
HDMI cameras to a NDI based video system

Provides a simple web interface (http: on port 80) for minimal control of the system (restart, reboot, shutdown)

## Hardware requirements

The default configuration of the program supports 1080p/30 when running on:
- ARM64 based SBC
- 4 cores, clock speed 1.5GHz or better (i.e. Raspberry Pi 4 or better)
- Gigabit Ethernet
- USB video device (webcam or HDMI capture) connected to USB 3.0

## Installation

This is intended to be installed on a dedicated Raspberry Pi, or a similar arm64 SBC (e.g. an OrangePi running Armbian) which will be used to adapt a USB video device (a webcam, or a USB HDMI capture device connected to a camera) to NDI.

The Quick Install procedure uses a pre-built (using pyinstaller) copy of the application. Alternatively you can close the repository and build your own copy.

The install script also installs the [Newtek NDI SDK](https://ndi.video/for-developers/ndi-sdk/) and the [v4l2ndi](https://github.com/lplassman/V4L2-to-NDI) application

The install script creates a new systemctl service 'v4l2ndi' which will run at system startup. It operates by finding the first USB video device and running *v4l2ndi* to advertise and stream the device to NDI. 

### Quick Install

```
git clone https://github.com/DanTappan/Pi-V4L2NDI-Control; cd Pi-V42NDI-Control
bash ./install.sh
```




