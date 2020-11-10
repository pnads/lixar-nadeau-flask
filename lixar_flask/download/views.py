from flask import render_template
from lixar_flask import app

@app.route("/download/")
def download():
    return render_template('download.html')