from ui import app
from modules.mongo import DataManager
from modules.time_handling import TimeManagement
import pandas as pd


class Inplay():
    def __init__(self):
        """
        The intention of this is for putting data onto the homepage 
        example loading all the inplay names from yesterday so I know where to focus tomorrow
        """

    def run(self):
        date = self.get_date_to_use()
        tickers = self.get_inplay(date,collection='premarket_tickers')
        return tickers

    def get_date_to_use(self):
        """
        looking to get todays date unless weekend then previous day
        """
        Time = TimeManagement()
        weekday = Time.day_of_week()
        if weekday not in [5]:
            date = Time.date_now()
        elif weekday == 6:
            date = Time.date_days_ago(days=2)
        elif weekday == 5:
            date = Time.date_days_ago(days=1)
        return date

    def get_inplay(self,date,collection='D1_plays'):
        DM = DataManager()
        returned = DM.find_info(collection=collection,query_dict_gte={'dt':date},query_dict_lte={'shs_float':31000000})
        if len(returned) > 0:
            df = pd.DataFrame(returned)
            df = df[['ticker','shs_float','premarket_change','premarket_volume','premarket_price','short_float']]
            return df.to_dict(orient='records')
        else:
            return []