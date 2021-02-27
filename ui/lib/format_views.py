class FormatWeeklyReview():
    def __init__(self,dates,tradeplans,journals,playbooks,reportcards):
        self.dates = dates
        self.tradeplans = tradeplans
        self.journals = journals
        self.playbooks = playbooks
        self.reportcards = reportcards

    def format_review(self):
        final_dict = {}
        for i in self.dates:
            journal = self.journals[i]
            tradeplan = self.tradeplans[i]
            playbook = self.playbooks[i]
            reportcard = self.reportcards[i]
            temp_list = []
            if self.check(journal):
                temp_list.append(journal)
            if self.check(reportcard):
                temp_list.append(reportcard)
            if self.check(tradeplan):
                temp_list.append(tradeplan)
            if self.check(playbook):
                temp_list.append(playbook)
            if len(temp_list) > 0:
                final_dict[i] = temp_list
        return final_dict

    def check(self,input_data):
        if len(input_data) == 0:
            return False
        else:
            return True