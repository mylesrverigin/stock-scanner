import pandas as pd 
from modules.mongo import DataManager

class CallPrice():
    def __init__(self,date):
        """
        The intention of this class is to get price data from the mongo db
        """
        self.date = date 

    def get_all_tickers(self,setup='D2'):
        """
        This returns all tickers in a list of strings 
        that have a matching setup to what is defined
        
        if the class is instantiated with more then one date in a list format 
        it can still handle that
        """
        dt = self.date
        Dm = DataManager()
        query = {'setup':setup}
        if isinstance(dt,list):
            result = []
            for date in dt:
                query['dt'] = date
                temp_result = Dm.find_info('price_data',query_dict_gte=query)
                result.append(pd.DataFrame(temp_result))
            while len(result) >= 2:
                result[0] = result[0].append(result[1],ignore_index=True)
                result.pop(1)
            tickers = result[0]['ticker'].to_list()
        else:
            query['dt'] = dt
            result = Dm.find_info('price_data',query_dict_gte=query)
            df = pd.DataFrame(result)
            try:
                tickers = df['ticker'].to_list()
            except:
                tickers = []
        if len(tickers) < 1:
            return False
        else:
            return tickers

    def return_price_intraday(self,ticker,interval='1'):
        """
        Takes price data patching interval specified from mongo
        currently can only do 1,5,15 intervals
        """
        interval_dict = {'1':'intraday_1m','5':'intraday_5m','15':'intraday_15m'}
        raw_price = self.get_price_from_db(ticker)[(interval_dict[interval])]
        df = self.format_to_df(raw_price)
        return df

    def return_price_daily(self,ticker):
        """
        return daily chart data
        """
        raw_price = self.get_price_from_db(ticker)['daily']
        df = self.format_to_df(raw_price)
        return df

    def get_price_from_db(self,ticker):
        """
        this method does all the heavy lifting when calling price data
        """
        DM = DataManager()
        data = DM.find_info('price_data',{'ticker':ticker,'dt':self.date})
        return data[0]

    def format_to_df(self,raw):
        """
        Returns the data as a Dataframe
        """
        df = pd.DataFrame(raw)
        df.reset_index(drop=True,inplace=True)
        if 'Datetime' in df.columns:
            df.drop('Datetime',axis=1,inplace=True)
        if 'Date' in df.columns:
            df.drop('Date',axis=1,inplace=True)
        return df
