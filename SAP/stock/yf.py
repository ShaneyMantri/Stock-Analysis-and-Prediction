import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import matplotlib.pyplot as plt 
import time

def Obtain_price(symbol):
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

    openrate = symbol_data['open']
    closerate = symbol_data['close']
    highest = symbol_data['high']
    lowest = symbol_data['low']
    # plt.scatter(newTime, y, label= "dots", color= "green",  marker= ".", s=30) 
    # plt.xlabel('Epoch Time')
    # plt.ylabel('Open Rate')

    # plt.title("Stock Price")
    # plt.legend() 
    # plt.show()
    # return [datelist[len(datelist)-1], y[len(y)-1]]
    return  openrate[len(openrate)-1], closerate[len(closerate)-1], highest[len(highest)-1], lowest[len(lowest)-1]






