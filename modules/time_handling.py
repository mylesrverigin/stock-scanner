from datetime import datetime,timedelta
from pytz import all_timezones,timezone

class TimeManagement():
    def __init__(self):
        self.now = datetime.now(timezone('US/Eastern'))

    def date_now(self,delimiter='/',date_time=None):
        #current yyyy/mm/dd
        time_format = "%Y{}%m{}%d".format(delimiter,delimiter)
        if date_time != None:
            return datetime.strftime(date_time,time_format)
        else:
            return datetime.strftime(self.now,time_format)

    def date_time_now(self):
        #current yyyy/mm/dd hh:mm
        time_format = "%Y/%m/%d %H:%M"
        return datetime.strftime(self.now,time_format)

    def date_days_ago(self,days):
        #previous yyyy/mm/dd hh:mm
        time_format = "%Y/%m/%d"
        date = self.now - timedelta(days=days)
        return datetime.strftime(date,time_format)

    def date_days_future(self,days):
        #previous yyyy/mm/dd hh:mm
        time_format = "%Y/%m/%d"
        date = self.now + timedelta(days=days)
        return datetime.strftime(date,time_format)

    def day_of_week(self):
        #current day as int mon=0 sun=6
        return datetime.today().weekday()

    def timeslice(self,days=None,years=None):
        time_slice = []
        if days != None:
            self.now = self.now + timedelta(days=1)
            temp_date = self.date_now('-')
            self.now = datetime.now(timezone('US/Eastern'))
            self.now = self.now - timedelta(days=days)
            time_slice.append(self.date_now('-'))
            time_slice.append(temp_date)
            #reset time to now have to re instantiate class again 
            self.now = datetime.now(timezone('US/Eastern'))
            return time_slice
        if years != None:
            self.now = self.now + timedelta(days=1)
            temp_date = self.date_now('-')
            total_days = float(years)*365
            self.now = self.now - timedelta(days=total_days)
            time_slice.append(self.date_now('-'))
            time_slice.append(temp_date)
            #reset time to now have to re instantiate class again 
            self.now = datetime.now(timezone('US/Eastern'))
            return time_slice

    def weekly_review_times(self):
        """
        the way I index my entries 'dt' isn't a date 
        this is a way to circumevent it
        """
        return_list = []
        current_weekday = self.day_of_week()
        current_weekday_hold = current_weekday
        while current_weekday >= 0:
            if current_weekday >= 5:
                current_weekday -= 1
            else:
                date_time = self.now - timedelta(days=(current_weekday_hold - current_weekday))
                temp_date = self.date_now(date_time=date_time)
                return_list.append(temp_date)
                current_weekday -= 1
        return_list.reverse()
        return return_list

# test = TimeManagement()
# x = test.timeslice(days=1)
# y = test.timeslice(years=1)
# dt = test.date_days_ago(2)
# print(dt)
# print(x,'\n',y)
