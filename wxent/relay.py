#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import threading

#class relay(threading.Thread):
def relay(no):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(no,GPIO.OUT)
    GPIO.output(no,GPIO.LOW)
    time.sleep(5)
    GPIO.output(no,GPIO.HIGH)
