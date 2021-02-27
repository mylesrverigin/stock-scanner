import pandas as pd
import datetime as dt

class FormatPrice():
    def __init__(self,df):
        """
        This class is meant to take in price dataframes and turn it into a format that can be injected into a canvas js chart
        """
        self.data = df

    def run(self):
        self.format_dates()
        self.format_price()
        self.assemble_final()
        return self.create_export()

    def format_dates(self):
        """
        Takes dt column and changes it into a useable format that list of strings in format (yyyy,mm,dd,hh,mm)
        """
        time_format = '%Y %m %d %H %M'
        df = self.data
        df['string_time'] = pd.to_datetime(df['dt']).dt.strftime(time_format)
        df['final_time'] = '{ x: new Date('+df['string_time'].str.replace(' ',',')+'), y: '
        self.data = df

    def format_price(self):
        df = self.data
        o = df['Open'].astype(str)
        h = df['High'].astype(str)
        l = df['Low'].astype(str)
        c = df['Close'].astype(str)
        df['final_price'] = '[' + o +','+ h +','+ l +','+ c + '] },'
        self.data = df

    def assemble_final(self):
        df = self.data
        df['for_export'] = df['final_time'] + df['final_price']
        self.data = df

    def drop_cols(self):
        pass

    def create_export(self):
        return self.data['for_export'].to_list()

