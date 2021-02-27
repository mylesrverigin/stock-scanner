from modules.mongo import DataManager

class TradePlans():
    def __init__(self,date,ticker):
        self.date = date
        self.ticker = ticker

    def log_tradeplan(self,tradeplan_dict):
        """
        takes in the form data from tradeplan page and and logs it into a dict
        if there is ticker data from the ticker selected, for the specific date(not implemented) it adds that to tradeplan 
        so that its easier to filter out in the future
        """
        log_dict = {}
        log_dict['dt'] = self.date
        for i in tradeplan_dict:
            if i in ['support','resistance']:
                numeric_levels = self.process_levels(tradeplan_dict[i])
                log_dict[i] = numeric_levels
            else:
                log_dict[i] = tradeplan_dict[i]
        DM = DataManager()
        #way to filter the most recent ticker request by date currently it just uses the last one in the list 
        extra_data = DM.find_info('premarket_tickers',query_dict_gte={'ticker':self.ticker},query_dict_lte={})
        try:
            extra_data = extra_data[-1]
        except:
            pass
        ####
        for col in ['premarket_change','premarket_vol','index','market_cap','shs_float','short_float','atr','rel_volume','avg_volume','price','volume_factor']:
            if col in extra_data:
                log_dict[col] = extra_data[col]
        DM.add_one(info=log_dict,collection='tradeplans')

    def process_levels(self,string):
        list_levels = string.split(',')
        return_list = []
        for i in list_levels:
            try:
                return_list.append(float(i))
            except:
                return_list.append(i)
        return return_list

    def return_views(self):
        """
        returns the trade plans for date specified in self.date (usually current date)
        plans is a list of dicts, We filter out some of the fields and then pass the 
        dictionary forward 
        """
        DM = DataManager()
        plans = DM.find_info('tradeplans',query_dict_gte={'dt':self.date},query_dict_lte={})
        for plan in plans:
            for key in ['_id','datetime','dt','save','index','market_cap','rel_volume','price','shs_float']:
                try:
                    del plan[key]
                except:
                    continue
            for key in ['short_float']:
                    try:
                        if plan[key] == '-':
                            del plan[key]
                    except:
                        continue
            for key in plan: 
                if isinstance(plan[key],str):
                    plan[key] = plan[key].strip()
        return plans

    def weekly_view(self,date_list):
        if len(date_list) == 0:
            return
        return_dict = {}
        for i in date_list:
            self.date = i
            tradeplans = self.return_views()
            return_dict[i] = tradeplans
        return return_dict
