from flask import render_template
from lixar_flask import app

@app.route("/")
def home():
    return render_template('home.html')