from web_scrape import Scrape,CleanScrape
import re
import pandas as pd 

#Base Urls to scrape 
# atr 0.75, 5 mil vol, avg vol > 750k, rvol > 2, 
# D1 criteria atr>0.5 avg vol >300k, rvol>2, up/down 3%, current vol>2m
base_address = 'https://finviz.com/screener.ashx?v=151&f=sh_avgvol_o300,sh_curvol_o2000,sh_relvol_o2,ta_averagetruerange_o0.5,ta_gap_u3&ft=4&o=-relativevolume&c=1,2,3,4,5,6,24,25,26,28,30,49,60,61,63,64,65,66,67,68'
# this was the old scan 
# 'https://finviz.com/screener.ashx?v=152&f=sh_avgvol_o750,sh_curvol_o5000,sh_relvol_o2,ta_averagetruerange_o0.75&ft=4&o=-change&c=1,2,3,4,5,6,24,25,26,28,30,49,60,61,63,64,65,66,67,68'
html_tag = 'tr'
html_element_dict = {'class':['table-light-row-cp','table-dark-row-cp']}
regex_pattern = r">(?![<\s])(-?\w*.?\w*%?.?\d*)\S"
df_col_names = ['ticker','company_name','sector','industry','country',
                    'market_cap','shares_outstanding','float','insider_own','inst_own','float_short',
                    'atr','change_from_open','gap_size','avg_vol','rel_vol','price','change_total','volume','earnings']

class PostMarketScrape():
    def __init__(self,base_address,html_tag,html_element_dict,regex_pattern,df_col_names):
        self.base_address = base_address
        self.html_tag = html_tag
        self.html_element_dict = html_element_dict
        self.regex_pattern = regex_pattern
        self.df_col_names = df_col_names

    def run(self,gainers=None,up=None):
        if gainers != None:
            self.change_address_sort(gainers=gainers)
        if up != None:
            self.change_scan(up=up)
        html_scrape = Scrape(self.base_address,self.html_tag,self.html_element_dict).run()
        self.clean_data = CleanScrape(html_scrape,self.regex_pattern,self.df_col_names).return_df()

    def change_address_sort(self,gainers=True):
        """
        to get down stock or up stock we need to change the sort of the webpage
        if its -change its gainers first 
        if its change its losers first 
        """
        address = self.base_address
        if gainers:
            self.base_address = re.sub(r"\-?change","-change",address)
        else:
            self.base_address = re.sub(r"\-?change","change",address)

    def change_scan(self,up=True):
        """
        changes the 3% gap to up/down if true/false
        """
        address = self.base_address
        if up:
            self.base_address = re.sub(r"\_[du]3\&ft","_u3&ft",address)
        else:
            self.base_address = re.sub(r"\_[du]3\&ft","_d3&ft",address)

    def return_specifc_settings(self,dict_of_settings,negative_values=None):
        """
        give a dictionary where keys match col names 
        will filter based on keys value
        numeric columns only as it changes column type to float before filtering
        """
        df1 = self.clean_data
        for i in dict_of_settings:
            df1[i] = df1[i].apply(self.individual_element_clean)
        filtered_df = df1.loc[(df1[list(dict_of_settings)] >= pd.Series(dict_of_settings)).all(axis=1)]
        if isinstance(negative_values,dict):
            for i in negative_values:
                filtered_df[i] = filtered_df[i].apply(self.individual_element_clean)
            filtered_df = filtered_df.loc[(filtered_df[list(negative_values)] <= pd.Series(negative_values)).all(axis=1)]
        return filtered_df

    def return_df(self):
        return self.clean_data

    def individual_element_clean(self,element):
        if 'M' in element:
            element = re.sub(r'(?<=\d)M','',element)
            element = float(element) * 1000000
        elif 'B' in element:
            element = re.sub(r'(?<=\d)B','',element)
            element = float(element) * 1000000000
        return float(element)

# postmarket = PostMarketScrape(base_address,html_tag,html_element_dict,regex_pattern,df_col_names)
# postmarket.run(up=False)
# print(postmarket.return_specifc_settings({},{}))