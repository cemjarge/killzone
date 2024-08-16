import json
import websocket
import pandas as pd
import numpy as np

assets = ['BTCUSDT']

assets = [coin.lower() + '@kline_15m' for coin in assets]

assets = '/'.join(assets)

socket = "wss://stream.binance.com:9443/stream?streams="+assets

def on_message(ws,message):
    message = json.loads(message)
    df_ = manipulation(message)
    df_.to_csv('btc_price.csv', mode='a', header=False)

def manipulation(source):
    curr_price = source['data']['k']['c']
    candle_h = source['data']['k']['h']
    candle_l = source['data']['k']['l']
    epoch_timestamp_ms = source['data']['E'] 
    epoch_timestamp_s = epoch_timestamp_ms / 1000 # Convert the epoch timestamp from milliseconds to seconds
    evt_ts = pd.to_datetime(int(epoch_timestamp_s), unit = 's') # Convert the epoch timestamp to a evt_ts object
    evt_time = evt_ts.time() # Get just the time from epoch timestamp
    total_seconds = (evt_time.hour * 3600) + (evt_time.minute * 60) + evt_time.second # Turn the time into seconds
    candle = {source['data']['s']: curr_price, 'candle high': candle_h, 'candle low': candle_l, 'seconds': total_seconds} # Set the data that we want to have in csv
    df = pd.DataFrame([candle], index = [evt_ts])
    df.index.name = 'timestamp'
    df.reset_index(drop=True)
    df = df.astype(float)
    return df

ws = websocket.WebSocketApp(socket, on_message=on_message)

ws.run_forever()