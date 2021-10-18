import time
import pyupbit
import datetime
import pandas
import json
import random

access = "ijIweUiME7MzHCxfAC5xHYjozoDLShwyUqpsH40X"
secret = "cJunnXFjjTuttfOwtoPeW09bRlETyZBTgFea2Kxn"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("가쥬아")

coinArray = pyupbit.get_tickers(fiat="KRW")
coinArray = random.shuffle(coinArray)
count = 0


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time



def search() :
    global count
   
    try :
        count +=1
        coinArray = pyupbit.get_tickers(fiat="KRW")
        coinArray = list(reversed(coinArray))
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        buy_time = start_time + datetime.timedelta(days=1)

        if start_time < now < buy_time :
            for i in coinArray :
            
                df = pyupbit.get_ohlcv(i, "minute1", count=2)
                #df = pyupbit.get_ohlcv(i, "minute1")
                curClose = float(df.iloc[0]['close'])
                
                Price = pyupbit.get_current_price(i)
                
                print()
                print("***  "+ i + "   ***")
                print('전분봉 종가/현재가' + str(curClose) + '/' + str(Price))                

                if curClose*1.02 < float(Price) :
                    print("!!!!!!!급등코인!!!!!!!!")
                    return i
                    break

    except :
        print("다시조회합니다. {} 회 반복중".format(count))
        time.sleep(1)
        search()           
         
    




while True:                                  # 급등코인 매수
    try:
        i = search()                         # 급등코인 결정
        krw = upbit.get_balance("KRW")
        upbit.buy_market_order(i, krw*0.9995)
        print("<<<< " + str(i) + " 구매완료 >>>>")
        
        # 결제 금액 
        firstPrice = pyupbit.get_current_price(i)
        print("구매금액 : " + str(firstPrice))
        
        while True :
            now = datetime.datetime.now()
            start_time = get_start_time("KRW-BTC")
            sell_time = start_time + datetime.timedelta(seconds=15)
            #df1 = pyupbit.get_ohlcv(i, interval="minute1", count=1)
            df1 = pyupbit.get_ohlcv(i, "minute1")
                       
            curPrice = pyupbit.get_current_price(i)
            
            # 09:00:20이후 일괄매도
            if  sell_time < now and ((firstPrice *1.01 < curPrice) or (firstPrice *0.97 > curPrice)) :
                useCoin = upbit.get_balance(i)
                upbit.sell_market_order(i, useCoin)
                print("<<<< " + str(i) + " 판매완료 >>>>")
                time.sleep(5)
                print("현재 보유 KRW : " + str(upbit.get_balance("KRW")))
                break
                
            else : time.sleep(2)
        
        print('판매코인 현재가 : ' + str(pyupbit.get_current_price(i)))
        time.sleep(900)
        
    except Exception as e:
        print(e)
        time.sleep(1)