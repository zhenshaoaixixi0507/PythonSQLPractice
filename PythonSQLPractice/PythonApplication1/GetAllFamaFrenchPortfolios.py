import pandas as pd
import pandas_datareader as web
import urllib.request
import zipfile
import os

startDate="201107"
endDate="202107"
ff_url = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_32_Portfolios_ME_BE-ME_OP_2x4x4_CSV.zip"
urllib.request.urlretrieve(ff_url,'fama_french.zip')
zip_file = zipfile.ZipFile('fama_french.zip', 'r') 
zip_file.extractall() 
zip_file.close()   
os.remove("fama_french.zip")
#os.remove("Developed_5_Factors.csv")
