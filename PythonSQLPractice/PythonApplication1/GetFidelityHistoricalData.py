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
        price.append(float(data[i]['Value']))
        date.append(data[i]['EndDate'])
    return price, date

filename = os.path.dirname(os.getcwd())+'\\FidelityOver10YrTickers.json'  
with open(filename,'r') as file_object:  
    data = json.loads(json.load(file_object)) 
SecIdList=data['SecIds']
NamesList=data['Names']
#Get 10-year historical data
dictPrice={}
dictDate={}
endDate='2021-08-31'
startDate='2001-01-31' #121 months for calculating 120 returns


OutputNames=[]
for i in range(len(SecIdList)):
    r=''
    while r == '':
        try:
            URL_Price = "https://lt.morningstar.com/api/rest.svc/timeseries_price/9vehuxllxs?currencyId=GBP&endDate="+endDate+"&forwardFill=true&frequency=monthly&id="+SecIdList[str(i)]+"&idType=Morningstar&outputType=json&startDate="+startDate#=1900-01-01"
            r = requests.get(URL_Price)
            encodedText = r.text.encode("utf-8")
            soup = BeautifulSoup(encodedText)
            rows=soup.currentTag.currentTag.currentTag.currentTag.text
            data = json.loads(rows)['TimeSeries']['Security'][0]['HistoryDetail']
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
        dictPrice[NamesList[str(i)]]=price
        dictDate[NamesList[str(i)]]=date
        OutputNames.append(NamesList[str(i)])

df = pd.DataFrame(dictPrice, index =dictDate[NamesList["0"]], columns =OutputNames) 
df.to_excel("FidelityMonthlyData.xlsx") 
print("Finished!")
