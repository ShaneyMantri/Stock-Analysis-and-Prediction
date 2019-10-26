import sys
import time
from datetime import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

matplotlib.use('TkAgg')


def get_price(symbol):
    my_share = share.Share(symbol)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                            200,
                                            share.FREQUENCY_TYPE_HOUR,
                                            1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    x = symbol_data['timestamp']
    newTime = [z / 1000 for z in x]
    datelist = []
    for x in newTime:
        datelist.append(str(time.strftime('%Y-%m-%d', time.localtime(x))))
    tempopenrate = symbol_data['open']
    openrate = [round(x,2) for x in tempopenrate]
    tempcloserate = symbol_data['close']
    closerate = [round(x,2) for x in tempopenrate]
    
    return datelist, openrate, closerate


def plotgraph(symbol):
    my_share = share.Share(symbol)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                            200,
                                            share.FREQUENCY_TYPE_DAY,
                                            1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    x = symbol_data['timestamp']
    newTime = [z / 1000 for z in x]
    datelist = []
    for x in newTime:
        datelist.append(str(time.strftime('%d/%m', time.localtime(x))))
    tempopenrate = symbol_data['open']
    openrate = [round(x,2) for x in tempopenrate]
    tempcloserate = symbol_data['close']
    closerate = [round(x,2) for x in tempopenrate]

    # print("DONE")
    # print(datelist[0],datelist[len(datelist)-1])
    len_date = len(datelist)
    len_date = len_date//10
    datelist_sent = []
    # print("DONE2")
    i = 0
    while i < len(datelist):
        datelist_sent.append(datelist[i])
        i = i+len_date
    # print("DONE3")
    # datelist_sent.append(datelist[len(datelist)-1])
    return datelist,openrate, datelist_sent, closerate


def lineear_regression(symbol):
    my_share = share.Share(symbol)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                            15,
                                            share.FREQUENCY_TYPE_DAY,
                                            1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    x = symbol_data['timestamp']
    newTime = [z / 1000 for z in x]
    datelist = []
    for x in newTime:
        datelist.append(str(time.strftime('%Y-%m-%d', time.localtime(x))))
    tempopenrate = symbol_data['open']
    openrate = [round(x,2) for x in tempopenrate]
    tempcloserate = symbol_data['close']
    closerate = [round(x,4) for x in tempopenrate]
    volume = symbol_data['volume']
    low = symbol_data['low']
    high = symbol_data['high']
    return datelist,openrate, closerate, low, high