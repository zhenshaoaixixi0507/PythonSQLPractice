import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import json
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=server_name;'
                      'Database=database_name;'
                      'Trusted_Connection=yes;')
dir_path = os.path.dirname(os.getcwd())
filename = dir_path+'\\FTSE100Tickers.json'  
with open(filename,'r') as file_object:  
    data = json.loads(json.load(file_object)) 

Tickers=data['Tickers']
tempTicker=Tickers['0']
print('Finished')
