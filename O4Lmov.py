from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
from talib import BBANDS
from talib import SMA
from datetime import datetime
import concurrent.futures
from discord import Webhook, RequestsWebhookAdapter
print("ONLY FOR LEGENDS SIGNALS || MV || 0.01_300_12")
account = input("Email :")
password = input("password :")
mood = input("Mood  :")
I_want_money = IQ_Option(account, password)
check = I_want_money.connect()
I_want_money.change_balance(mood)
I_want_money.get_server_timestamp()
now = datetime.now()
n = 1
j = 1
if check:
        print("####   CONNECT  SUCCEFULY    #####")
else:
        print("connect failed")
def send_msj(message):
    webhook = Webhook.from_url("https://discord.com/api/webhooks/989158059022618655/hgkfCPkxufy_j5xmUsBG76ZslDftZc1sAZlpwjSXckvcMdlLnLwylHGPcn0r1K6lQQ1X", adapter=RequestsWebhookAdapter())
    webhook.send(message)
send_msj("################  %s/%s/%s  ################ " % (now.day, now.month, now.year))
def bbands(goal):
    print(f"##connect to {goal}")
    size = 300
    maxdict = 200
    I_want_money.start_candles_stream(goal, size, maxdict)
    while True:
        time.sleep(0.25)
        candles = I_want_money.get_realtime_candles(goal, size)
        inputs = {
            'open': np.array([]),
            'close': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
        }
        for timestamp in list(candles.keys()):
            open = inputs["open"] = np.append(inputs["open"], candles[timestamp]["open"])
            close = inputs["close"] = np.append(inputs["open"], candles[timestamp]["close"])
            high = inputs["high"] = np.append(inputs["open"], candles[timestamp]["max"])
            low = inputs["low"] = np.append(inputs["open"], candles[timestamp]["min"])
        real_20 = SMA(close, timeperiod=20)
        real_50 = SMA(close, timeperiod=50)
        cls = close[-1] * 10000000000000
        rl20 = real_20[-1] * 10000000000000
        rl50 = real_50[-1] * 10000000000000
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S:")   
        if rl20 < rl50 and n == 1 :
                send_msj(f"## Sell MV {goal} ##{current_time} ")
                print(f"# sell {goal}||| Close : {cls} ||| {current_time}||| MV20 : {rl20} || MV_200 : {rl50}")
                time.sleep(size)
                n = 0
                j += 1
                continue
        if rl20 > rl50 and j == 1:
                send_msj(f"## Buy MV {goal} ##{current_time}")
                print(f"# buy {goal}||| Close : {cls} ||| {current_time}||| MV20 : {rl20} || MV_200 : {rl50}")
                time.sleep(size)
                j = 0
                n += 1
                continue
        if now.strftime("%S") == "00" :
            print(f"# {goal}||| Close : {cls} ||| {current_time}||| MV20 : {rl20} || MV_200 : {rl50}")

with concurrent.futures.ThreadPoolExecutor () as executor :
    goals = ["EURUSD", "USDJPY", "AUDUSD", "GBPUSD", "EURJPY", "EURGBP", "AUDCAD", "GBPJPY", "AUDJPY",
             "CADJPY", "USDCAD", "EURAUD"]
    results = [executor.submit(bbands, goal) for goal in goals]