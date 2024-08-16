import pandas as pd

'''
#Asia Range in UTC 00:00-04:00
#Asia range close
#London Open in UTC 06:00-09:00
#New York Open in UTC 11:00-14:00
#Silver Bullet in UTC 14:00-15:00
#London Close in UTC 14:00-16:00
#08:30 in UTC-4 in UTC 12:30
'''

class Trader:
    # Loading the csv data file
    df = pd.read_csv('BTCUSDT-15m-2024-07.csv', names = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_volume', 'count', 
                                                     'taker_buy_volume', 'taker_buy_quote_volume', 'ignore'])

    # Convert open and close times from epoch to normal 
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    num_rows = df.shape[0] # Number of candles

    def __init__(self):
        # Defining some variables to have some reference values
        self.asia_high = 0
        self.asia_low = 100000000
        self.asia_open = 0
        self.asia_close = 0
        self.londono_high = 0
        self.londono_low = 100000000
        self.londono_open = 0
        self.londono_close = 0
        self.newyork_high = 0
        self.newyork_low = 100000000
        self.newyork_open = 0
        self.newyork_close = 0
        self.londonc_high = 0
        self.londonc_low = 100000000
        self.londonc_open = 0
        self.londonc_close = 0
        self.newyork_midnight_open = 0
        self.eight_thrity = 0
        self.i = 1
        self.day = 1
        self.day_next = 2
        self.date = 0
        self.ts = 0
        self.ts_next = 0

    def det_killzone(self, idx):

        row_data = self.df.iloc[idx] # Get one row from the whole csv file
        self.date = row_data['close_time'].date()
        minute = row_data['open_time'].minute
        ts = row_data['open_time'].hour
        self.day = row_data['close_time'].day

        # Asia Open Price
        if ts == 0 and minute == 0:
            self.asia_open = row_data['open']

        # Asia Close Price
        if ts == 4 and minute == 0:
            self.asia_close = row_data['close']

        # Get Asia High and Low
        if 0 <= ts < 4:
            high = row_data['high']
            low = row_data['low']
            if high >= self.asia_high:
                self.asia_high = high
            if low <= self.asia_low:
                self.asia_low = low

        # London Open Open Price
        if ts == 6 and minute == 0:
            self.londono_open = row_data['open']

        # London Open Close Price
        if ts == 9 and minute == 0:
            self.londono_close = row_data['close']

        # Get London Open High and Low
        if 6 <= ts < 9:
            high = row_data['high']
            low = row_data['low']
            if high >= self.londono_high:
                self.londono_high = high
            if low <= self.londono_low:
                self.londono_low = low

        # New York Open Price
        if ts == 11 and minute == 0:
            self.newyork_open = row_data['open']

        # New York Close Price
        if ts == 14 and minute == 0:
            self.newyork_close = row_data['close']

        # Get New York High and Low
        if 11 <= ts < 14:
            high = row_data['high']
            low = row_data['low']
            if high >= self.newyork_high:
                self.newyork_high = high
            if low <= self.newyork_low:
                self.newyork_low = low

        # London Close Open Price
        if ts == 14 and minute == 0:
            self.londonc_open = row_data['open']

        # London Close Close Price
        if ts == 16 and minute == 0:
            self.londonc_close = row_data['close']

        # Get London Close Open High and Low
        if 14 <= ts < 16:
            high = row_data['high']
            low = row_data['low']
            if high >= self.londonc_high:
                self.londonc_high = high
            if low <= self.londonc_low:
                self.londonc_low = low
        
        # 8:30
        if ts == 12 and minute == 30:
            self.eight_thrity = row_data['open']

        # New York Midnight Open Price
        if ts == 4 and minute == 0:
            self.newyork_midnight_open = row_data['open']
    
    def execute(self):
        i = 0
        idx = 0
        df3 = pd.DataFrame()
        
        for i in range(self.num_rows): # Reading through every row of the csv file
            # If open time is 23:45 then compare the price for the last row then execute csv write for killzone prices 
            if int(self.df.iloc[idx]['open_time'].hour) == 23 and int(self.df.iloc[idx]['open_time'].minute) == 45: 
                self.det_killzone(idx)
                idx = idx + 1
                data = {'Asia Range Open': self.asia_open, 'Asia Range Close': self.asia_close, 'Asia Range High': self.asia_high, 'Asia Range Low': self.asia_low, 
                        'London Open Open': self.londono_open, 'London Open Close': self.londono_close, 'London Open High': self.londono_high, 'London Open Low': self.londono_low, 
                        'New York Open': self.newyork_open, 'New York Close': self.newyork_close, 'New York High': self.newyork_high, 'New York Low': self.newyork_low, 
                        'London Close Open': self.londonc_open, 'London Close Close': self.londonc_close, 'London Close High': self.londonc_high, 
                        'London Close Low': self.londonc_low, 'New York Midnight Open Price': self.newyork_open, '8:30 Open': self.eight_thrity}
                df2 = pd.DataFrame(data, index=[self.date])
                df2 = df2.astype(float)
                df2.to_csv('./killzone.cvs', mode='a', header=False)
                self.__init__()
            # Else just compare the prices normal
            else:
                self.det_killzone(idx)
                idx = idx + 1


killzone = Trader()

killzone.execute()

