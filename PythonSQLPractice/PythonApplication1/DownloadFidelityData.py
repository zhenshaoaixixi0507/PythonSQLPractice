from bs4 import BeautifulSoup
import requests
import json
import os

def GetHistoricalDataArray(data):
    price=[]
    date=[]
    for i in range(len(data)):
        price.append(float(data[i]['Value']))
        date.append(data[i]['EndDate'])
    return price, date


#Get SecId of the selected funds from Fidelity, the funds are ranked with recent 3-month performace
URL = "https://lt.morningstar.com/api/rest.svc/9vehuxllxs/security/screener?page=1&pageSize=100&sortOrder=GBRReturnM3%20desc&outputType=json&version=1&languageId=en-GB&currencyId=GBP&universeIds=FOGBR%24%24ALL_3521&securityDataPoints=SecId%7CName%7CTenforeId%7CholdingTypeId%7Cisin%7Csedol%7CCustomAttributes1%7CCustomAttributes2%7CCustomExternalURL1%7CCustomExternalURL2%7CCustomExternalURL3%7CCustomIsClosed%7CCustomIsFavourite%7CCustomIsRecommended%7CCustomMarketCommentary%7CQR_MonthDate%7CExchangeId%7CExchangeCode%7CCurrency%7CLegalName%7CCustomBuyFee%7CYield_M12%7COngoingCostEstimated%7CCustomCategoryId3Name%7CStarRatingM255%7CQR_GBRReturnM12_5%7CQR_GBRReturnM12_4%7CQR_GBRReturnM12_3%7CQR_GBRReturnM12_2%7CQR_GBRReturnM12_1%7CCustomMinimumPurchaseAmount%7CCustomAdditionalBuyFee%7CCustomSellFee%7CTransactionFeeEstimated%7CPerformanceFee%7CGBRReturnM0%7CGBRReturnM12%7CGBRReturnM36%7CGBRReturnM60%7CGBRReturnM120%7CTrackRecordExtension&filters=&term=&subUniverseId=MFEI"
r = requests.get(URL)
encodedText = r.text.encode("utf-8")
soup = BeautifulSoup(encodedText)
rows=soup.currentTag.currentTag.currentTag.currentTag.text
data = json.loads(rows)
NamesList=[]
IdList=[]
for i in range(len(data['rows'])):
    NamesList.append(data['rows'][i]['LegalName'])
    IdList.append(data['rows'][i]['SecId'])

#Get 10-year historical data
dictPrice={}
dictDate={}
endDate='2021-08-25'
startDate='2011-07-25' #121 months for calculating 120 returns
for i in range(len(IdList)):
    URL_Price = "https://lt.morningstar.com/api/rest.svc/timeseries_price/9vehuxllxs?currencyId=GBP&endDate="+endDate+"&forwardFill=true&frequency=monthly&id="+IdList[i]+"&idType=Morningstar&outputType=json&startDate="+startDate#=1900-01-01"
    r = requests.get(URL_Price)
    encodedText = r.text.encode("utf-8")
    soup = BeautifulSoup(encodedText)
    rows=soup.currentTag.currentTag.currentTag.currentTag.text
    data = json.loads(rows)['TimeSeries']['Security'][0]['HistoryDetail']
    if len(data)==121:
        price,date=GetHistoricalDataArray(data)
        dictPrice[NamesList[i]]=price
        dictDate[NamesList[i]]=date




