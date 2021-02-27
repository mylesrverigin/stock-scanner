from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re
import pandas as pd

class Scrape():
    def __init__(self,address,html_tag,dict_of_elements):
        self.address = address
        self.html_tag = html_tag
        self.dict_of_elements = dict_of_elements
        self.get_webpage()

    def run(self):
        self.parse_page()
        return self.elements

    def get_webpage(self):
        """
        Opens the webpage and stores the result 
        """
        req = Request(self.address,headers={'User-Agent': 'Chrome/85.0.4183.83 '})
        self.webpage_html = urlopen(req).read()

    def parse_page(self):
        """
        Parses the stored page and returns specific parts 
        can pass multiple keys in dict_of_elements or values
        returns list 
        example html_tag = 'tr',
        example dict_of_elements = {'class':['table-light-row-cp','table-dark-row-cp']}
        for a good baseline leave dict of elements like {'class':''} and it will just get alot of page 
        """
        page_soup = soup(self.webpage_html,"html.parser")
        self.elements = []
        for key,value in self.dict_of_elements.items():
            if isinstance(value,list):
                for i in value:
                    self.elements.extend(page_soup.findAll(self.html_tag,{key:i}))
            else:
                self.elements.extend(page_soup.findAll(self.html_tag,{key:value}))

class CleanScrape():
    def __init__(self,list_of_elements,pattern,col_names):
        """
        list_of_elements is what gets scraped
        pattern example = r"[stonks]"
        col_names is what we want the DF col names to be 
        example col_names 
        ['ticker','company_name','sector','industry','country',
            'market_cap','shares_outstanding','float','insider_own','inst_own','float_short',
            'atr','change_from_open','gap_size','avg_vol','rel_vol','price','change_total','volume','earnings']
        """
        self.elements = list_of_elements
        self.pattern = pattern
        self.col_names = col_names

    def return_lists(self):
        self.refine_html()
        return self.cleaned_html

    def return_df(self):
        self.refine_html()
        try:
            df = pd.DataFrame(self.cleaned_html,columns=self.col_names)
            return df
        except:
            print('Miss matched col lens',len(self.col_names),'data return len',len(self.cleaned_html[0]))
        
    def refine_html(self):
        """
        takes the raw html and then converts it to a list 
        through a series of methods to be legible to humans
        """
        final_list = []
        for element in self.elements:
            unclean_list = self.collect_info(element)
            clean_list = self.clean_info(unclean_list)
            final_list.append(clean_list)
        self.cleaned_html = final_list

    def collect_info(self,html_obj):
        """
        Takes in html elements individually and extracts the info we want and 
        return them as a list 
        """
        result = re.findall(self.pattern,str(html_obj),flags=re.IGNORECASE)
        return result

    def clean_info(self,info_list):
        """
        Takes list from collect_info and removes the unused characters 
        """
        return [ re.sub(r'[<>/,&%]*','',i) for i in info_list]

# print('testing')
# test = Scrape(address='https://thestockmarketwatch.com/markets/pre-market/today.aspx',html_tag='tr',dict_of_elements={'class':''})
# result = test.run()
# c = CleanScrape(list_of_elements=result,pattern=r">(?![<\s])(-?\w*.?\w*%?.?\d*)\S",col_names=['test'])
# final = c.return_lists()
# print(final)
# print('Done')