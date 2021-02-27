from modules.mongo import DataManager

class Journals():
    def __init__(self,date):
        self.date = date

    def log_journal(self,journal_dict):
        """
        takes the journal dict and removes hardcoded fields 
        and logs it to mongo
        (we copy to another dict because input dict is immutible)
        """
        log_dict = {}
        log_dict['dt'] = self.date
        for i in journal_dict:
            if i in ['save']:
                continue
            else:
                log_dict[i] = journal_dict[i]
        DM = DataManager()
        DM.add_one(info=log_dict,collection='journals')

    def return_views(self):
        """
        returns the journal for date specified in self.date (usually current date)
        journal is a list of dicts
        """
        DM = DataManager()
        journals = DM.find_info('journals',query_dict_gte={'dt':self.date},query_dict_lte={})
        for journal in journals:
            for key in ['_id','save']:
                try:
                    del journal[key]
                except:
                    continue
            for key in journal: 
                if isinstance(journal[key],str):
                    journal[key] = journal[key].strip()
        return journals

    def weekly_view(self,date_list):
        if len(date_list) == 0:
            return
        return_dict = {}
        for i in date_list:
            self.date = i
            journals = self.return_views()
            return_dict[i] = journals
        return return_dict

    def weekly_trades(self,date_list):
        if len(date_list) == 0:
            return
        trades = 0
        for i in date_list:
            self.date = i
            journals = self.return_views()
            try:
                trades += int(journals[0]['num_trades'])
            except:
                continue
        return trades