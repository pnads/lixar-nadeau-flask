from flask import Flask

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from .main import *
# from .home.views import *
# from .download.views import *
# from .dashboard.views import *