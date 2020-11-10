
import requests
import io
import py7zr
import os, sys
import pandas as pd

URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'

ZIP_FILE_PATH = os.path.join('data', '1500000 Sales Records.7z')


print('DOWNLOADING .7z...')
response = requests.get(URL, headers={"User-Agent": "XY"})
with open(ZIP_FILE_PATH, 'wb') as zf:
    zf.write(response.content)



print('READING DATA...')
with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
    for _, bio in zip_file.readall().items():
        df = pd.read_csv(bio)

print(df.head())

print(df.columns.tolist())

g = df.groupby('Region')['Total Profit'].sum()
g_df = pd.DataFrame(g)
g_df_html = g_df.to_html()

