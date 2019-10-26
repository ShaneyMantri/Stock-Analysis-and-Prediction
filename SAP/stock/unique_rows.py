import csv
import pandas as pd
import os
import time

def read_unique_rows(company_name):
    DataCaptured = pd.read_csv(r"F:/Git/SAP/SAP/{}.csv".format(company_name))
    timer,openrate, high, low, closerate  = [],[],[],[],[]
    a = DataCaptured['timestamp']
    b = DataCaptured['open']
    c = DataCaptured['close']
    d = DataCaptured['high']
    e = DataCaptured['low']
    l = len(a)
    i = 0
    
    while i < l:
        if a[i] not in timer and a[i]!='timestamp':
            timer.append(a[i])
            openrate.append(b[i])
            closerate.append(c[i])
            high.append(d[i])
            low.append(e[i])
        i+=1
    timer = list(map(float, timer))
    openrate = list(map(float, openrate))
    closerate = list(map(float, closerate))
    high = list(map(float, high))
    low = list(map(float, low))
    timer = list(map(int,timer))
    timedet = []
    for x in timer:
        timedet.append(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))))
    # print(time[0],type(openrate[0]),type(closerate[0]),type(high[0]),type(low[0]))
    return timedet, openrate, closerate, high, low



# read_unique_rows("AAPL")