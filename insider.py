import pandas as pd
from datetime import datetime
import ssl  #Needed to use pandas read html for some reason
ssl._create_default_https_context = ssl._create_unverified_context

def scrape_to_csv():

    startTime = datetime.now()
    finaldf = pd.DataFrame()
    numPages = 3
    pageScraped = 0
    transaction_types = ['buying', 'sales']
    for t in transaction_types:
        for i in range(numPages):
            url = f"https://www.insidearbitrage.com/insider-{t}/?desk=yes&pagenum={i+1}"
            df = pd.read_html(url)
            df = df[2]  # the desired information is the third element
            columns = df.iloc[0]
            df.columns = columns
            df.drop(columns[0], axis=1, inplace=True)
            df = df[1:]
            if t == 'buying': 
                df['type'] = 'Buy'
            else:
                df['type'] = 'Sell'
            finaldf = pd.concat([finaldf, df])
            pageScraped+=1
            print(f'{pageScraped} Pages Scraped : Total Elapseld time = {datetime.now() - startTime}')

    finaldf.to_csv('./Insider_trade.csv')
    print(f'CSV File Created - Execution Time: {datetime.now() - startTime}')
