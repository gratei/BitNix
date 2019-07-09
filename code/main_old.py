
import RealtimeAPI as RTAPI1

import threading
import time
import serial
import json
import ast
import sys
import datetime
import random

getticker = ""
getboard = ""
getexecutions = ""

def realtimeTicker(): #リアルタイムAPIを用いてTickerの最新情報を取得
    while True:
        url = 'wss://ws.lightstream.bitflyer.com/json-rpc'
        tickerurl = 'lightning_ticker_FX_BTC_JPY'
        channel = tickerurl
        realTicker = RTAPI1.RealtimeAPI(url=url, channel=channel)
        realTicker.run()
        time.sleep(10)

def dispticker(): #realtimeTickerで取得した最新情報をグローバル変数gettickerに格納
    global getticker
    maeticker = {'channel': 'lightning_ticker_FX_BTC_JPY', 'message': {'product_code': 'FX_BTC_JPY', 'timestamp': '2019-01-10T12:19:25.8426304Z', 'tick_id': 64804420, 'best_bid':409909, 'best_ask': 409925, 'best_bid_size': 0.38, 'best_ask_size': 0.14, 'total_bid_depth': 11403.18951766, 'total_ask_depth': 10453.35219681, 'ltp': 409909, 'volume': 366319.37355456, 'volume_by_product': 366319.37355456}}
    while True:
        getticker = RTAPI1.nowticker
        if getticker['message']['ltp'] != maeticker['message']['ltp']:
            maeticker = getticker
        time.sleep(0.01)

def sendToArduino():
    global getticker
    ser = serial.Serial('COM4', 9600)
    time.sleep(3)
    while True:
        now = datetime.datetime.now()
        sendValue = getticker['message']['ltp']
        ser.write(b"a")
        ser.write(str(sendValue).encode())
        time.sleep(0.1)
        if now.minute % 5 == 0 and now.second == 0:
            for i in range(20):
                num = random.randint(0,999999)
                ser.write(b"a")
                ser.write(str(num).encode())
                time.sleep(0.1)

def main():
    global getticker
    global getboard
    global getexecutions

    thread_1 = threading.Thread(target=realtimeTicker)
    thread_2 = threading.Thread(target=dispticker)
    thread_3 = threading.Thread(target=sendToArduino)


    thread_1.start()
    time.sleep(2)  #通信がはじまってから値をとってくるようにする
    #thread_4.start()
    thread_2.start()
    thread_3.start()
    #mySQLaccesstest()

if __name__ == "__main__":
    main()
