import time
import serial
import json
import ast
import sys
import datetime
import random
import requests

def main():
    ser = serial.Serial('/dev/serial0', 9600, timeout = 10)
    time.sleep(1)
    while True:
        getticker = requests.get('https://api.bitflyer.com/v1/getticker?product_code=FX_BTC_JPY').json()
        ticker = int(getticker['ltp'])
        print(ticker)
        now = datetime.datetime.now()
        sendticker = str(ticker).encode()
        ser.write(b"a")
        ser.write(sendticker)
        time.sleep(0.2)
        if now.minute % 5 == 0 and now.second == 0:
            ser.write(b"b")
            time.sleep(1)
    ser.close()

if __name__ == "__main__":
    main()
