#! /usr/bin/env python3
#
# Control program for V4L2NDI
# Loop:
# - find usb video devices
# - run v4l2ndi as a subprocess to translate video to NDU
# - run a separate browser thread for configuration and control
#
# this must run as root, in order to be able to use 'nice' and 'shutdown'
#
#
from wsgiref.simple_server import make_server
import multipart
import io
import os
import time
import re
import threading
import subprocess
from linuxpy.video.device import Device
import data_files

if os.getuid() == 0:
    listensocket = 80
else:
    listensocket = 8000

v4l2ndi = "/usr/bin/v4l2ndi"

def reboot (reboot_flag=True):
    """ try to reboot the system """
    if reboot_flag:
        flag = "-r"
    else:
        flag = "-h"

    args = [
             "/usr/sbin/shutdown",
             flag,
             "now"
    ]
    try:
        subprocess.run(args)
    except FileNotFoundError:
        pass

def shutdown ():
    """ try to shut down the system """
    reboot(False)


def schedule_task(action, delay):
    """ thread task to perform scheduled work """
    time.sleep(delay)
    action()


def schedule(action, delay=2):
    """ schedule an action to occur after a delay"""
    threading.Thread(target=(lambda: schedule_task(action, delay))).start()


def webpage(msg=None):
    """ return the HTML body of a webpage. "
        msg" is an optional text to insert
    """
    try:
        with open(data_files.html_index) as f,  io.BytesIO(b'') as of:
            for line in f:
                m = re.search("!MSG!", line)
                if m is not None:
                    if msg is not None:
                        of.write(bytes('<p>', "utf-8"))
                        of.write(bytes(msg, "utf-8"))
                        of.write(bytes('<br><p>', "utf-8"))
                else:
                    of.write(bytes(line, "utf-8"))
            return of.getvalue()

    except FileNotFoundError:
        return None


def handle_form(form):
    """ handle a form """

    if form.get("Restart"):
        v4l2ndi_kill()
        body = webpage("Restarting V4L2NDI")

    elif form.get("Reboot"):
        schedule(reboot)
        body = webpage("Rebooting")

    elif form.get("Shutdown"):
        schedule(shutdown)
        body = webpage("Shutting down")
    else:
        body = webpage("Unexpected action")

    return body

def my_web_app(environ, start_response):
    status = '200 OK'

    if environ['REQUEST_METHOD'] == 'GET':
        body = webpage()
    elif multipart.is_form_request(environ):
        forms, files = multipart.parse_form_data(environ)
        body = handle_form(forms)
    else:
        body = None

    if body is None:
        status = "404 not found"
        body = bytes("<html><body><p>internal error</p></body></html>", 'utf-8')

    headers = [('Content-Type', 'text/html'),
               ('Content-Length', str(len(body)))]
    start_response(status, headers)
    return [body]

#
#
def find_device():
    """ Find a USB Video device to forward
        returns Device or None"""
    num = 0
    while True:
        dev = Device.from_id(num)
        try:
            dev.open()
        except FileNotFoundError:
            return None
        driver = dev.info.driver
        dev.close()
        if driver == "uvcvideo":
            return dev.filename
        num = num + 1

v4l2ndi_terminate_process = False

def v4l2ndi_kill():
    global v4l2ndi_terminate_process

    v4l2ndi_terminate_process = True

def run_v4l2ndi():
    while True:
        device = find_device()
        if device is None:
            time.sleep(10)
            continue

        # nice the process to a higher priority to get closer to
        # realtime performance
        args = [
                "/usr/bin/nice", "--19",
                v4l2ndi, "-d", device, "-i", "-f"
        ]
        popen = subprocess.Popen(args)
        return popen

#
# Periodically clean up dead children
#
v4l2ndi_thread_exit = False

def v4l2ndi_thread():
    global v4l2ndi_terminate_process, v4l2ndi_thread_exit

    while True:
        v4l2ndi_terminate_process = False
        popen = run_v4l2ndi()

        if popen is None:
            time.sleep(10)
        else:
            while popen.returncode is None:
                try:
                    popen.wait(2)
                except (subprocess.TimeoutExpired, KeyboardInterrupt):
                    pass
                finally:
                    if v4l2ndi_terminate_process:
                        popen.terminate()
                        v4l2ndi_terminate_process = False

                    if v4l2ndi_thread_exit:
                        return
                pass
        
if __name__ == '__main__' :

    threading.Thread(target=v4l2ndi_thread).start()

    try:
        print(f"webserver listening on port {listensocket}")
        with make_server('', listensocket, my_web_app) as httpd:
            httpd.serve_forever()

    except KeyboardInterrupt:
        v4l2ndi_kill()
        v4l2ndi_thread_exit = True
