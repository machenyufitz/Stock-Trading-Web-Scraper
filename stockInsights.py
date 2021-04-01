import insider
import sector
import pandas as pd
import pandas_datareader as dr
from datetime import datetime,date,timedelta
startTime = datetime.now()


# insider csv creation 
insider.scrape_to_csv() #uncomment to refresh the csv file
df = pd.read_csv('Insider_trade.csv',index_col = 0)

# sector csv creation
sector.sector_to_csv()

# updating insider csv with additional information
hashmap = {}
periods = 180

def get_info(ticker,n):

    try:
        tickerdf = dr.data.get_data_yahoo(ticker,start = date.today() - timedelta(300) , end = date.today())
        currentprice = tickerdf.iloc[-1]['Close']
        MA = pd.Series(tickerdf['Close'].rolling(n, min_periods=0).mean(), name='MA')
        currentma = MA[-1]
        print(f"data gathered for {ticker}")
        return (currentprice,currentma)
    except:
        return ('na','na')

def prices():
    periods = 180
    for ticker in df.Symbol.unique():
        #hashmap[ticker] = get_info(ticker, periods)
        if ticker not in hashmap.keys():
            hashmap[ticker] = get_info(ticker, periods)
    return hashmap

df['currentprice'] = df.apply (lambda row: prices()[row['Symbol']][0], axis=1)
print("Prices gathered")

df['movingaverage'] = df.apply (lambda row: prices()[row['Symbol']][1], axis=1) 
print("movingaverages gathered")

df.to_csv('Insider_trade.csv')

print(f'Execution Time: {datetime.now() - startTime}')