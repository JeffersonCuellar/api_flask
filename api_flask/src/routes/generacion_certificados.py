from flask import Blueprint,request,jsonify
from datetime import datetime
from utils.db import db
from modulos.GEN_CERTIF import generar_cert as gc




generarCertificados = Blueprint("generarCertificados",__name__)


@generarCertificados.route('/certificados/individual',methods=['POST'])
def get_certificado():
    
    conn1 = db.get_engine(bind='db1')
    conn2 = db.get_engine(bind='db2')

    SOLICITUD =  request.json['SOLICITUD']
    DMEV_ID_TANDA = request.json['ID_TANDA']
    SERIAL_MEDIDOR = request.json['SERIAL_MEDIDOR']

    gc.main_certificado(SOLICITUD,DMEV_ID_TANDA,SERIAL_MEDIDOR,conn1,conn2)
    
    
    return jsonify({"message": "Route Individual Working Successfully"})



@generarCertificados.route('/certificados/masivo',methods=['POST'])
def get_certificados():

    conn1 = db.get_engine(bind='db1')
    conn2 = db.get_engine(bind='db2')

    SOLICITUD =  request.json['SOLICITUD']
    DMEV_ID_TANDA = request.json['ID_TANDA']
    SERIAL_MEDIDOR = None
    

    gc.main_certificado(SOLICITUD,DMEV_ID_TANDA,SERIAL_MEDIDOR,conn1,conn2)
    
    return jsonify({"message": "Route Massive Working Successfully"})


