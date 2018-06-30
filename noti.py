#!/usr/bin/python
# coding=utf-8
import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus
import re
from datetime import date, datetime, timedelta
import traceback

import requests
from forex_python.converter import CurrencyRates


#logging.basicConfig(level=logging.DEBUG)
c = CurrencyRates()

#ROOT = '/root/git/.../'
ROOT = "./"

#텔레그램 상으로는 4096까지 지원함. 가독성상 1000정도로 끊자.
MAX_MSG_LENGTH = 1000

def sendMessage(user,msg):
    try:
        bot.sendMessage(user,msg)
    except:
        traceback.print_exc(file=sys.stdout)

def get_upbit_price(coinName):
    headers = {
      'User-Agent': 'kope bot v1.0',
    }
    r = requests.get(url="https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT."+coinName, headers=headers)
    #print r
    a = r.json()[0]
    return a["tradePrice"]

def get_kope(coinName="BTC"):
    ticker = get_upbit_price('KRW-'+coinName.upper())
    btckrw_upbit = float( ticker )
    print( 'upbit',coinName,'krw :', btckrw_upbit )

    r = requests.get(url='https://api.bitfinex.com/v1/ticker/'+coinName.lower()+'usd')
    btcusd = float( r.json()['last_price'] )

    print( 'bitfinex',coinName,'usd :', btcusd )

    usdkrw = float( c.get_rate('USD', 'KRW') )
    print( 'usdkrw :', usdkrw )

    btckrw_bitfinex = btcusd * usdkrw
    print( 'bitfinex',coinName,'krw :' , btckrw_bitfinex )

    kope = (btckrw_upbit / btckrw_bitfinex) - 1
    print( coinName,'kope :', kope )

    return kope, btckrw_upbit

def getCoinData():
    coins = [
        "btc",
        "eth",
        "xrp",
        "eos",
        "trx",
        "xlm",
        "snt",
        "neo"
    ];
    res = []
    for coin in coins:
        kope, price = get_kope(coin)
        kope = str(kope)[:5]
        res.append( coin.upper() + " : "+kope+" ("+str(price)+")" )
    return res

def runNoti():
    conn = sqlite3.connect(ROOT+'user.db')
    c = conn.cursor()
    c.execute('SELECT user from user') # get all comamnds
    for data in c.fetchall():
        filter_param=None
        user = data[0].encode('utf-8')

        res_list = getCoinData()
        msg = ''
        for r in res_list:
            print str(datetime.now()).split('.')[0], r
            if len(r+msg)+1>MAX_MSG_LENGTH:
                sendMessage( user, msg )
                msg = r+'\n'
            else:
                msg += r+'\n'
        if msg:
            sendMessage( user, msg )


today = date.today()
TOKEN = sys.argv[1]
print '[',today,']received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

runNoti()
