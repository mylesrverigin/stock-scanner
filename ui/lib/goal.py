from ui import app

class Goals():
    def __init__(self):
        self.weekly = app.config['WEEKLY_GOAL']
        self.business_plan = app.config['BUSINESS_PLAN']

    def return_weekly_goal(self):
        return self.weekly

    def return_business_plan(self):
        return self.business_plan