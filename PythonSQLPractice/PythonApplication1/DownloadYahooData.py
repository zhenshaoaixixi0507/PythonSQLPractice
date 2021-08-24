import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import json

dir_path = os.path.dirname(os.getcwd())
filename = dir_path+'\\FTSE100Tickers.json'  
with open(filename,'r') as file_object:  
    data = json.loads(json.load(file_object)) 

Tickers=data['Tickers']

print('Finished')
