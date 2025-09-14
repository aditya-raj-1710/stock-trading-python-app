import os
from dotenv import load_dotenv
import requests
import time
import csv

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
TIME_DELAY = 30

url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'

tickers = []

is_data_present = True

while is_data_present:
    response = requests.get(url)
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)
    if 'next_url' in data:
        url = data['next_url'] + f'&apiKey={POLYGON_API_KEY}'
        time.sleep(TIME_DELAY)
    else:
        is_data_present = False

print(len(tickers))

example_ticker =  {'ticker': 'ZWS', 
	'name': 'Zurn Elkay Water Solutions Corporation', 
	'market': 'stocks', 
	'locale': 'us', 
	'primary_exchange': 'XNYS', 
	'type': 'CS', 
	'active': True, 
	'currency_name': 'usd', 
	'cik': '0001439288', 
	'composite_figi': 'BBG000H8R0N8', 	'share_class_figi': 'BBG001T36GB5', 	'last_updated_utc': '2025-09-11T06:11:10.586204443Z'}

# Write tickers to CSV with example_ticker schema
fieldnames = list(example_ticker.keys())
output_csv = 'tickers.csv'
with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for t in tickers:                       
        row = {key: t.get(key, '') for key in fieldnames}
        writer.writerow(row)
print(f'Wrote {len(tickers)} rows to {output_csv}')
