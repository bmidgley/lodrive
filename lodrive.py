#!/usr/bin/env python3

# sudo apt install build-essential python3-dev python3-pip libhdf5-100 libcblas3 libatlas3-base libjasper1
# pip3 install "picamera[array]" opencv-contrib-python-headless luma.oled

import cv2
import io
import time
import math
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image
from luma.core.interface.serial import spi
from luma.oled.device import ssd1306

serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=24)
device = ssd1306(serial)

threshold = 200
orientations = 16
hist = np.empty([orientations], dtype=int)
cutoffs = np.empty([orientations])

for i in range(orientations):
    cutoffs[i] = ((i+1)/orientations)*(2*np.pi) - np.pi

def display(im):
    image = Image.fromarray(im).convert('1').transpose(Image.FLIP_LEFT_RIGHT)
    device.display(image)

def stats(dx, dy):
    if((abs(dx) + abs(dy)) > threshold):
        angle = math.atan2(dy, dx)
        for i in range(orientations):
            if(angle <= cutoffs[i]):
                hist[i] += 1
                return

def score(i):
    return hist[i] + hist[(i+7)%orientations]

def process(im):
    h, w, d = im.shape
    hist[:] = 0
    dx = cv2.Sobel(im, cv2.CV_16S, 1, 0)
    dy = cv2.Sobel(im, cv2.CV_16S, 0, 1)
    for i in range(0,w,4):
        for j in range(0,h,4):
            stats(dx[j][i][0], dy[j][i][0])
    print(hist)
    max = 0
    imax = 0
    for i in range(orientations):
        newscore = score(i)
        if newscore > max:
            max = newscore
            imax = i
    return imax, max
    
with PiCamera() as camera:
    camera.resolution = (128, 64)
    camera.start_preview()
    camera.color_effects = (128, 128)
    rawCapture = PiRGBArray(camera)
    while True:
        started_at = time.time()
        camera.capture(rawCapture, format='bgr')
        display(rawCapture.array)
        direction, speed = process(rawCapture.array)
        print(direction, speed)
        rawCapture.truncate(0)
        print(time.time() - started_at)

