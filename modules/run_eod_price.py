import pandas as pd 
from mongo import DataManager
from price_data import GetPriceData
from time_handling import TimeManagement
from formatting import FormatData

"""
Tales all the tickers found in todays playbook and get 1m 5m and daily data on them

"""
#makes sure not to run on sat or sunday
if TimeManagement().day_of_week() not in [5,6]:
    print('Starting')
    date = TimeManagement().date_now()
    DM = DataManager()
    ## Time slices for price calls 
    time = TimeManagement()
    if TimeManagement().day_of_week() == 0:
        days = 3
    else:
        days = 1
    m1_timeslice = time.timeslice(days=days)
    m15_timeslice = time.timeslice(days=7)
    daily_timeslice = time.timeslice(years=1)
    print(f'Date {date},Timeslices = intraday:{m1_timeslice[0]} , {m1_timeslice[1]},  15m: {m15_timeslice[0]} , {m15_timeslice[1]} daily:{daily_timeslice[0]} , {daily_timeslice[1]}')
    ## Morning gappers 
    print('Loading gapper tickers from db')
    data_lists = DM.find_info('premarket_tickers',query_dict_gte={'dt':date},query_dict_lte={'shs_float':50000000})
    gapper_data = pd.DataFrame(data_lists)
    print('Loaded Gappers')
    try:
        tickers_gapper = gapper_data['ticker'].to_list()
        print(tickers_gapper)
        print(f'{len(tickers_gapper)}: Tickers loaded D1')
    except:
        print('No Tickers, data looks like',gapper_data)
    print('Getting Price data')
    for i in tickers_gapper:
        Price = GetPriceData(i)
        print("1m Run Attempt")
        m1_data = Price.get_data(timeframe='1m',daterange=m1_timeslice,premarket=True)
        print("5m Run Attempt")
        m5_data = Price.get_data(timeframe='5m',daterange=m1_timeslice,premarket=True)
        print("1d Run Attempt")
        daily_data = Price.get_data(timeframe='1d',daterange=daily_timeslice,premarket=False)
        print(f'Data for {i} collected Formatting it')
        m1_formatting = FormatData(m1_data).format_price_json()
        m5_formatting = FormatData(m5_data).format_price_json()
        daily_formatting = FormatData(daily_data).format_price_json()
        info_dict = {'dt':date,'setup':'premarket_gapper','ticker':i,'intraday_1m':m1_formatting,'intraday_5m':m5_formatting,'daily':daily_formatting}
        print(f'Data for {i} formatted, Storing it')
        DM.add_one(info_dict,'price_data')
    print('Finished Gappers')
    ## Morning Gappers D2
    print('Loading D2 Gappers from db')
    if TimeManagement().day_of_week() == 0:
        days = 3
    else:
        days = 1
    data_lists = DM.find_info('premarket_tickers',query_dict_gte={'dt':TimeManagement().date_days_ago(days=days)},query_dict_lte={})
    gappers_d2 = pd.DataFrame(data_lists)
    print('Loaded Gapper D2 plays')
    try:
        gap_ticker_D2 = gappers_d2['ticker'].to_list()
        print(gap_ticker_D2)
        print(f'{len(gap_ticker_D2)}: Tickers loaded D2')
    except:
        print('No Tickers data looks like',gappers_d2)
    print('Starting D2 Gapper price data run')
    for i in gap_ticker_D2:
        Price = GetPriceData(i)
        print("1m Run Attempt")
        m1_data = Price.get_data(timeframe='1m',daterange=m1_timeslice,premarket=False)
        print("5m Run Attempt")
        m5_data = Price.get_data(timeframe='5m',daterange=m1_timeslice,premarket=False)
        print("15m Run Attempt")
        m15_data = Price.get_data(timeframe='15m',daterange=m15_timeslice,premarket=False)
        print("1d Run Attempt")
        daily_data = Price.get_data(timeframe='1d',daterange=daily_timeslice,premarket=False)
        print(f'Data for {i} collected Formatting it')
        m1_formatting = FormatData(m1_data).format_price_json()
        m5_formatting = FormatData(m5_data).format_price_json()
        m15_formatting = FormatData(m15_data).format_price_json()
        daily_formatting = FormatData(daily_data).format_price_json()
        info_dict = {'dt':date,'setup':'gapper_D2','ticker':i,'intraday_1m':m1_formatting,'intraday_5m':m5_formatting,'intraday_15m':m15_formatting,'daily':daily_formatting}
        print(f'Data for {i} formatted, Storing it')
        DM.add_one(info_dict,'price_data')
    print('Finished D2 Gappers')
    """
    All this code commented out is for pulling D1 and D2 plays and getting price action which I am not doing currently
    """
    ##### D1
    # data_lists = DM.find_info('D1_plays',query_dict_gte={'dt':date},query_dict_lte={})
    # data1 = pd.DataFrame(data_lists)
    # print('Loaded D1 plays')
    # try:
    #     tickers_D1 = data1['ticker'].to_list()
    #     print(tickers_D1)
    #     print(f'{len(tickers_D1)}: Tickers loaded D1')
    # except:
    #     print('No Tickers data looks like',data1)
    # ###### D2
    # if TimeManagement().day_of_week() == 0:
    #     days = 3
    # else:
    #     days = 1
    # print(TimeManagement().date_days_ago(days=days))
    # data_lists = DM.find_info('D1_plays',query_dict_gte={'dt':TimeManagement().date_days_ago(days=days)},query_dict_lte={})
    # data2 = pd.DataFrame(data_lists)
    # print('Loaded D2 plays')
    # try:
    #     tickers_D2 = data2['ticker'].to_list()
    #     print(tickers_D2)
    #     print(f'{len(tickers_D2)}: Tickers loaded D2')
    # except:
    #     print('No Tickers data looks like',data2)
    # print('Getting Price data')
    # #########
    # time = TimeManagement()
    # m1_timeslice = time.timeslice(days=0)
    # m15_timeslice = time.timeslice(days=7)
    # daily_timeslice = time.timeslice(years=1)
    # print(f'Date {date},Timeslices = intraday:{m1_timeslice[0]} , {m1_timeslice[1]},  15m: {m15_timeslice[0]} , {m15_timeslice[1]} daily:{daily_timeslice[0]} , {daily_timeslice[1]}')
    # #### D1 
    # print('Starting D1 price data run')
    # for i in tickers_D1:
    #     Price = GetPriceData(i)
    #     print("1m Run Attempt")
    #     m1_data = Price.get_data(timeframe='1m',daterange=m1_timeslice,premarket=False)
    #     print("5m Run Attempt")
    #     m5_data = Price.get_data(timeframe='5m',daterange=m1_timeslice,premarket=False)
    #     print("1d Run Attempt")
    #     daily_data = Price.get_data(timeframe='1d',daterange=daily_timeslice,premarket=False)
    #     print(f'Data for {i} collected Formatting it')
    #     m1_formatting = FormatData(m1_data).format_price_json()
    #     m5_formatting = FormatData(m5_data).format_price_json()
    #     daily_formatting = FormatData(daily_data).format_price_json()
    #     info_dict = {'dt':date,'setup':'D1','ticker':i,'intraday_1m':m1_formatting,'intraday_5m':m5_formatting,'daily':daily_formatting}
    #     print(f'Data for {i} formatted, Storing it')
    #     DM.add_one(info_dict,'price_data')
    # #### D2 
    # print('Starting D2 price data run')
    # for i in tickers_D2:
    #     Price = GetPriceData(i)
    #     print("1m Run Attempt")
    #     m1_data = Price.get_data(timeframe='1m',daterange=m1_timeslice,premarket=False)
    #     print("5m Run Attempt")
    #     m5_data = Price.get_data(timeframe='5m',daterange=m1_timeslice,premarket=False)
    #     print("15m Run Attempt")
    #     m15_data = Price.get_data(timeframe='15m',daterange=m15_timeslice,premarket=False)
    #     print("1d Run Attempt")
    #     daily_data = Price.get_data(timeframe='1d',daterange=daily_timeslice,premarket=False)
    #     print(f'Data for {i} collected Formatting it')
    #     m1_formatting = FormatData(m1_data).format_price_json()
    #     m5_formatting = FormatData(m5_data).format_price_json()
    #     m15_formatting = FormatData(m15_data).format_price_json()
    #     daily_formatting = FormatData(daily_data).format_price_json()
    #     info_dict = {'dt':date,'setup':'D2','ticker':i,'intraday_1m':m1_formatting,'intraday_5m':m5_formatting,'intraday_15m':m15_formatting,'daily':daily_formatting}
    #     print(f'Data for {i} formatted, Storing it')
    #     DM.add_one(info_dict,'price_data')
    print('Success, Finished')
else: 
    print('Its the weekend, Go home')

