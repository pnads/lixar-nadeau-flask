from flask import Flask

app = Flask(__name__)

from .home.views import *
from .download.views import *
from .dashboard.views import *