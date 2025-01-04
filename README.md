# V4L2NDI-Control

A front-end to run [v4l2ndi](https://github.com/lplassman/V4L2-to-NDI) on a single-board-computer, such as a Raspberry Pi, to connect USB or 
HDMI cameras to a NDI based video system

Provides a simple web interface for minimal control of the system (restart, reboot, shutdown)

## Installation

This is intended to be installed on a dedicated Raspberry Pi, or a similar arm64 SBC (e.g. an OrangePi running Armbian) which will be used to adapt a USB video device (a webcam, or a USB HDMI capture device connected to a camera) ro NDI.

The Quick Install procedure uses a pre-built (using pyinstaller) copy of the application. Alternatively you can close the repository and build your own copy.

The install script also installs the [Newtek NDI SDK](https://ndi.video/for-developers/ndi-sdk/) and the [v4l2ndi](https://github.com/lplassman/V4L2-to-NDI) application

### Quick Install

```
git clone https://github.com/DanTappan/Pi-V4L2NDI-Control; cd Pi-V42NDI-Control
./install.sh
```




