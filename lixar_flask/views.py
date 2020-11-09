from lixar_flask import app

@app.route("/")
def home_view():
    return "<h1>Hello world!</h1>"