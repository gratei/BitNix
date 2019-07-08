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

class nixie_markey(object):
    def __init__(self):
        global status
        status = 2
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(3,GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(4,GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(18,GPIO.OUT)
        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.switchpush, bouncetime=300)
        GPIO.add_event_detect(3, GPIO.FALLING, callback=self.reboot, bouncetime=10)
        GPIO.add_event_detect(4, GPIO.FALLING, callback=self.shutdown, bouncetime=10)
        GPIO.output(18,GPIO.LOW)
        #print("init kidou")


    def main(self):
        global status
        global ser
        ser = serial.Serial('/dev/serial0', 9600, timeout = 10)
        time.sleep(1)
        num = random.randint(0,99999999)
        iti = random.randint(0,9)
        sendticker = str(00000000).encode()
        try:
            while True:
                if status % 20 == 0: #BTC_FX mode
                    try:
                        for i in range(3):
                            ser.write(b"a")
                            ser.write(sendticker)
                            time.sleep(0.05)
                            ser.write(b"e")
                            ser.write(sendticker)
                            time.sleep(0.05)
                        getticker = requests.get('https://api.bitflyer.com/v1/getticker?product_code=FX_BTC_JPY').json()
                        ticker = int(getticker['ltp'])
                        now = datetime.datetime.now()
                        keta = str(ticker).zfill(8)
                        sendticker = keta.encode()
                        if now.minute % 5 == 0 and now.second == 0:
                            ser.write(b"b")
                            time.sleep(1)
                    except:
                        time.sleep(1)

                elif status % 20 ==1 : #random_number mode @ 10s
                    now = datetime.datetime.now()
                    sendvalue = (str(iti)+"."+str(num)).encode()
                    #sendvalue = ("0."+str(num)).encode()
                    ser.write(b"a")
                    ser.write(sendvalue)
                    time.sleep(0.05)
                    ser.write(b"e")
                    ser.write(sendvalue)
                    time.sleep(0.1)
                    if now.second %10== 0:
                        ser.write(b"b")
                        time.sleep(1)
                        num = random.randint(0,99999999)
                        iti = random.randint(0,9)
                elif status % 20 ==2 : #clock mode
                    now = datetime.datetime.now()
                    jikan = str(now.hour).zfill(2)
                    fun = str(now.minute).zfill(2)
                    byou = str(now.second).zfill(2)
                    nen = str(now.year%100)
                    tuki = str(now.month).zfill(2)
                    niti = str(now.day).zfill(2)
                    ima = (jikan +"."+ fun +"."+ byou).encode()
                    imadate = (nen +"."+tuki+"."+niti).encode()
                    ser.write(b"a")
                    ser.write(ima)
                    time.sleep(0.05)
                    ser.write(b"e")
                    ser.write(imadate)
                    time.sleep(0.1)
                    if now.minute % 5 == 0 and now.second == 0:
                        ser.write(b"b")
                        time.sleep(1)
                else:
                    status = 0

        except KeyboardInterrupt:
            GPIO.output(18,GPIO.HIGH)
            GPIO.cleanup()
            print("break")
            ser.close()

    def switchpush(self, channel):
        global status
        global ser
        ser.write(b"c")
        GPIO.output(18,GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(18,GPIO.LOW)
        status += 1

    def shutdown(self, channel):
        global ser
        ser.write(b"e")
        ser.close()
        GPIO.output(18,GPIO.HIGH)
        GPIO.cleanup()
        os.system("sudo shutdown -h now")
        sys.exit()
        time.sleep(3)
        #print("shutdown no tumori")

    def reboot(self, channel):
        global ser
        ser.close()
        GPIO.output(18,GPIO.HIGH)
        GPIO.cleanup()
        os.system("sudo reboot")
        sys.exit()
        time.sleep(3)
        #print("shutdown no tumori")

if __name__ == "__main__":
    nix = nixie_markey()
    #try:
    nix.main()
    #except KeyboardInterrupt:
    #    print("break")
