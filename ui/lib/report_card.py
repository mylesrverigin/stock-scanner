from modules.mongo import DataManager

class ReportCard():
    def __init__(self,date):
        """
        This is for saving Report cards, 
        HTML has hidden inputs that default everything to false
        the user changes inputs to true over the day
        """
        self.date = date

    def log_report_card(self,data):
        """
        Takes the data submitted and then stores it in mongo
        """
        self.card = data
        log_dict = {'dt':self.date,'weekly_goal':self.card['weekly_goal']}
        for i in self.card:
            if i not in ['save','weekly_goal']:
                try:
                    log_dict[i] = bool(self.card[i])
                except:
                    log_dict[i] = self.card[i]
        DM = DataManager()
        DM.add_one(info=log_dict,collection='reportcards')

    def return_views(self):
        """
        returns the report cards for date specified in self.date (usually current date)
        reports is a list of dicts
        """
        DM = DataManager()
        reports = DM.find_info('reportcards',query_dict_gte={'dt':self.date},query_dict_lte={})
        for report in reports:
            for key in ['_id','save','datetime','dt']:
                try:
                    del report[key]
                except:
                    continue
            for key in list(report):
                if report[key] == False:
                    del report[key]
        return reports

    def weekly_view(self,date_list):
        """
        takes a list of dates and calls return_views for each one to 
        make a review sheet for the week to look at
        """
        if len(date_list) == 0:
            return
        return_dict = {}
        for i in date_list:
            self.date = i
            reports = self.return_views()
            return_dict[i] = reports
        return return_dict