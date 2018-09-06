
'''
14家交易所(去除Fcoin)order_book(BTCUSDT为例)行情系统获取,汇总response time(max avg),row_counts指标
Author by liuhuihui
since 2018-08-28
'''
import requests
import json
import datetime

 
#交易对以BTCUSDT为例，后面要考虑统一表示各大交易所币对？？
symbol_pair='BTCUSDT'  ##以币安的交易对为蓝本
#重复测试次数,可以设置
repeat_times = 200
repeat_times_helper = 200   ##与上一变量保持一致

##全局常量
binance_depth_url ='https://api.binance.com/api/v1/depth?symbol='+symbol_pair
okex_depth_url='https://www.okex.com/api/v1/depth.do?symbol=btc_usdt'
bithumb_depth_url='https://api.bithumb.com/public/orderbook/BTC'  #KRW计价
bitfinex_depth_url='https://api.bitfinex.com/v2/book/tBTCUSD/P0'
hitbtc_depth_url='https://api.hitbtc.com/api/2/public/orderbook/BTCUSD'

kraken_depth_url='https://api.kraken.com/0/public/Depth?pair=XXBTZUSD'
bibox_depth_url='https://api.bibox.com/v1/mdata?cmd=depth&pair=BTC_USDT'
bittrex_depth_url='https://bittrex.com/api/v1.1/public/getorderbook?market=USDT-BTC&type=both'
zb_depth_url='http://api.zb.cn/data/v1/depth?market=btc_usdt'
gateio_depth_url='https://data.gateio.io/api2/1/orderBook/btc_usdt'

bitz_depth_url='https://apiv2.bitz.com/Market/depth?symbol=btc_usdt'
bitstamp_depth_url='https://www.bitstamp.net/api/v2/order_book/btcusd/'
bigone_depth_url='https://big.one/api/v2/markets/BTC-USDT/depth'
huobi_depth_url='https://api.huobi.pro/market/depth?symbol=btcusdt&type=step1'


##请求函数
def request_get(url):
    r = requests.get(url)
    return json.loads(r.text)

##测试函数
def test_response(ex_depth_url):
    global repeat_times,repeat_times_helper
    
    time_list = []
    while repeat_times>0:
        repeat_times = repeat_times - 1
        d1 =datetime.datetime.now()
        try:
            result=request_get(ex_depth_url)
        except:
            pass
        d2 = datetime.datetime.now()
        d3 = (d2-d1).microseconds / 1000
        time_list.append(d3)
    #total_milliseconds
    used_time=0
    for i in time_list:
        used_time=used_time+ i    
    ###特征变量 
    ex_name = ex_depth_url.split('.',2)[1] 
    avg_response_time = used_time / repeat_times_helper                             ##平均响应时间
    max_response_time = max(time_list)                                               ##单次响应最大时间
    if ex_name == 'binance' or ex_name =='okex' or ex_name=='zb' or ex_name=='gateio' or ex_name=='bitstamp':
        row_counts = len(result.get('bids'))         ##深度列表
    elif ex_name =='bithumb' or ex_name=='bitz':
        row_counts = len(result.get('data').get('bids'))
    elif ex_name =='bitfinex':
        row_counts=25
    elif ex_name =='hitbtc':
        row_counts= len(result.get('bid'))
    elif ex_name =='kraken':
        row_counts= len(result.get('result').get('XXBTZUSD').get('bids'))
    elif ex_name =='bibox':
        row_counts= len(result.get('result').get('bids'))
    elif ex_name=='com/api/v1':#bittrex
        ex_name='bittrex'
        row_counts= len(result.get('result').get('buy'))
    elif ex_name=='one/api/v2/markets/BTC-USDT/depth':#bigone
        ex_name='bigone'
        row_counts = len(result.get('data').get('bids'))
    elif ex_name=='huobi':
        row_counts = len(result.get('tick').get('bids'))
        
    ##文件输出
    f = open('order_book_response.txt','a+')
    print('交易所%s , Response time:max=%.2f(ms),avg=%.2f(ms),testTimes=%d,rowCounts=%d'%(ex_name,max_response_time,avg_response_time,repeat_times_helper,row_counts),file=f)
    f.close()



if __name__ == '__main__':
    print('start!')
    #test_response(okex_depth_url)
    
    ##url列表集合
    list_depth_url=[okex_depth_url,binance_depth_url,bithumb_depth_url,bitfinex_depth_url,hitbtc_depth_url,
                    kraken_depth_url,bibox_depth_url,bittrex_depth_url,zb_depth_url,gateio_depth_url,
                    bitz_depth_url,bitstamp_depth_url,bigone_depth_url,huobi_depth_url]

    for i in list_depth_url:
       repeat_times = 200    ##与第一次repeat_times相同
       test_response(i) 
    
    
     
    print('Done!')
     


