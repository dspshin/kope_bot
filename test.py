#-*- coding: utf-8 -*-
from upbitpy import Upbitpy
import requests
from forex_python.converter import CurrencyRates

#logging.basicConfig(level=logging.DEBUG)
upbitpy = Upbitpy()
c = CurrencyRates()

def get_kope(coinName="BTC"):
  ticker = upbitpy.get_ticker(['KRW-'+coinName.upper()])
  btckrw_upbit = float( ticker[0]['trade_price'] )
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

  return kope

get_kope("btc")
#get_kope("eth")
#get_kope("xrp")
#get_kope("eos")
#get_kope("trx")
#get_kope("xlm")
#get_kope("snt")
get_kope("neo")


