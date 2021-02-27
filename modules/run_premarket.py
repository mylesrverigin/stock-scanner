from pre_market import PreMarket
from mongo import DataManager
from time_handling import TimeManagement
from formatting import FormatData
from get_additional_info import RequestInfo



#makes sure not to run on sat or sunday
if TimeManagement().day_of_week() not in [5,6]:
    print('Starting Process')
    premarket = PreMarket()
    premarket.run(return_df=False)
    premarket_df = premarket.return_specifc_settings({'premarket_volume':30000},{'premarket_price':20})
    print('Data Aquired Attempting additional info get')
    Formatting = FormatData(premarket_df)
    db_dicts = Formatting.format_premarket()
    print('Adding To DB')
    dm = DataManager()
    dm.add_info(db_dicts,'premarket_tickers')
    print('Success')
else: 
    print('Its the weekend, Go home')