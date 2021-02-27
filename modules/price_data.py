import yfinance as yf 


class GetPriceData():
    def __init__(self,ticker):
        """
        ticker is a string 
        """
        self.ticker = yf.Ticker(ticker)

    def get_data(self,timeframe='1m',daterange=['2020-09-01','2020-09-02'],premarket=True):
        """
        timeframe can be 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        daterange = [start,end] YYYY-MM-DD
        gets price data up to but not including end date
        """
        price_data = self.ticker.history(interval=timeframe,start=daterange[0],end=daterange[1],prepost=premarket)
        return price_data




# print('Starting')
# test = GetPriceData('EARS')
# print(test.get_data(timeframe='5m',daterange=['2020-09-04','2020-09-05'],premarket=True))
# print('Working')