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


#returnList= SortFundsBasedOnPast3MothPerformance()
#print("Finished")

# Pandas to read csv file and other things
import pandas as pd
import pandas_datareader as web
import statsmodels.api as smf
import urllib.request
import zipfile
ff_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_5_Factors_CSV.zip"
urllib.request.urlretrieve(ff_url,'fama_french.zip')
zip_file = zipfile.ZipFile('fama_french.zip', 'r') 
zip_file.extractall() 
zip_file.close()   
ff_factors = pd.read_csv('Developed_5_Factors.csv', skiprows = 6, index_col = 0)
startDate="201106"
endDate="202107"
firstCol=ff_factors.RF.axes[0].values
RF=[]
Mkt=[]
SMB=[]
HML=[]
RMW=[]
CMA=[]
endstr="Annual Factors: January-December"

for i in range(len(firstCol)):
    tempDate=str(firstCol[i]).strip()
    check4=tempDate!=endstr and tempDate!='nan'
    if check4:
        check1=float(tempDate[0:4])==float(startDate[0:4])
        check2=float(tempDate[4:6])>=float(startDate[4:6])
        check3=float(tempDate[0:4])>=float(startDate[0:4])+1
        if ((check1 and check2) or check3):
            RF.append(float(ff_factors['RF'][i]))
            Mkt.append(float(ff_factors['Mkt-RF'][i]))
            SMB.append(float(ff_factors['SMB'][i]))
            HML.append(float(ff_factors['HML'][i]))
            RMW.append(float(ff_factors['RMW'][i]))
            CMA.append(float(ff_factors['CMA'][i]))
    else:
        break

    
print("Finished!")