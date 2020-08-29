from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from nlp_core import PoliticClassification

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

pc = None
if pc is None:
    print("init model")
    pc = PoliticClassification()

from app import routes
