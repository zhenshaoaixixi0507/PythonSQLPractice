# Pandas to read csv file and other things
import pandas as pd
import pandas_datareader as web
import urllib.request
import zipfile

startDate="201107"
endDate="202107"
ff_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_5_Factors_CSV.zip"
urllib.request.urlretrieve(ff_url,'fama_french.zip')
zip_file = zipfile.ZipFile('fama_french.zip', 'r') 
zip_file.extractall() 
zip_file.close()   
os.remove("fama_french.zip")
#os.remove("Developed_5_Factors.csv")
ff_factors = pd.read_csv('Developed_5_Factors.csv', skiprows = 6, index_col = 0)
firstCol=ff_factors.RF.axes[0].values
RF=[]
Mkt=[]
SMB=[]
HML=[]
RMW=[]
CMA=[]
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
            RF.append(float(ff_factors['RF'][i]))
            Mkt.append(float(ff_factors['Mkt-RF'][i]))
            SMB.append(float(ff_factors['SMB'][i]))
            HML.append(float(ff_factors['HML'][i]))
            RMW.append(float(ff_factors['RMW'][i]))
            CMA.append(float(ff_factors['CMA'][i]))
            #factors.append([1.0,float(ff_factors['Mkt-RF'][i]),float(ff_factors['SMB'][i]),float(ff_factors['HML'][i]),float(ff_factors['RMW'][i]),float(ff_factors['CMA'][i])])
    else:
        break
