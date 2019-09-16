import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import matplotlib.pyplot as plt 
import time

def get_price(symbol):
    my_share = share.Share(symbol)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                            50,
                                            share.FREQUENCY_TYPE_HOUR,
                                            1)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    x = symbol_data['timestamp']
    newTime = [z / 1000 for z in x]
    datelist = []
    for x in newTime:
        datelist.append(str(time.strftime('%d-%m-%Y', time.localtime(x))))
    tempopenrate = symbol_data['open']
    openrate = [round(x,2) for x in tempopenrate]


    # plt.scatter(newTime, y, label= "dots", color= "green",  marker= ".", s=30) 
    # plt.xlabel('Epoch Time')
    # plt.ylabel('Open Rate')

    # plt.title("Stock Price")
    # plt.legend() 
    # plt.show()
    return datelist, openrate



