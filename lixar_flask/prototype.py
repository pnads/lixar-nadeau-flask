
import requests
import io
import py7zr
import os, sys
import glob
import pandas as pd
import numpy as np

URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'


# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))

ZIP_FILE_PATH = os.path.join('data', '1500000 Sales Records.7z')

# print('DOWNLOADING .7z...')
# response = requests.get(URL, headers={"User-Agent": "XY"})
# with open(ZIP_FILE_PATH, 'wb') as zf:
#     zf.write(response.content)

print('READING DATA...')
try:
    with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
        for _, bio in zip_file.readall().items():
            df = pd.read_csv(bio)
except FileNotFoundError:
    print('Download the file first!')


df_world = pd.DataFrame(df[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()).T
df_world[['Units Sold']] = df_world[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
df_world[['Total Revenue', 'Total Cost', 'Total Profit']] = df_world[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
table_world = df_world.to_html(justify='center', index=False, classes=["table"], header=True)
table_world = table_world.replace('<thead>', '<thead class="thead-dark">')
print(table_world)

print(df.head())

print(df.columns.tolist())

# Make a summary table by doing a groupby on the region and including some Total columns
g_region = df.groupby('Region')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()

df_region = pd.DataFrame(g_region)

df_region += np.random.rand(*df_region.shape) * 10000.0


df_region[['Units Sold']] = df_region[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
df_region[['Total Revenue', 'Total Cost', 'Total Profit']] = df_region[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
table_region = df_region.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
table_region = table_region.replace('<thead>', '<thead class="thead-dark">')

with open(os.path.join(DATA_DIR, 'by_region.html'), 'w') as f:
        f.write(table_region)

with open(os.path.join(DATA_DIR, 'by_region.html'), 'r') as f:
    table_region_read = f.read()

# Make a summary table by doing a groupby on the region and including some Total columns
g_country = df.groupby('Country')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()
df_country = pd.DataFrame(g_country)

df_country += np.random.rand(*df_country.shape) * 10.0

# top 20 countries by profit
df_country_top = df_country.sort_values('Total Profit').head(30).reset_index()
df_country_top['Rank'] = df_country_top.index.values + 1
cols = ['Rank', 'Country', 'Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']
df_country_top = df_country_top[cols]
df_country_top = df_country_top.set_index(['Rank', 'Country'])
df_country_top[['Units Sold']] = df_country_top[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
df_country_top[['Total Revenue', 'Total Cost', 'Total Profit']] = df_country_top[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
table_country = df_country_top.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
table_country = table_country.replace('<thead>', '<thead class="thead-dark">')



tables = [table_region, table_country]
titles = ['na', 'By Region', 'By Country']



data_files = glob.glob('data/*')

for data_file in data_files:
    os.remove(data_file)