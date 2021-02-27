from web_scrape import Scrape,CleanScrape
import re
import pandas as pd 

#'base_address':'https://www.benzinga.com/premarket/',
#'html_element_dict':{'class':"cell large-auto medium-auto"},
#'regex_pattern' : r"(?<=>)\s*?(\w{0,4}?[\$-]?\d*?\.?\d*?%?\w?)\s*?<",

defaults_dict = {
    'base_address':'https://thestockmarketwatch.com/markets/pre-market/today.aspx',
    'html_tag':'tr',
    'html_element_dict':{'class':""},
    'regex_pattern' : r">(?![<\s])(-?\w*.?\w*%?.?\d*)\S",
    'df_col_names' : ['premarket_change', 'premarket_price', 'premarket_volume', 'ticker', 'company', 'premarket_v'],
}
class PreMarket():
    def __init__(self,dict_of_options=None):
        """
        By default we use the global dict unless another one is provided so 
        that we dont have to mess with settings
        """
        global defaults_dict
        if dict_of_options != None:
            dict_to_use = dict_of_options
        else:
            dict_to_use = defaults_dict
        self.base_address = dict_to_use['base_address']
        self.html_tag = dict_to_use['html_tag']
        self.html_element_dict = dict_to_use['html_element_dict']
        self.regex_pattern = dict_to_use['regex_pattern']
        self.df_col_names = dict_to_use['df_col_names']
    
    def run(self,return_df=False):
        html_scrape = Scrape(self.base_address,self.html_tag,self.html_element_dict).run()
        self.clean_data = CleanScrape(html_scrape,self.regex_pattern,self.df_col_names).return_lists()[0]
        self.lists = self.clean_stock_market_watch()
        self.results = self.create_df()
        if return_df:
            return self.results
        
    def clean_benzinga(self):
        """
        setup specifically for the format benzinga comes in as 
        turns out a list of lists to be made into a df 
        """
        data = self.clean_data
        temp_list = []
        for index,value in enumerate(data):
            index + 1 
            if value in ['','Gainers','Losers','Stock','Company','Price','Volume']:
                continue
            elif len(temp_list) >= 1 and value in temp_list[-1]:
                #checks to make sure value isnt the same as the one before 
                continue
            else:
                lower = re.findall(r"[a-z]",value)
                if len(lower) >= 1:
                    continue
                else:
                    temp_list.append(re.sub(r'\$','',value))
        return_list = [temp_list[i:i + 4] for i in range(0, len(temp_list), 4)]
        for i in return_list:
            if 'K' in i[-1]:
                i[-1] = float(re.sub('K','',i[-1])) * 1000
            elif 'M' in i[-1]:
                i[-1] = float(re.sub('M','',i[-1])) * 1000000
        return return_list

    def clean_stock_market_watch(self):
        """
        setup specifically for the format stock market watch comes in as 
        turns out a list of lists to be made into a df 
        runs through list and takes out column names and $ then splits remaining info into lists of 6 that get returned
        to be made into a DF
        """
        data = self.clean_data
        count = 0
        temp_list = []
        return_list = []
        for i in data:
            if i in ['$','Company','Volume','PreMarket','Pro','Top Losing ','Chg','Last','Symb','Top Gaining ']:
                continue
            else:
                count += 1
                if count <= 6:
                    temp_list.append(i)
                else:
                    return_list.append(temp_list)
                    temp_list = []
                    temp_list.append(i)
                    count = 1
            if i == data[-1]:
                return_list.append(temp_list)
        return return_list

    def create_df(self):
        df = pd.DataFrame(self.lists,columns=self.df_col_names)
        return df

    def return_specifc_settings(self,dict_of_settings,negative_values=None):
        """
        give a dictionary where keys match col names 
        will filter based on greater then keys value
        numeric columns only as it changes column type to float before filtering
        """
        df1 = self.results
        for i in dict_of_settings:
            df1[i] = df1[i].astype(float)
        filtered_df = df1.loc[(df1[list(dict_of_settings)] >= pd.Series(dict_of_settings)).all(axis=1)]
        if isinstance(negative_values,dict):
            for i in negative_values:
                filtered_df[i] = filtered_df[i].astype(float)
            filtered_df = filtered_df.loc[(filtered_df[list(negative_values)] <= pd.Series(negative_values)).all(axis=1)]
        return filtered_df

# premarket = PreMarket()
# results = premarket.run(return_df=True)
# print('Start',results,'END')
# print(premarket.return_specifc_settings({'volume':30000},{'price':20}))
#'change', 'price', 'volume'