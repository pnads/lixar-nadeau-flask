
import requests
import io
import py7zr
import os, sys
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

# # Make a summary table by doing a groupby on the region and including some Total columns
# g_country = df.groupby('Country')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()
# df_country = pd.DataFrame(g_country)

# df_country += np.random.rand(*df_country.shape) * 10.0

# df_country[['Units Sold']] = df_country[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
# df_country[['Total Revenue', 'Total Cost', 'Total Profit']] = df_country[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
# table_country = df_country.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
# table_country = table_country.replace('<thead>', '<thead class="thead-dark">')



tables = [table_region, table_country]
titles = ['na', 'By Region', 'By Country']
