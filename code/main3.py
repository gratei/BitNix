import time
import serial
import json
import ast
import sys
import datetime
import random
import requests

def main():
    try:
        ser = serial.Serial('/dev/serial0', 9600, timeout = 10)
        time.sleep(1)
        while True:
            getticker = requests.get('https://api.bitflyer.com/v1/getticker?product_code=FX_BTC_JPY').json()
            ticker = int(getticker['ltp'])

            now = datetime.datetime.now()
            ser.write(b"a")
            ser.write(str(ticker).encode())
            time.sleep(0.2)
            if now.minute % 5 == 0 and now.second == 0:
                ser.write(b"b")
                time.sleep(1)
    except:
        time.sleep(10)
        main()

if __name__ == "__main__":
    main()
