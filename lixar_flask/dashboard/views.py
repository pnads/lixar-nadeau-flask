import os
import py7zr

import pandas as pd

from flask import render_template
from lixar_flask import app

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'data'))
# ZIP_FILE_PATH = os.path.join(DATA_DIR, '1500000 Sales Records.7z')

@app.route("/dashboard/")
def dashboard():
    
    df_total = pd.read_csv(os.path.join(DATA_DIR, 'region_totals.csv'))
    df_total = df_total.set_index('Region')
    table_total = df_total.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
    table_total = table_total.replace('<thead>', '<thead class="thead-dark">')

    tables = [table_total]
    titles = ['na', 'Total']

    return render_template('dashboard.html', tables=tables, titles=titles)

