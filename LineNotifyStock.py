import requests as rs
import twstock
import schedule
import time
from datetime import datetime
import sys

def LinNotifyMessage(token,msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = rs.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code
    

if __name__ == "__main__":
    code = "2610"
    stock_price = float(twstock.realtime.get(code)["realtime"]["latest_trade_price"])
    name = twstock.realtime.get(code)["info"]["name"]
    target_price = 19

    token = "你的token"
    message = name + "現價:" + "%.2f"%stock_price

    schedule.every(20).seconds.do(LinNotifyMessage,token,message)

    open_time = 90000
    close_time = 133000
    now = int(datetime.now().strftime("%H%M%S"))

    while True:
        if(now > open_time and now < close_time):
            if(stock_price > target_price):
                schedule.run_pending()
                time.sleep(2)
            else:
                print("還沒到")
                time.sleep(2)
        else:
            sys.exit("收盤了")
        
