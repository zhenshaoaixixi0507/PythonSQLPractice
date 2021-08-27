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


returnList= SortFundsBasedOnPast3MothPerformance()
print("Finished")
