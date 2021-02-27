import pandas as pd 

class CreateDatatable():
    def __init__(self,data):
        self.data = data
        #todo make names a dict passed in so this code is robust
        self.names = {'ticker':'Ticker','premarket_price':'Price','premarket_change':'Gap %','atr':'ATR','premarket_vol':'Premarket Volume',
                    'avg_volume':'Avg Volume','volume_factor':'Volume Factor',
                    'short_float':'Float % Short','inst_own':'Institutional Ownership'}
        self.shrink_values = ['premarket_vol','avg_volume']

    def run(self):
        data = self.data
        table_return = ''
        if len(data) != 0: 
            for i in self.names:
                if i in data.columns:
                    table_return += self.make_table_row(i)
        return table_return

    def make_table_row(self,field):
        data = self.data 
        row_return = '<tr>'
        row_name = f'<th style="text-align:right" nowrap>{self.names[field]}</th>'
        data = data.round(2)
        if field in data.columns:
            row_return += row_name
            if field in self.shrink_values:
                data[field] = (data[field].astype(float)/1000).astype(str) + 'K'
            values = data[field].astype(str).values
            row_return += '<TD nowrap>'+'</TD><TD nowrap>'.join(values)+'</TD>'
        row_return += '</tr>'
        return row_return