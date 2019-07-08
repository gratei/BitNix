import time
import serial
import json
import ast
import sys
import datetime
import random
import requests
import os

import RPi.GPIO as GPIO

status = 0

def main():
    global status
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4,GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(21,GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=switchpush, bouncetime=300)
    GPIO.add_event_detect(21, GPIO.FALLING, callback=shutdown, bouncetime=300)
    ser = serial.Serial('/dev/serial0', 9600, timeout = 10)
    time.sleep(1)
    num = random.randint(0,999999)
    try:
        while True:
            if status % 20 == 0: #BTC_FX mode
                getticker = requests.get('https://api.bitflyer.com/v1/getticker?product_code=FX_BTC_JPY').json()
                ticker = int(getticker['ltp'])
                now = datetime.datetime.now()
                sendticker = str(ticker).encode()
                ser.write(b"a")
                ser.write(sendticker)
                time.sleep(0.4)
                if now.minute % 5 == 0 and now.second == 0:
                    ser.write(b"b")
                    time.sleep(1)
            elif status % 20 ==1 : #random_number mode @ 10s
                now = datetime.datetime.now()
                sendvalue = str(num).encode()
                ser.write(b"a")
                ser.write(sendvalue)
                time.sleep(0.5)
                if now.second %10== 0:
                    ser.write(b"b")
                    time.sleep(1)
                    num = random.randint(0,999999)
            elif status % 20 ==2 : #clock mode
                now = datetime.datetime.now()
                jikan = str(now.hour).zfill(2)
                fun = str(now.minute).zfill(2)
                byou = str(now.second).zfill(2)
                ima = (jikan + fun + byou).encode()
                ser.write(b"a")
                ser.write(ima)
                time.sleep(0.1)
                if now.minute % 5 == 0 and now.second == 0:
                    ser.write(b"b")
                    time.sleep(1)
            else:
                status = 0

    except KeyboardInterrupt:
        print("break")
        ser.close()

def switchpush(channel):
    global status
    status += 1

def shutdown(channel):
    os.system("sudo shutdown -h now")

if __name__ == "__main__":
    main()
