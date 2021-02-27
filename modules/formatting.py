import pandas as pd
import re
import json
from time_handling import TimeManagement
from get_additional_info import RequestInfo

class FormatData():
    def __init__(self,df):
        self.data = df

    def format_premarket(self):
        """
        Gets tickers ready for mongo, adds timestamp 
        Need to make sure column names of what is scraped are what is hardcoded in this classes methods or we have problems with self.volumefactor and self.tagentry
        """
        print('Starting Formatting')
        self.add_timestamps()
        self.get_facts(self.data['ticker'])
        self.merge_on_tickers()
        self.merged = self.volume_factor()
        self.merged = self.tag_entry('premarket')
        print('Attempting Cleaning')
        self.merged = CleanColumns(self.merged).clean()
        print("Ending Formatting")
        return self.format_for_db(self.merged)

    def format_ticker_scan(self):
        print('Starting Formatting')
        self.add_timestamps()
        print('Attempting Cleaning')
        self.data = CleanColumns(self.data).clean()
        print("Ending Formatting")
        return self.format_for_db(self.data)

    def add_timestamps(self):
        df = self.data
        """
        Creates the dt column and the process time column with current time
        """
        Time = TimeManagement()
        df.loc[:,'dt'] = Time.date_now()
        df.loc[:,'process_time'] = Time.date_time_now()
        self.data = df

    def filter_premarket(self,price=1,change_up=3,change_down=-3,vol=50000):
        """
        Uses pandas boolean filtering to narrow our search down to a few tickers 
        """
        print("Filtering Premarket Scrape Results Down")
        df = self.data
        price_filter = df['premarket_price'].astype(float) >= price
        gap_up_filter = df['premarket_change'].astype(float) >= change_up
        gap_down_filter = df['premarket_change'].astype(float) <= change_down
        vol_filter = df['premarket_vol'].astype(float) >= vol
        filtered_df = df[price_filter & vol_filter & (gap_up_filter | gap_down_filter)]
        self.data = filtered_df 

    def get_facts(self,list_of_tickers):
        """
        Gets the finviz stats for each ticker in the list_of_tickers 
        """
        print("Getting Additional Ticker info")
        info = RequestInfo(series_of_tickers=list_of_tickers)
        info.run()
        returned_data = info.dump_return()
        self.ticker_info = returned_data

    def merge_on_tickers(self):
        try:
            merged = self.data.merge(self.ticker_info, left_on='ticker', right_on='ticker')
            self.merged = merged
        except:
            print('ERROR could not merge')
           
    def volume_factor(self,df=None):
        if df == None:
            df = self.merged
        if 'avg_volume' and 'premarket_volume'in df.columns:
            df['avg_volume'] = df['avg_volume'].apply(self.clean_column_mapper)
            df['volume_factor'] = df['premarket_volume']/df['avg_volume']
            df['volume_factor'] = df['volume_factor'].astype(float).round(2)
            return df
        else: 
            print('Not the right columns for volume factor') 
    
    def clean_column_mapper(self,data):
        if 'K' in data:
            return float(re.sub('K','',data)) * 1000
        elif 'M' in data:
            return float(re.sub('M','',data)) * 1000000
        else:
            return data

    def tag_entry(self,tag,df=None):
        if df == None:
            df = self.merged
        df['index'] = tag
        return df 

    def format_for_db(self,df):
        """
        Takes df and turns it into dicts for mongo DB storage 
        """
        print('Formatting for Db entry')
        return df.to_dict(orient='records')

    def format_price_json(self):
        """
        Takes a dataframe of price action and turns it into a lists of lists
        """
        df = self.data
        df['dt'] = df.index.astype(str)
        df.reset_index(inplace=True)
        json_data = df.to_json()
        parsed = json.loads(json_data)
        return parsed

    def create_price_dict(self,ticker,date,daily_data=None):
        return_dict = {}
        data = self.data
        return_dict['dt'] = date
        return_dict['ticker'] = ticker
        return_dict['price_data'] = data
        if daily_data != None:
            return_dict['daily_data'] = daily_data
        return return_dict

class CleanColumns():
    def __init__(self,df):
        self.df = df

    def clean(self):
        """
        Iterates all columns to clean except those in the list
        """
        df = self.df
        for i in df.columns:
            if i in ['ticker','dt','process_time','company','index','earnings','company_name', 'sector', 'industry', 'country','setup']:
                continue
            else:
                df[i] = df[i].apply(self.column_cleaner_mapping)
        return df 

    def column_cleaner_mapping(self,data):
        """
        converts k,m,b ending numbers into floats 
        """
        try:
            return float(data)
        except:
            if 'K' in data:
                return float(re.sub('K','',data)) * 1000
            elif 'M' in data:
                return float(re.sub('M','',data)) * 1000000
            elif 'B' in data:
                return float(re.sub('B','',data)) * 1000000000
            else: 
                return data 