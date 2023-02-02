import csv
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import math
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(executable_path=r'C:\Users\Michael\OneDrive\Projects\chromedriver_win32\chromedriver.exe', options=options)

price_guide = "https://prices.tcgplayer.com/price-guide/yugioh/"
collection = pd.read_csv("collection.csv").dropna(axis='columns')
collection = collection[['Set Name', 'Set Number']].rename(columns={"Set Number": "Number"})

sets = collection["Set Name"].unique()
card_list = []
updated_price = []
for set in sets:
    search_df = collection[collection["Set Name"]==set]
    driver.get(price_guide + set)

    # GET TABLE FROM tcgplayer
    price_df = pd.read_html(driver.page_source)[0]

    # Match cards from searchdf to pricedf
    match_df = pd.merge(search_df, price_df, on=['Number'], how='inner')

    # Add new results to outputdf
    if len(match_df['Number']) != len(search_df['Number']):
        match_df = match_df.drop_duplicates(subset=['Number'], keep='first')

    card_list.extend(list(match_df['Number']))
    updated_price.extend(list(match_df['Market Price']))

    updated = {'Set number': card_list, 'Value': updated_price}
    output_df = pd.DataFrame(data=updated,index=None)
    output_df.to_csv('updated.csv')

# Convert outputdf to CSV
'''
updated = {'Set number': card_list, 'Value': updated_price}
output_df = pd.DataFrame(data=updated,index=None)
output_df.to_csv('updated.csv')
'''
