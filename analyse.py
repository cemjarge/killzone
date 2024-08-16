import pandas as pd

df = pd.read_csv('killzone.csv', names = ['date', 'asia_high', 'asia_low', 'london_open_high', 'london_open_low', 'new_york_high', 'new_york_low', 'london_close_high', 'london_close_low', 
                                                     'new_york_mo', 'eight_thirty'])

idx = 0



for i in range(df.shape[0]):
    row_data = df.iloc[idx]
    if row_data['asia_high'] >= row_data['london_open_high'] and row_data['asia_low'] <= row_data['london_open_low']:
        print(row_data['date'])
    idx = idx + 1