from ui import app
from modules.mongo import DataManager
from ui.lib.call_price import CallPrice
from ui.lib.format_price import FormatPrice
import re 
import pandas as pd 

class Charts():
    def __init__(self,date):
        self.container = 'ChartContainer_'
        self.dt = date
        self.charts = []
        self.divs = []
    
    def return_charts(self):
        return self.charts

    def return_divs(self):
        return self.divs

    def run(self):
        charts,divs = self.build_price_charts()
        return charts,divs

    def inject_chart_container(self,template,con=''):
        """
        Con is container name (java script variable name) and they need to be all distinct for multiple charts 
        """
        return re.sub('CHARTCONTAINER',con,template)

    def inject_div(self,con=''):
        """
        Con is container name (java script variable name) and they need to be all distinct for multiple charts 
        """
        base_template = app.config['CHART_DIV']
        base_template = re.sub('CHARTCONTAINER',con,base_template)
        return base_template

    def get_tickers(self,dt='2020/10/23'):
        """
        Make sure you call the setup in the price data collection otherwise you default to D2 setups
        """
        Price = CallPrice(dt)
        tickers = Price.get_all_tickers(setup='premarket_gapper')
        if not tickers:
            return False
        else:
            return tickers

    def inject_price(self,template,price_data=''):
        """
        Meant to put price data into charts
        """
        return re.sub('PRICEDATA',price_data,template)

    def inject_title(self,template,title):
        """
        Meant to put title into charts
        """
        return re.sub('TITLE',title,template)

    def build_price_charts(self):
        tickers = self.get_tickers(self.dt)
        if not tickers:
            return {},{}
        Price = CallPrice(self.dt)
        result_charts = ['<script>']
        result_divs = []
        for ticker in tickers:
            for timeframe in ['d','15','5','1']:
                try:
                    if timeframe == 'd':
                        container_name = self.container + f'_{ticker}_' + 'daily'
                        data = Price.return_price_daily(ticker=ticker)
                        title = ticker + ' ' + 'Daily'
                    else:
                        container_name = self.container + f'_{ticker}_' + timeframe
                        data = Price.return_price_intraday(ticker=ticker,interval=timeframe)
                        title = ticker + ' ' + timeframe + 'm'
                    Format = FormatPrice(data)
                    rendered_price = ''.join(Format.run())
                    div = self.inject_div(con=container_name)
                    if timeframe == 'd':
                        charts = self.inject_chart_container(template=app.config['DAILY_CHART_TEMPLATE'],con=container_name)
                    else:
                        charts = self.inject_chart_container(template=app.config['CHART_TEMPLATE'],con=container_name)
                    charts = self.inject_title(template=charts,title=title)
                    charts = self.inject_price(template=charts,price_data=rendered_price)
                    result_charts.append(charts)
                    result_divs.append(div)
                except:
                    continue
        result_charts.append('</script>')
        return result_charts,result_divs



            