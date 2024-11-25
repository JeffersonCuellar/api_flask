from flask import Flask
from routes.datos import datos
from utils.db import db,ma
from config import DATA_CONNECTION_URI



app = Flask(__name__)

app.secret_key = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = DATA_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODOFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

app.register_blueprint(datos)
