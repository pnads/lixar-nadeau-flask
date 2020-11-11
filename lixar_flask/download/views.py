import os, sys, io
import requests
import py7zr
import threading

import pandas as pd

from flask import render_template

from lixar_flask import app


URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'data'))
ZIP_FILE_PATH = os.path.join(DATA_DIR, '1500000 Sales Records.7z')



@app.route("/download/")
def download():
    print('Starting download and summarize process...')
    threading.Thread(target=download_and_summarize).start()
    return render_template('download.html')

def download_and_summarize():
    """
    Background process to download the .7z file, extract large .csv and create
    smaller .csv files for the dashboard tables.
    :return: None
    """
    print('Downloading "1500000 Sales Records.7z"...')
    response = requests.get(URL, headers={"User-Agent": "XY"})
    with open(ZIP_FILE_PATH, 'wb') as zf:
        zf.write(response.content)

    print('Loading Data...')
    with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
        for _, bio in zip_file.readall().items():
            df = pd.read_csv(bio)

    print('Making Summary Files...')
    # Make a summary table by doing a groupby on the region and including some Total columns
    g_total = df.groupby('Region')[['Total Revenue', 'Total Cost', 'Total Profit']].sum()
    df_total = pd.DataFrame(g_total)
    df_total.to_csv(os.path.join(DATA_DIR, 'region_totals.csv'))
    print('Done.')

    return
