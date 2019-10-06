import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import time
import csv

def Obtain_price(company_symbol):
    my_share = share.Share(company_symbol)
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
    
    del symbol_data['volume']
    
    symbol_data['timestamp'] = newTime
    save_output(symbol_data, "{}.csv".format(company_symbol))
    
    openrate = symbol_data['open']
    closerate = symbol_data['close']
    highest = symbol_data['high']
    lowest = symbol_data['low']
    
    lastest_open_rate = openrate[len(openrate)-1]
    latest_close_rate =  closerate[len(closerate)-1]
    highest_price_for_today = highest[len(highest)-1]
    lowest_price_for_today = lowest[len(lowest)-1]


    return  lastest_open_rate, latest_close_rate, highest_price_for_today, lowest_price_for_today


def save_output(mydict, output_file_name):
    with open(output_file_name,'a',newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(mydict.keys())
        writer.writerows(zip(*mydict.values()))




