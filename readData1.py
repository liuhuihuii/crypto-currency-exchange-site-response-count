import bitmex
from time import sleep
import datetime
import requests
import json

client = bitmex.bitmex(test=False, api_key="your api key", api_secret="your api secret")

 
while 1:
    try:
        ##bitmex平台行情数据
        result=client.Instrument.Instrument_get(symbol='XBTUSD', reverse=True, count=1).result()
        ##huobi平台行情数据
        resp = requests.get('https://api.huobi.pro/market/detail/merged?symbol=btcusdt')
        while resp.status_code != 200:
            resp = requests.get('https://api.huobi.pro/market/detail/merged?symbol=btcusdt')
            sleep(1)
        resp1 = requests.get('https://api.huobi.pro/market/trade?symbol=btcusdt')
        while resp1.status_code != 200:
            resp1 = requests.get('https://api.huobi.pro/market/trade?symbol=btcusdt')
            sleep(1)
    except:
        continue
    time_tag = datetime.datetime.now()
    ##解析数据
    json_resp = json.loads(resp.text)
    json_resp1 = json.loads(resp1.text)
    #print('bidprice 日期:%s-- bitmex:%f--huobi: %f' % (time_tag,result[0][0].get('bidPrice'),json_resp.get('tick').get('bid')[0]))
    #print('askprice 日期:%s-- bitmex:%f--huobi: %f' % (time_tag,result[0][0].get('askPrice'),json_resp.get('tick').get('ask')[0]))
    print('marketprice 日期:%s-- bitmex:%f--huobi: %f' % (time_tag,result[0][0].get('lastPrice'),json_resp1.get('tick').get('data')[0].get('price')))

    print('=======================')
    sleep(1)
