from modules.mongo import DataManager

class PlayBooks():
    def __init__(self,date,ticker):
        """
        default params are a date and a ticker
        for just viewing the playbooks default uses only dt so ticker can be any string
        """
        self.date = date
        self.ticker = ticker

    def log_playbook(self,playbook_dict):
        """
        takes in the form data from playbook page and and logs it into a dict
        if there is ticker data from the ticker selected it for the specific date(not implemented) it adds that to playbook 
        so that its easier to filter out in the future
        """
        log_dict = {'dt':self.date}
        for i in playbook_dict:
            if i in ['daily_support','daily_resistance','support_30m','resistance_30m','premarket_support','premarket_resistance']:
                try: 
                    log_dict[i] = float(playbook_dict[i])
                except:
                    log_dict[i] = playbook_dict[i]
            else:
                log_dict[i] = playbook_dict[i]
        DM = DataManager()
        #way to filter the most recent ticker request by date currently it just uses the last one in the list 
        extra_data = DM.find_info('premarket_tickers',query_dict_gte={'ticker':self.ticker},query_dict_lte={})
        try:
            extra_data = extra_data[-1]
        except:
            pass
        ####
        for col in ['premarket_change','premarket_vol','index','market_cap','shs_float','short_float','rel_volume','avg_volume','price','volume_factor']:
            if col in extra_data:
                log_dict[col] = extra_data[col]
        DM.add_one(info=log_dict,collection='playbooks')

    def return_views(self):
        """
        returns the playbooks for date specified in self.date (usually current date)
        playbook is a list of dicts, We filter out some of the fields and then pass the 
        dictionary forward 
        """
        DM = DataManager()
        playbooks = DM.find_info('playbooks',query_dict_gte={'dt':self.date},query_dict_lte={})
        for play in playbooks:
            for key in ['_id','dt','save','index','market_cap','rel_volume','price','shs_float']:
                try:
                    del play[key]
                except:
                    continue
            for key in ['short_float']:
                    try:
                        if play[key] == '-':
                            del play[key]
                    except:
                        continue
            for key in play: 
                if isinstance(play[key],str):
                    play[key] = play[key].strip()
        return playbooks

    def weekly_view(self,date_list):
        if len(date_list) == 0:
            return
        return_dict = {}
        for i in date_list:
            self.date = i
            playbooks = self.return_views()
            return_dict[i] = playbooks
        return return_dict