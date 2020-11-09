from lixar_flask import app

@app.route("/")
def home_view():
    return "<h1>Home</h1>"

@app.route("/download/")
def download_view():
    return "<h1>Download</h1>"


@app.route("/dashboard/")
def dashboard_view():
    return "<h1>Dashboard</h1>"