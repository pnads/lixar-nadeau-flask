"""Flask App - Main

Defines HTTP Routes and associated logic for this app.
"""

import os
import io
import sys
import requests
import py7zr

import pandas as pd
import numpy as np

from flask import render_template, request

from lixar_flask import app

#-----------------------------------------------------------------------------
# Global Variables
#-----------------------------------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, 'data'))
ZIP_FILE_PATH = os.path.join(DATA_DIR, '1500000 Sales Records.7z')

DATA_URL = 'http://eforexcel.com/wp/wp-content/uploads/2017/07/1500000%20Sales%20Records.7z'

PEPPER_DATA = True    # Add random numbers to data tables

#-----------------------------------------------------------------------------
# Routes
##----------------------------------------------------------------------------
@app.route("/")
def index():
    tables, titles = load_tables()
    return render_template('index.html', tables=tables, titles=titles)

@app.route("/download")
def download():
    """Downloads the compressed data file from the remote server."""

    if not os.path.exists(DATA_DIR):
        print('Making directory "lixar_flask/data/"...')
        os.makedirs(DATA_DIR)

    print('Downloading ' + DATA_URL + '...')
    try:
        response = requests.get(DATA_URL, headers={"User-Agent": "XY"}) # Arbitrary user-agent so download isn't blocked
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: Download failed!')
        return str(e), 500
    print(response)
    # Save the response content as binary to a zip file
    with open(ZIP_FILE_PATH, 'wb') as zf:
        zf.write(response.content)

    return 'success', 200

@app.route("/process")
def process():
    print('Extracting Data...')
    try:
        with py7zr.SevenZipFile(ZIP_FILE_PATH) as zip_file:
            for _, bio in zip_file.readall().items():
                df = pd.read_csv(bio)
    except FileNotFoundError:
        return 'error', 500

    print('Making Summary Files...')
    print('--> "by_region.html"')
    make_table_region(df)
    print('--> "by_country.html"')
    make_table_country(df)
    print('Done.')

    return 'success', 200


#-----------------------------------------------------------------------------
# Helper Functions
#-----------------------------------------------------------------------------
def load_tables():
    """Loads HTML tables as strings.  Returns a list of HTML tables and a 
    list of corresponding titles.

    Returns:
        tables (list): HTML tables as Strings
        titles (list): titles for each table
    """
    error_message = '<p>Uh oh! This table is missing!</p><p>Please click "Download", then "Process", then "Refresh".</p>'

    try:
        with open(os.path.join(DATA_DIR, 'by_region.html'), 'r') as f:
            table_region = f.read()
    except FileNotFoundError:
        table_region = error_message

    try:
        with open(os.path.join(DATA_DIR, 'by_country.html'), 'r') as f:
            table_country = f.read()
    except FileNotFoundError:
        table_country = error_message
       
    tables = [table_region, table_country]
    titles = ['na', 'By Region', 'By Country'] # 'na' is skipped but necessary

    return tables, titles


def make_table_region(df_in):
    """Performs a groupby on df_in by "Region". Generates an HTML table and
    saves to file.

    Args:
        df_in (dataframe): input sales data
    """
    df = df_in.groupby('Region')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()

    if PEPPER_DATA:
        # Pepper the data with random numbers to make it more obvious when the
        # tables have been updated
        df += np.random.rand(*df.shape) * 10000.0

    # Format the table
    df[['Units Sold']] = df[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
    df[['Total Revenue', 'Total Cost', 'Total Profit']] = df[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
    
    # Create HTML file
    table = df.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
    table = table.replace('<thead>', '<thead class="thead-dark">')

    with open(os.path.join(DATA_DIR, 'by_region.html'), 'w') as f:
        f.write(table)

    return

def make_table_country(df_in):
    """Performs a groupby on df_in by "Country". Generates an HTML table and
    saves to file.

    Args:
        df_in (dataframe): input sales data
    """

    df = df_in.groupby('Country')[['Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].sum()

    if PEPPER_DATA:
        # Pepper the data with random numbers to make it more obvious when the
        # tables have been updated
        df += np.random.rand(*df.shape) * 100.0
    
    # Format the table
    df[['Units Sold']] = df[['Units Sold']].applymap(lambda x: "{:,.0f}".format((x)))
    df[['Total Revenue', 'Total Cost', 'Total Profit']] = df[['Total Revenue', 'Total Cost', 'Total Profit']].applymap(lambda x: "${:,.0f}".format((x)))
    
    # Create HTML file
    table = df.to_html(justify='center', classes=["table", "table-striped", "table-hover"], header=True)
    table = table.replace('<thead>', '<thead class="thead-dark">')
    
    with open(os.path.join(DATA_DIR, 'by_country.html'), 'w') as f:
        f.write(table)

    return
