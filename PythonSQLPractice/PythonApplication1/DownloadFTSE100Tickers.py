import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import json

def FindTickers(tables):
    tickers = tables[0].findAll('td', class_='clickable bold-font-weight instrument-tidm gtm-trackable td-with-link')                 
    result=[]
    for i in range(len(tickers)):
        if tickers[i].text[-1]=='.':
            tempText=tickers[i].text+'L'
        else:
            tempText=tickers[i].text
        result.append(tempText)
    return result

def FindDescriptions(tables):
    descriptions = tables[0].findAll('td', class_='clickable instrument-name gtm-trackable td-with-link')
    result=[]
    for i in range(len(descriptions)):
        result.append(descriptions[i].text)
    return result

def AddElements(tickerList,descriptionList,tempTickerList,tempDescriptionList):
    for i in range(len(tempTickerList)):
        tickerList.append(tempTickerList[i])
        descriptionList.append(tempDescriptionList[i])
    return tickerList,descriptionList

tickerList=[]
descriptionList=[]
numOfPages=6
for i in range(numOfPages):
    URL = "https://www.londonstockexchange.com/indices/ftse-100/constituents/table?page="+str(i)
    r = requests.get(URL)
    encodedText = r.text.encode("utf-8")
    soup = BeautifulSoup(encodedText)
    tables =  soup.findAll('table')
    tempTickerList=FindTickers(tables)
    tempDescriptionList=FindDescriptions(tables)
    tickerList,descriptionList=AddElements(tickerList,descriptionList,tempTickerList,tempDescriptionList)

df = pd.DataFrame({'Tickers': tickerList, 'Descriptions': descriptionList}, columns=['Tickers', 'Descriptions'])
jsonFile=df.to_json(orient = 'columns')
dir_path = os.path.dirname(os.getcwd())
filename = dir_path+'\\FTSE100Tickers.json'  
with open(filename, 'w') as file_object: 
    json.dump(jsonFile, file_object)   
print("-----------Finished!----------------")



