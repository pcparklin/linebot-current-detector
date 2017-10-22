#!/usr/bin/python3
# coding: utf-8

import RPi.GPIO as GPIO

GPIO_SENSOR = 7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(GPIO_SENSOR, GPIO.IN, GPIO.PUD_DOWN)

while True:
	print(GPIO.input(GPIO_SENSOR), end='\r')