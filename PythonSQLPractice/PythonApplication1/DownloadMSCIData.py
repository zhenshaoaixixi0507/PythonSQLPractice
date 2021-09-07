from bs4 import BeautifulSoup
import requests
import json
import os
import pandas as pd
import time

def GetHistoricalDataArray(data):
    price=[]
    date=[]
    for i in range(len(data)):
        price.append(float(data[i]['level_eod']))
        date.append(data[i]['calc_date'])
    return price, date

tickerList=['904000','905600','920800','924600','925000','928000',
            '937200','938000','952800','957800','962000','972400','975200',
            '975600','982600','903600','934400','939200',
            '955400','128680','998100','912400','984000','300400','127200',
            '139899','711886','136613','127300','701536','701425',
            '136619','136625','136626','711887','136627','136621','136624',
            '701519','303000','892000']

endDate="20210831"
startDate="20010131"
dictPrice={}
dictDate={}
OutputNames=[]
for i in range(len(tickerList)):
    r=''
    while r == '':
        try:
            URL_Price = "https://app2.msci.com/products/service/index/indexmaster/getLevelDataForGraph?currency_symbol=USD&index_variant=STRD&start_date="+startDate+"&end_date="+endDate+"&data_frequency=END_OF_MONTH&index_codes="+tickerList[i]
            r = requests.get(URL_Price)
            encodedText = r.text.encode("utf-8")
            soup = BeautifulSoup(encodedText)
            rows=soup.currentTag.currentTag.currentTag.currentTag.text
            data = json.loads(rows)['indexes']['INDEX_LEVELS']
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    price,date=GetHistoricalDataArray(data)
    if len(price)==248:
        dictPrice[tickerList[i]]=price
        dictDate[tickerList[i]]=date
        OutputNames.append(tickerList[i])

df = pd.DataFrame(dictPrice, index =dictDate[tickerList[0]], columns =OutputNames) 
df.to_excel("MSCIData.xlsx") 

print("Finished!")
