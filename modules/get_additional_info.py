from web_scrape import Scrape,CleanScrape
import re
import pandas as pd 

defaults_dict = {
    'base_html' : 'https://finviz.com/quote.ashx?t=',
    'html_tag' : 'tr',
    'dict_of_elements' : {'class':"table-dark-row"},
    'pattern' : r">(?![<\s])(-?\w*.?\w*\s?\d*%?)\S",
    'col_names' : ['1','2']
}

class RequestInfo():
    def __init__(self,series_of_tickers,settings_dict=None):
        """
        By default we use the global dict unless another one is provided so 
        that we dont have to mess with settings
        """
        global defaults_dict
        if settings_dict != None:
            info = settings_dict
        else: 
            info = defaults_dict
        self.tickers = series_of_tickers
        self.base_html = info['base_html']
        self.html_tag = info['html_tag']
        self.dict_of_elements = info['dict_of_elements']
        self.pattern = info['pattern']
        self.col_names = info['col_names']

    def run(self,):
        df = pd.DataFrame()
        for ticker in self.tickers:
            try:
                self.submit_scrape(ticker,self.html_tag,self.dict_of_elements)
                clean_lists = self.clean_scrape(self.pattern,self.col_names)
                temp_df = self.create_df(clean_lists)
                temp_df['ticker'] = ticker
                df = pd.concat([df,temp_df],axis=0,ignore_index=True,)
            except:
                continue
        self.final = df 

    def dump_return(self):
        return self.final

    def submit_scrape(self,ticker,html_tag,dict_of_elements):
        """
        the code that scrapes each tickers page 
        """
        address = self.generate_html(ticker)
        self.raw_html = Scrape(address,html_tag,dict_of_elements).run()
    
    def clean_scrape(self,pattern,col_names):
        """
        Cleans the returned data from each request
        """
        cleaned = CleanScrape(self.raw_html,pattern,col_names=col_names).return_lists()
        return cleaned

    def generate_html(self,ticker):
        """
        creates the HTML address for each ticker 
        """
        return self.base_html + str(ticker)

    def create_df(self,list_of_info):
        """
        creates a df from, list_of_info is the output from beautiful soup after cleaning it 
        """
        temp_dict = {}
        for row in list_of_info: 
            for val in range(0,len(row),2):
                temp_dict[row[val]] = row[val+1]
        df = pd.DataFrame(temp_dict,index=[0])
        df.columns = df.columns.str.lower().str.strip().str.replace('.','').str.replace(' ','_')
        return df 

    def create_dict(self,list_of_info):
        """
        Creates a dict of all the values easily inserted into db
        """
        temp_dict = {}
        for row in list_of_info: 
            for val in range(0,len(row),2):
                temp_dict[row[val]] = row[val+1]
        return temp_dict

# test = RequestInfo(series_of_tickers=['AMD'])
# test.run()
# x = test.dump_return()
# print(x)