#-*- coding: utf-8 -*-
import requests
from forex_python.converter import CurrencyRates

#logging.basicConfig(level=logging.DEBUG)

def get_upbit_price(coinName):
  headers = {
      'User-Agent': 'kope bot v1.0',
  }
  r = requests.get(url="https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT."+coinName, headers=headers)
  print r
  a = r.json()
  c = a[0]
  return c["tradePrice"]

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

  return kope

get_kope("btc")
#get_kope("eth")
#get_kope("xrp")
#get_kope("eos")
#get_kope("trx")
#get_kope("xlm")
#get_kope("snt")
#get_kope("neo")


