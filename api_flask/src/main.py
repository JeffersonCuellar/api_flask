from flask import Flask
from routes.datos import datos
from routes.generacion_certificados import generarCertificados
from utils.db import db,ma
from config import DATA_CONNECTION_URI, DATA_CONNECTION_SAC
from flask_cors import CORS
from dotenv import load_dotenv
import os



app = Flask(__name__)

CORS(app)
CORS(app,resources={r"/*":{"origins":os.environ['URL_ORIGIN']}})


app.secret_key = 'secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = DATA_CONNECTION_URI
app.config['SQLALCHEMY_BINDS'] = {
    'db1' : DATA_CONNECTION_URI,
    'db2' : DATA_CONNECTION_SAC
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

app.register_blueprint(datos)
app.register_blueprint(generarCertificados)

