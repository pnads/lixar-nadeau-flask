
import os, sys, io
import requests
import py7zr
import threading

import pandas as pd
import numpy as np

from flask import render_template, request, Response, redirect, flash

from lixar_flask import app


URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
ZIP_FILE_PATH = os.path.join(DATA_DIR, '1500000 Sales Records.7z')


@app.route("/")
def index():
    tables, titles = display_table()
    return render_template('index.html', tables=tables, titles=titles)

@app.route("/download")
def download():
    print('Downloading "1500000 Sales Records.7z"...')
    response = requests.get(URL, headers={"User-Agent": "XY"})
    with open(ZIP_FILE_PATH, 'wb') as zf:
        zf.write(response.content)

    return 'success'

@app.route("/process")
def process():
    print('Extracting Data...')
    with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
        for _, bio in zip_file.readall().items():
            df = pd.read_csv(bio)

    print('Making Summary Files...')
    print('--> "region_totals.csv"')
    # Make a summary table by doing a groupby on the region and including some Total columns
    g_total = df.groupby('Region')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()
    df_total = pd.DataFrame(g_total)
    print(df_total)
    df_total += np.random.rand(*df_total.shape) * 10000.0
    print(df_total)
    df_total.to_csv(os.path.join(DATA_DIR, 'region_totals.csv'))
    print('Done.')

    return 'success'

@app.route("/update")
def update():
    tables, titles = display_table()
    return render_template('index.html', tables=tables, titles=titles)

# @app.route("/download")
# def download():
#     download_and_summarize()
#     return 'DONE'

# @app.route("/download/", methods=['POST'])
# @app.route("/download/", methods=['GET','POST'])
# def download():
#     if request.method == 'POST':
#         download_and_summarize()
        
#     return Response(status=200)

# @app.route("/download/", methods=['GET'])
# def download_view():
#     # print('Starting download and summarize process...')
#     # threading.Thread(target=download_and_summarize).start()
#     return render_template('download.html')

# @app.route("/download")
# def download_and_summarize():
#     """
#     Background process to download the .7z file, extract large .csv and create
#     smaller .csv files for the dashboard tables.
#     :return: None
#     """
#     print('Downloading "1500000 Sales Records.7z"...')
#     response = requests.get(URL, headers={"User-Agent": "XY"})
#     with open(ZIP_FILE_PATH, 'wb') as zf:
#         zf.write(response.content)

#     print('Loading Data...')
#     with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
#         for _, bio in zip_file.readall().items():
#             df = pd.read_csv(bio)

#     print('Making Summary Files...')
#     # Make a summary table by doing a groupby on the region and including some Total columns
#     g_total = df.groupby('Region')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()
#     df_total = pd.DataFrame(g_total)
#     df_total.to_csv(os.path.join(DATA_DIR, 'region_totals.csv'))
#     print('Done.')

#     return 'success'

def display_table():
    try:
        df_total = pd.read_csv(os.path.join(DATA_DIR, 'region_totals.csv'))
        df_total = df_total.set_index('Region')
        df_total[['Units Sold']] = df_total[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
        df_total[['Total Revenue', 'Total Cost', 'Total Profit']] = df_total[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
        table_total = df_total.to_html(justify='center', classes=["table", "table-striped", "table-hover", "table-responsive-xl"], header=True)
        table_total = table_total.replace('<thead>', '<thead class="thead-dark">')

        tables = [table_total]
        titles = ['na', 'By Region']
    except Exception as e:
        flash('ERROR: ' + str(e))
        return [], []

    
    return tables, titles