from bs4 import BeautifulSoup
import requests
import json
import os
import time

def SortFundsBasedOnValuationMeasures(mode,valuationmeasure):
    #mode="FromLowestToHighest","FromHighestToLowest"
    #valuationmeasure="earnings","sales","book","flow"
    dir_path = os.path.dirname(os.getcwd())
    filename = dir_path+'\\FidelityOver10YrTickers.json'  
    with open(filename,'r') as file_object:  
        data = json.loads(json.load(file_object)) 
    isinList=data['ISINs']

    ratioList={}
   
    for i in range(len(isinList)):
        URL="https://www.fidelity.co.uk/factsheet-data/api/factsheet/"+isinList[str(i)]+"/portfolio"
        r = requests.get(URL)
        encodedText = r.text.encode("utf-8")
        soup = BeautifulSoup(encodedText)
        rows=soup.currentTag.currentTag.currentTag.currentTag.text
        try:
            valuations= json.loads(rows)['valuation']['fund']
            if valuations[valuationmeasure]!="":
                ratioList[isinList[str(i)]]=valuations[valuationmeasure]
        except:
            pass

    if mode=="FromLowestToHighest":
        newRatioList=sorted(ratioList.items(), key=lambda x: x[1])    
    else:
        newRatioList=sorted(ratioList.items(), key=lambda x: x[1],reverse=True)    
    return newRatioList

def SortFundsBasedOnPast3MothPerformance():

    dir_path = os.path.dirname(os.getcwd())
    filename = dir_path+'\\FidelityOver10YrTickers.json'  
    with open(filename,'r') as file_object:  
        data = json.loads(json.load(file_object)) 
    isinList=data['ISINs']

    returnList={}
    oldreturnList={}
    for i in range(len(isinList)):
        r=''
        while r == '':
            try:
                URL="https://www.fidelity.co.uk/factsheet-data/api/factsheet/"+isinList[str(i)]+"/performance"
                r = requests.get(URL)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue
        encodedText = r.text.encode("utf-8")
        soup = BeautifulSoup(encodedText)
        rows=soup.currentTag.currentTag.currentTag.currentTag.text
        try:
            ret=float(json.loads(rows)['timeFrameData'][7]['trailingReturnsValue'])
            oldreturnList[isinList[str(i)]]=ret
        except:
            pass

    returnList=sorted(oldreturnList.items(), key=lambda x: x[1],reverse=True)    
   
    return  returnList

def CalculateFidelityFundReturn(data,ff_factors):
    Price = [float(tempData["Value"]) for tempData in data]
    Returns=[(Price[i+1]/Price[i]-1)*100-float(ff_factors['RF'][i]) for i in range(len(Price)-1)]
    return Returns


#returnList= SortFundsBasedOnPast3MothPerformance()
#print("Finished")

# Pandas to read csv file and other things
import pandas as pd
import pandas_datareader as web
import statsmodels.api as smf
from statsmodels.regression.rolling import RollingOLS
import urllib.request
import zipfile
import matplotlib.pyplot as plt
import seaborn
seaborn.set_style('darkgrid')
pd.plotting.register_matplotlib_converters()

startDate="201107"
endDate="202107"
FidelityendDate='2021-07-31'
FidelitystartDate='2011-06-30'
ff_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_5_Factors_CSV.zip"
urllib.request.urlretrieve(ff_url,'fama_french.zip')
zip_file = zipfile.ZipFile('fama_french.zip', 'r') 
zip_file.extractall() 
zip_file.close()   
os.remove("fama_french.zip")
#os.remove("Developed_5_Factors.csv")
ff_factors = pd.read_csv('Developed_5_Factors.csv', skiprows = 6, index_col = 0)
firstCol=ff_factors.RF.axes[0].values
factors=[]
endstr="Annual Factors: January-December"

for i in range(len(firstCol)):
    tempDate=str(firstCol[i]).strip()
    check4=tempDate!=endstr and tempDate!='nan'
    if check4:
        check1=float(tempDate[0:4])==float(startDate[0:4])
        check2=float(tempDate[4:6])>=float(startDate[4:6])
        check3=float(tempDate[0:4])>=float(startDate[0:4])+1
        if ((check1 and check2) or check3):
            factors.append([1.0,float(ff_factors['Mkt-RF'][i]),float(ff_factors['SMB'][i]),float(ff_factors['HML'][i]),float(ff_factors['RMW'][i]),float(ff_factors['CMA'][i])])
    else:
        break


filename = os.path.dirname(os.getcwd())+'\\FidelityOver10YrTickers.json'  
with open(filename,'r') as file_object:  
    data = json.loads(json.load(file_object)) 
SecIdList=data['SecIds']

URL_Price = "https://lt.morningstar.com/api/rest.svc/timeseries_price/9vehuxllxs?currencyId=GBP&endDate="+FidelityendDate+"&forwardFill=true&frequency=monthly&id="+SecIdList["0"]+"&idType=Morningstar&outputType=json&startDate="+FidelitystartDate#=1900-01-01"
r = requests.get(URL_Price)
encodedText = r.text.encode("utf-8")
soup = BeautifulSoup(encodedText)
rows=soup.currentTag.currentTag.currentTag.currentTag.text
data = json.loads(rows)['TimeSeries']['Security'][0]['HistoryDetail']    
returns=CalculateFidelityFundReturn(data,ff_factors)
rols = RollingOLS(returns, factors, window=36)
rres = rols.fit()
lastTvalue=rres.tvalues[-1][0]
plt.show()
print("Finished!")