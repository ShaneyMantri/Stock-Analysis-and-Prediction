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
    
    lastest_open_rate = openrate[len(openrate)-1]
    latest_close_rate =  closerate[len(closerate)-1]
    highest_price_for_today = highest[len(highest)-1]
    lowest_price_for_today = lowest[len(lowest)-1]

    return  lastest_open_rate, latest_close_rate, highest_price_for_today, lowest_price_for_today






