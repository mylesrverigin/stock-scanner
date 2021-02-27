import pandas as pd 
from time_handling import TimeManagement
from post_market import PostMarketScrape
from mongo import DataManager
from formatting import FormatData

"""
Takes a scrape from finviz and saves all the tickers for later use 
and data analysis
"""
base_address = 'https://finviz.com/screener.ashx?v=151&f=cap_microover,sh_avgvol_o300,sh_price_u50,sh_relvol_o2,ta_averagetruerange_o0.5,ta_gap_u3&ft=4&c=1,2,3,4,5,6,24,25,26,28,30,49,60,61,63,64,65,66,67,68'
html_tag = 'tr'
html_element_dict = {'class':['table-light-row-cp','table-dark-row-cp']}
regex_pattern = r">(?![<\s])(-?\w*.?\w*%?.?\d*)\S"
df_col_names = ['ticker','company_name','sector','industry','country',
                    'market_cap','shares_outstanding','float','insider_own','inst_own','float_short',
                    'atr','change_from_open','gap_size','avg_vol','rel_vol','price','change_total','volume','earnings']

if TimeManagement().day_of_week() not in [5,6]:
    scrape = PostMarketScrape(base_address,html_tag,html_element_dict,regex_pattern,df_col_names)
    scrape.run(up=True)
    gap_up = scrape.return_df()
    scrape.run(up=False)
    gap_down = scrape.return_df()
    combined = gap_up.append(gap_down,ignore_index=True)
    ### D1 
    combined['setup'] = 'D1'
    formatting = FormatData(combined)
    final_dict_d1 = formatting.format_ticker_scan()
    print('Adding To DB')
    DM = DataManager()
    DM.add_info(final_dict_d1,'D1_plays')
    print('Success')
else: 
    print('Its the weekend, Go home')