import os
import py7zr

import pandas as pd

from flask import render_template
from lixar_flask import app

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'data'))
ZIP_FILE_PATH = os.path.join(DATA_DIR, '1500000 Sales Records.7z')

@app.route("/dashboard/")
def dashboard():
    table = summary_html()
    return render_template('dashboard.html', table=table)

def summary_html():
    df = read_data()
    g = df.groupby('Region')['Total Profit'].sum()
    g_df = pd.DataFrame(g)
    g_df_html = g_df.to_html()
    return g_df_html

def read_data():
    print('READING DATA...')
    with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
        for _, bio in zip_file.readall().items():
            df = pd.read_csv(bio)

    return df

if __name__ == '__main__':
    print(summary_html())