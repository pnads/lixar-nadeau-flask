
import requests
import io
import py7zr
import os, sys
import pandas as pd
import numpy as np

URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'

ZIP_FILE_PATH = os.path.join('data', '1500000 Sales Records.7z')


# print('DOWNLOADING .7z...')
# response = requests.get(URL, headers={"User-Agent": "XY"})
# with open(ZIP_FILE_PATH, 'wb') as zf:
#     zf.write(response.content)



print('READING DATA...')
with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
    for _, bio in zip_file.readall().items():
        df = pd.read_csv(bio)

print(df.head())

print(df.columns.tolist())

# Make a summary table by doing a groupby on the region and including some Total columns
g_total = df.groupby('Region')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()
df_total = pd.DataFrame(g_total)

df_total += np.random.rand(*df_total.shape) * 10000.0


df_total[['Units Sold']] = df_total[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
df_total[['Total Revenue', 'Total Cost', 'Total Profit']] = df_total[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
table_total = df_total.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
table_total = table_total.replace('<thead>', '<thead class="thead-dark">')


tables = [table_total]
titles = ['na', 'Total']
