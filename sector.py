import pandas as pd
from datetime import datetime,date,timedelta



def sector_to_csv():

    startTime = datetime.now()
    df = pd.read_html("https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/")
    sectorList = []
    for i in df[0]['Unnamed: 0']:
        i = i.replace(' ','-')
        i = i.replace('&','')
        i = i.replace(':','')
        i = i.replace('/','-')
        i = i.replace('--','-')
        i = i.lower()
        sectorList.append(i)


    sectorDict = {}
    for i in sectorList:
        url = f"https://www.tradingview.com/markets/stocks-usa/sectorandindustry-industry/{i}"
        db = pd.read_html(url)
        for stock in db[0]['Unnamed: 0']:
            ticker = stock[:4].strip()
            ticker = ticker.replace(" ", "")
            ticker = ticker.replace(".", "")
            sectorDict[ticker] = i
        print(f"Finished Scraping: {i}")



    finaldf = pd.DataFrame.from_dict(sectorDict, orient = "index")
    finaldf.to_csv('StockSectors.csv')
    
    print(f'Sector CSV File Creation time: {datetime.now() - startTime}')

#sector_to_csv()