#!/usr/bin/python3
# coding: utf-8

import os

from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_wtf.csrf import CsrfProtect

import RPi.GPIO as GPIO

from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


CHANNEL_ACCESS_TOKEN = ''
CHANNEL_SECRET = ''

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

app = Flask(__name__)
app.secret_key = os.urandom(24)
CsrfProtect(app)

GPIO_SENSOR = 7

@app.route('/_update_current', methods=['GET'])
def update_current():
    return jsonify({'current':GPIO.input(GPIO_SENSOR)})

@app.route('/send_alarm', methods=['POST'])
def send_alarm():
    info = {'current': GPIO.input(GPIO_SENSOR)}
    if request.form['alarm'] != '':
        try:
            line_bot_api.push_message(
                '', # ID of the recipient, not the ID shwon in LINE App
                TextSendMessage(text=request.form['alarm'])
            )
            return redirect(url_for('gpio', status='Succeed!'))
        except Exception:
            return redirect(url_for('gpio', status='Failed!'))
    else:
        return redirect(url_for('gpio'))

@app.route("/")
def gpio():
    return render_template('gpio.html', info={
        'current': GPIO.input(GPIO_SENSOR),
        'status': request.args.get('status')
    })

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_SENSOR, GPIO.IN, GPIO.PUD_DOWN)

    app.run(host='0.0.0.0', port=80, debug=True)