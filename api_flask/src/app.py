from datetime import datetime
from flask import Flask,request,jsonify, session
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+oracledb://SEFMEC:g3SQOuK*blQvBTs5@CENS-TO11:1522/ORADBVARIAS'
app.config['SQLAlchemy_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
ma = Marshmallow(app)



#Esquema tabla normas
class SEF_TNORMAS(db.Model):
    NORN_ID_NORMA = db.Column(db.Integer,primary_key=True)
    NORV_CODIGO_NORMA = db.Column(db.String(50))
    NORV_DETALLE = db.Column(db.String(500))

    def __init__(self,NORN_ID_NORMA, NORV_CODIGO_NORMA, NORV_DETALLE):
        self.NORN_ID_NORMA = NORN_ID_NORMA
        self.NORV_CODIGO_NORMA = NORV_CODIGO_NORMA
        self.NORV_DETALLE = NORV_DETALLE
        db.create_all()

class NormaSchema(ma.Schema):
    class Meta:
        fields = ('NORN_ID_NORMA','NORV_CODIGO_NORMA','NORV_DETALLE','NORV_COMENTARIOS','DMEV_USUARIO_CREACION','DMEV_USUARIO_ACTUALIZACION','DMED_FECHA_CREACION','DMED_FECHA_ACTUALIZACION')

norma_schema = NormaSchema()
normas_schema = NormaSchema(many=True)

#Esquema tabla ensayos
class SEF_TENSAYOS(db.Model):
    ENSN_ID_ENSAYO = db.Column(db.Integer,primary_key=True)
    ENSV_TIPO_ENSAYO = db.Column(db.String(100))
    ENSV_METODO_UNO = db.Column(db.String(100))
    ENSV_METODO_DOS = db.Column(db.String(100))
    ENSV_METODO_TRES = db.Column(db.String(100))
    ENSV_COMENTARIOS = db.Column(db.String(500))
    OPCNV_USUARIO_CREACION = db.Column(db.String(45))
    OPCNV_USUARIO_ACTUALIZACION = db.Column(db.String(45))
    OPCND_FECHA_CREACION = db.Column(db.Date)
    OPCND_FECHA_ACTUALIZACION = db.Column(db.Date)

    def __init__(self,ENSV_TIPO_ENSAYO,ENSV_METODO_UNO, ENSV_METODO_DOS):
        self.ENSV_TIPO_ENSAYO = ENSV_TIPO_ENSAYO
        self.ENSV_METODO_UNO = ENSV_METODO_UNO
        self.ENSV_METODO_DOS = ENSV_METODO_DOS
        db.create_all()


class EnsayoSchema(ma.Schema):
    class Meta:
        fields = ('ENSN_ID_ENSAYO','ENSV_TIPO_ENSAYO','ENSV_METODO_UNO','ENSV_METODO_DOS','ENSV_METODO_TRES','ENSV_COMENTARIOS','OPCNV__USUARIO_CREACION','OPCNV__USUARIO_ACTUALIZACION','OPCND_FECHA_CREACION','OPCND_FECHA_ACTUALIZACION')

ensayo_schema = EnsayoSchema()
ensayos_schema = EnsayoSchema(many=True)

#Esquema tabla sesiones
class SEF_TSESSION(db.Model):


    SESN_ID_TANDA = db.Column(db.Integer,primary_key=True)
    SESD_FECHA_INICIO = db.Column(db.Date)
    SESD_FECHA_FIN = db.Column(db.Date)
    SESV_CALIBRADOR = db.Column(db.String(50))  
    SESN_TEMPERATURA = db.Column(db.Float)
    EQUN_ID_EPM = db.Column(db.Integer)
    SESV_TIPO_DE_ENERGIA = db.Column(db.String(20))
    SESV_FLUJO_ENERGIA = db.Column(db.String(20))
    SESN_TENSION_PRUEBA = db.Column(db.Float)
    SESN_CORRIENTE_PRUEBA_NOM = db.Column(db.Float)
    SESN_CORRIENTE_PRUEBA_MAX = db.Column(db.Float)
    SESV_METODO_FUNCIONAMIENTO_SC = db.Column(db.String(100))
    SESV_METODO_ARRANQUE = db.Column(db.String(100))
    SESV_METODO_EXACTITUD = db.Column(db.String(100))
    SESV_METODO_VERIFICACION_CONST = db.Column(db.String(100))


    def __init__(self,SESN_ID_TANDA,SESD_FECHA_INICIO,SESD_FECHA_FIN,SESV_CALIBRADOR,SESN_TEMPERATURA,EQUN_ID_EPM,SESV_TIPO_DE_ENERGIA,SESV_FLUJO_ENERGIA,SESN_TENSION_PRUEBA,SESN_CORRIENTE_PRUEBA_NOM,SESN_CORRIENTE_PRUEBA_MAX,SESV_METODO_FUNCIONAMIENTO_SC,SESV_METODO_ARRANQUE,SESV_METODO_EXACTITUD,SESV_METODO_VERIFICACION_CONST):
        self.SESN_ID_TANDA = SESN_ID_TANDA
        self.SESD_FECHA_INICIO = SESD_FECHA_INICIO
        self.SESD_FECHA_FIN = SESD_FECHA_FIN
        self.SESV_CALIBRADOR = SESV_CALIBRADOR
        self.SESN_TEMPERATURA = SESN_TEMPERATURA
        self.EQUN_ID_EPM = EQUN_ID_EPM
        self.SESV_TIPO_DE_ENERGIA = SESV_TIPO_DE_ENERGIA
        self.SESV_FLUJO_ENERGIA = SESV_FLUJO_ENERGIA
        self.SESN_TENSION_PRUEBA = SESN_TENSION_PRUEBA
        self.SESN_CORRIENTE_PRUEBA_NOM = SESN_CORRIENTE_PRUEBA_NOM
        self.SESN_CORRIENTE_PRUEBA_MAX = SESN_CORRIENTE_PRUEBA_MAX
        self.SESV_METODO_FUNCIONAMIENTO_SC = SESV_METODO_FUNCIONAMIENTO_SC
        self.SESV_METODO_ARRANQUE = SESV_METODO_ARRANQUE
        self.SESV_METODO_EXACTITUD = SESV_METODO_EXACTITUD
        self.SESV_METODO_VERIFICACION_CONST = SESV_METODO_VERIFICACION_CONST

class SesionSchema(ma.Schema):
    class Meta:
        fields = ('SESN_ID_TANDA','SESD_FECHA_INICIO','SESD_FECHA_FIN','SESV_CALIBRADOR','SESN_TEMPERATURA','EQUN_ID_EPM','SESV_TIPO_DE_ENERGIA','SESV_FLUJO_ENERGIA','SESN_TENSION_PRUEBA','SESN_CORRIENTE_PRUEBA_NOM','SESN_CORRIENTE_PRUEBA_MAX','SESV_METODO_FUNCIONAMIENTO_SC','SESV_METODO_ARRANQUE','SESV_METODO_EXACTITUD','SESV_METODO_VERIFICACION_CONST')

sesion_schema = SesionSchema()
sesions_schema = SesionSchema(many=True)

#Esquema tabla medidores

class SEF_TDATOS_MEDIDORES(db.Model):

    

    DMEV_ID_SERIAL = db.Column(db.Integer,primary_key=True,autoincrement=True)
    DMEV_ID_TANDA = db.Column(db.Integer)
    DMEV_SERIAL = db.Column(db.String(30))
    DMEV_MARCA = db.Column(db.String(20))
    DMEV_MODELO = db.Column(db.String(25))
    DMEV_CONSTRUCCION = db.Column(db.String(20))
    DMEV_TIPO_DE_ENERGIA = db.Column(db.String(15))
    DMEV_CLASE = db.Column(db.String(10))
    DMEV_TIPO_CONEXION = db.Column(db.String(20))
    DMEV_FABRICACION = db.Column(db.String(20))
    DMEV_VOLTAJE_NOMINAL = db.Column(db.Float)
    DMEV_CORRIENTE_NOMINAL = db.Column(db.Float)
    DMEV_CORRIENTE_MAXIMA = db.Column(db.Float)
    DMEV_CONSTANTE = db.Column(db.Float)
    DMEN_RESOLUCION_MEDIDOR = db.Column(db.String(5))

    


    def __init__(self,DMEV_ID_TANDA,DMEV_SERIAL, DMEV_MARCA, DMEV_MODELO, DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_CLASE,DMEV_TIPO_CONEXION,DMEV_FABRICACION,DMEV_VOLTAJE_NOMINAL,DMEV_CORRIENTE_NOMINAL,DMEV_CORRIENTE_MAXIMA,DMEV_CONSTANTE,DMEN_RESOLUCION_MEDIDOR):
        
        self.DMEV_ID_TANDA = DMEV_ID_TANDA
        self.DMEV_SERIAL = DMEV_SERIAL
        self.DMEV_MARCA = DMEV_MARCA
        self.DMEV_MODELO = DMEV_MODELO
        self.DMEV_CONSTRUCCION = DMEV_CONSTRUCCION
        self.DMEV_TIPO_DE_ENERGIA = DMEV_TIPO_DE_ENERGIA
        self.DMEV_CLASE = DMEV_CLASE
        self.DMEV_TIPO_CONEXION = DMEV_TIPO_CONEXION
        self.DMEV_FABRICACION = DMEV_FABRICACION
        self.DMEV_VOLTAJE_NOMINAL = DMEV_VOLTAJE_NOMINAL
        self.DMEV_CORRIENTE_NOMINAL = DMEV_CORRIENTE_NOMINAL
        self.DMEV_CORRIENTE_MAXIMA = DMEV_CORRIENTE_MAXIMA
        self.DMEV_CONSTANTE = DMEV_CONSTANTE
        self.DMEN_RESOLUCION_MEDIDOR = DMEN_RESOLUCION_MEDIDOR




class MedidorSchema(ma.Schema):
    class Meta:
        fields = ('DMEV_ID_SERIAL','DMEV_ID_TANDA', 'DMEV_SERIAL', 'DMEV_MARCA', 'DMEV_MODELO', 'DMEV_CONSTRUCCION', 'DMEV_TIPO_DE_ENERGIA', 'DMEV_CLASE', 'DMEV_TIPO_CONEXION', 'DMEV_FABRICACION', 'DMEV_VOLTAJE_NOMINA', 'DMEV_CORRIENTE_NOMINAL', 'DMEV_CORRIENTE_MAXIMA', 'DMEV_CONSTANTE', 'DMEV_RESOLUCION_MEDIDOR')



medidor_schema = MedidorSchema()
medidores_schema = MedidorSchema(many=True)

        
#Esquema tabla opciones_norma

class SEF_TOPCIONES_NORMA(db.Model):
    OPCNN_ID = db.Column(db.Integer,primary_key=True)
    SESN_ID_TANDA = db.Column(db.Integer)
    DMEV_CONSTRUCCION = db.Column(db.String(20))
    DMEV_TIPO_DE_ENERGIA = db.Column(db.String(20))
    DMEV_FABRICACION = db.Column(db.String(20))
    DMEV_TIPO_CONEXION = db.Column(db.String(20))
    OPCNN_ID_NORMA =  db.Column(db.Integer)
    OPCNN_CANT_PUNTOS_CARGA = db.Column(db.Integer)


    def __init__(self,SESN_ID_TANDA,DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_FABRICACION,DMEV_TIPO_CONEXION):
        self.SESN_ID_TANDA = SESN_ID_TANDA
        self.DMEV_CONSTRUCCION = DMEV_CONSTRUCCION 
        self.DMEV_TIPO_DE_ENERGIA = DMEV_TIPO_DE_ENERGIA 
        self.DMEV_FABRICACION = DMEV_FABRICACION
        self.DMEV_TIPO_CONEXION = DMEV_TIPO_CONEXION
        db.create_all()


class OpNormaSchema(ma.Schema):
    class Meta:
        fields=('OPCNN_ID','SESN_ID_TANDA','DMEV_CONSTRUCCION','DMEV_TIPO_DE_ENERGIA','DMEV_FABRICACION','DMEV_TIPO_CONEXION','OPCNN_ID_NORMA','OPCNN_CANT_PUNTOS_CARGA','OPCNV_COMENTARIOS','OPCNV_USUARIO_CREACION','OPCNV_USUARIO_ACTUALIZACION','OPCND_FECHA_CREACION','OPCND_FECHA_ACTUALIZACION')

        
# Esquema tabla mediciones

class SEF_TMEDICIONES(db.Model):
    MEDN_ID_MEDICIONES = db.Column(db.Integer,primary_key=True)
    DMEN_ID_SERIAL = db.Column(db.Integer)
    MEDV_VACIO = db.Column(db.String(8))
    MEDV_ARRANQUE = db.Column(db.String(8))
    MEDN_IMIN_RST_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_IMIN_RST_1_DESV_EST = db.Column(db.Float)
    MEDN_5_RST_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_5_RST_1_DESV_EST = db.Column(db.Float)
    MEDN_100_RST_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_RST_1_DESV_EST = db.Column(db.Float)
    MEDN_100_R_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_R_1_DESV_EST = db.Column(db.Float)
    MEDN_100_S_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_S_1_DESV_EST = db.Column(db.Float)
    MEDN_100_T_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_T_1_DESV_EST = db.Column(db.Float)
    MEDN_100_RST_0_5I_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_RST_0_5I_DESV_EST = db.Column(db.Float)
    MEDN_100_RST_0_8C_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_RST_0_8C_DESV_EST = db.Column(db.Float)
    MEDN_100_RST_0_5C_VALOR_MEDIO = db.Column(db.Float)
    MEDN_100_RST_0_5C_DESV_EST = db.Column(db.Float)
    MEDN_MAX_RST_1_VALOR_MEDIO = db.Column(db.Float)
    MEDN_MAX_RST_1_DESV_EST = db.Column(db.Float)
    MEDN_LECTURA_INICIAL_UNO = db.Column(db.Float)
    MEDN_LECTURA_FINAL_UNO = db.Column(db.Float)
    MEDN_ENERGIA_APLICADA_UNO = db.Column(db.Float)
    MEDN_LECTURA_INICIAL_DOS = db.Column(db.Float)
    MEDN_LECTURA_FINAL_DOS = db.Column(db.Float)
    MEDN_ENERGIA_APLICADA_DOS = db.Column(db.Float)
    MEDN_LECTURA_INICIAL_TRES = db.Column(db.Float)
    MEDN_LECTURA_FINAL_TRES = db.Column(db.Float)
    MEDN_ENERGIA_APLICADA_TRES = db.Column(db.Float)


    def __init__(self, DMEN_ID_SERIAL,MEDV_VACIO,MEDV_ARRANQUE,MEDN_IMIN_RST_1_VALOR_MEDIO, MEDN_IMIN_RST_1_DESV_EST, MEDN_5_RST_1_VALOR_MEDIO, MEDN_5_RST_1_DESV_EST, MEDN_100_RST_1_VALOR_MEDIO, MEDN_100_RST_1_DESV_EST, MEDN_100_R_1_VALOR_MEDIO, MEDN_100_R_1_DESV_EST, MEDN_100_S_1_VALOR_MEDIO, MEDN_100_S_1_DESV_EST, MEDN_100_T_1_VALOR_MEDIO, MEDN_100_T_1_DESV_EST, MEDN_100_RST_0_5I_VALOR_MEDIO, MEDN_100_RST_0_5I_DESV_EST, MEDN_100_RST_0_8C_VALOR_MEDIO, MEDN_100_RST_0_8C_DESV_EST, MEDN_100_RST_0_5C_VALOR_MEDIO, MEDN_100_RST_0_5C_DESV_EST, MEDN_MAX_RST_1_VALOR_MEDIO, MEDN_MAX_RST_1_DESV_EST, MEDN_LECTURA_INICIAL_UNO, MEDN_LECTURA_FINAL_UNO, MEDN_ENERGIA_APLICADA_UNO, MEDN_LECTURA_INICIAL_DOS, MEDN_LECTURA_FINAL_DOS, MEDN_ENERGIA_APLICADA_DOS, MEDN_LECTURA_INICIAL_TRES, MEDN_LECTURA_FINAL_TRES, MEDN_ENERGIA_APLICADA_TRES):

        
        self.DMEN_ID_SERIAL = DMEN_ID_SERIAL
        self.MEDV_VACIO = MEDV_VACIO
        self.MEDV_ARRANQUE = MEDV_ARRANQUE
        self.MEDN_IMIN_RST_1_VALOR_MEDIO = MEDN_IMIN_RST_1_VALOR_MEDIO
        self.MEDN_IMIN_RST_1_DESV_EST = MEDN_IMIN_RST_1_DESV_EST
        self.MEDN_5_RST_1_VALOR_MEDIO = MEDN_5_RST_1_VALOR_MEDIO
        self.MEDN_5_RST_1_DESV_EST = MEDN_5_RST_1_DESV_EST
        self.MEDN_100_RST_1_VALOR_MEDIO = MEDN_100_RST_1_VALOR_MEDIO
        self.MEDN_100_RST_1_DESV_EST = MEDN_100_RST_1_DESV_EST
        self.MEDN_100_R_1_VALOR_MEDIO = MEDN_100_R_1_VALOR_MEDIO
        self.MEDN_100_R_1_DESV_EST = MEDN_100_R_1_DESV_EST
        self.MEDN_100_S_1_VALOR_MEDIO = MEDN_100_S_1_VALOR_MEDIO
        self.MEDN_100_S_1_DESV_EST = MEDN_100_S_1_DESV_EST
        self.MEDN_100_T_1_VALOR_MEDIO = MEDN_100_T_1_VALOR_MEDIO
        self.MEDN_100_T_1_DESV_EST = MEDN_100_T_1_DESV_EST
        self.MEDN_100_RST_0_5I_VALOR_MEDIO = MEDN_100_RST_0_5I_VALOR_MEDIO
        self.MEDN_100_RST_0_5I_DESV_EST = MEDN_100_RST_0_5I_DESV_EST
        self.MEDN_100_RST_0_8C_VALOR_MEDIO = MEDN_100_RST_0_8C_VALOR_MEDIO
        self.MEDN_100_RST_0_8C_DESV_EST = MEDN_100_RST_0_8C_DESV_EST
        self.MEDN_100_RST_0_5C_VALOR_MEDIO = MEDN_100_RST_0_5C_VALOR_MEDIO
        self.MEDN_100_RST_0_5C_DESV_EST = MEDN_100_RST_0_5C_DESV_EST
        self.MEDN_MAX_RST_1_VALOR_MEDIO = MEDN_MAX_RST_1_VALOR_MEDIO
        self.MEDN_MAX_RST_1_DESV_EST = MEDN_MAX_RST_1_DESV_EST
        self.MEDN_LECTURA_INICIAL_UNO = MEDN_LECTURA_INICIAL_UNO
        self.MEDN_LECTURA_FINAL_UNO = MEDN_LECTURA_FINAL_UNO
        self.MEDN_ENERGIA_APLICADA_UNO = MEDN_ENERGIA_APLICADA_UNO
        self.MEDN_LECTURA_INICIAL_DOS = MEDN_LECTURA_INICIAL_DOS
        self.MEDN_LECTURA_FINAL_DOS = MEDN_LECTURA_FINAL_DOS
        self.MEDN_ENERGIA_APLICADA_DOS = MEDN_ENERGIA_APLICADA_DOS
        self.MEDN_LECTURA_INICIAL_TRES = MEDN_LECTURA_INICIAL_TRES
        self.MEDN_LECTURA_FINAL_TRES = MEDN_LECTURA_FINAL_TRES
        self.MEDN_ENERGIA_APLICADA_TRES = MEDN_ENERGIA_APLICADA_TRES





    class MedicionSchema(ma.Schema):
        class Meta:
            fields = ('DMEN_ID_SERIAL','MEDV_VACIO','MEDV_ARRANQUE','MEDN_IMIN_RST_1_VALOR_MEDIO', 'MEDN_IMIN_RST_1_DESV_EST', 'MEDN_5_RST_1_VALOR_MEDIO', 'MEDN_5_RST_1_DESV_EST', 'MEDN_100_RST_1_VALOR_MEDIO', 'MEDN_100_RST_1_DESV_EST', 'MEDN_100_R_1_VALOR_MEDIO', 'MEDN_100_R_1_DESV_EST', 'MEDN_100_S_1_VALOR_MEDIO', 'MEDN_100_S_1_DESV_EST', 'MEDN_100_T_1_VALOR_MEDIO', 'MEDN_100_T_1_DESV_EST', 'MEDN_100_RST_0_5I_VALOR_MEDIO', 'MEDN_100_RST_0_5I_DESV_EST', 'MEDN_100_RST_0_8C_VALOR_MEDIO', 'MEDN_100_RST_0_8C_DESV_EST', 'MEDN_100_RST_0_5C_VALOR_MEDIO', 'MEDN_100_RST_0_5C_DESV_EST', 'MEDN_MAX_RST_1_VALOR_MEDIO', 'MEDN_MAX_RST_1_DESV_EST', 'MEDN_LECTURA_INICIAL_UNO', 'MEDN_LECTURA_FINAL_UNO', 'MEDN_ENERGIA_APLICADA_UNO', 'MEDN_LECTURA_INICIAL_DOS', 'MEDN_LECTURA_FINAL_DOS', 'MEDN_ENERGIA_APLICADA_DOS', 'MEDN_LECTURA_INICIAL_TRES', 'MEDN_LECTURA_FINAL_TRES', 'MEDN_ENERGIA_APLICADA_TRES', 'MEDV_COMENTARIOS', 'MEDV_USUARIO_CREACION','MEDV_USUARIO_ACTUALIZACION', 'MEDD_FECHA_CREACION','MEDD_FECHA_ACTUALIZACION')

medicion_schema = MedidorSchema()
mediones_schema = MedidorSchema(many=True)










@app.route('/') 
def index():
    return jsonify({"message":"API Working Successfully"})



# @app.route('/normas/insertarNorma',methods=['POST'])
# def create_tnormas():

#     #Inserción en SEF_TNORMAS
#     NORN_ID_NORMA=request.json['id_norma']
#     NORV_CODIGO_NORMA = request.json['codigo_norma']
#     NORV_DETALLE = request.json['detalle'][1]['detalle 2']
#     new_norma = SEF_TNORMAS(NORN_ID_NORMA, NORV_CODIGO_NORMA, NORV_DETALLE)

#     # #Inserción en SEF_TENSAYOS
#     # ENSV_TIPO_ENSAYO = request.json['tipo_ensayo']
#     # ENSV_METODO_UNO = request.json['metodo_uno']
#     # ENSV_METODO_DOS = request.json['metodo_dos']
#     # new_ensayo = SEF_TENSAYOS(ENSV_TIPO_ENSAYO, ENSV_METODO_UNO, ENSV_METODO_DOS)



#     db.session.add(new_norma)
#     # db.session.add(new_ensayo)
#     db.session.commit()

#     return jsonify({"message":"data inserted successfully"})

@app.route('/normas/insertarDatosJson',methods=['POST'])
def insertar_datos():

    #Inserción en SEF_TSESSION
    SESN_ID_TANDA = request.json['SESSION']['ID_TANDA']
    SESD_FECHA_INICIO_str = request.json['SESSION']['FECHA_INICIO']
    SESD_FECHA_FIN_str = request.json['SESSION']['FECHA_FIN']
    SESV_CALIBRADOR = request.json['SESSION']['CALIBRADOR']
    SESN_TEMPERATURA = request.json['SESSION']['TEMPERATURA']
    EQUN_ID_EPM = request.json['SESSION']['ID_EPM']
    SESV_TIPO_DE_ENERGIA = request.json['SESSION']['TIPO_DE_ENERGIA']
    SESV_FLUJO_ENERGIA = request.json['SESSION']['FLUJO_ENERGIA']
    SESN_TENSION_PRUEBA = request.json['SESSION']['TENSION_PRUEBA']
    SESN_CORRIENTE_PRUEBA_NOM = request.json['SESSION']['CORRIENTE_PRUEBA_NOM']
    SESN_CORRIENTE_PRUEBA_MAX = request.json['SESSION']['CORRIENTE_PRUEBA_MAX']
    SESV_METODO_FUNCIONAMIENTO_SC = request.json['SESSION']['METODO_FUNCIONAMIENTO_SC']
    SESV_METODO_ARRANQUE = request.json['SESSION']['METODO_ARRANQUE']
    SESV_METODO_EXACTITUD = request.json['SESSION']['METODO_EXACTITUD']
    SESV_METODO_VERIFICACION_CONST = request.json['SESSION']['METODO_VERIFICACION']

    #Conversion de cadena y tipo Date
    SESD_FECHA_INICIO = datetime.strptime(SESD_FECHA_INICIO_str,'%d-%m-%Y').date()
    SESD_FECHA_FIN = datetime.strptime(SESD_FECHA_FIN_str,'%d-%m-%Y').date()

    new_sesion = SEF_TSESSION(SESN_ID_TANDA,SESD_FECHA_INICIO,SESD_FECHA_FIN, SESV_CALIBRADOR, SESN_TEMPERATURA, EQUN_ID_EPM,SESV_TIPO_DE_ENERGIA, SESV_FLUJO_ENERGIA, SESN_TENSION_PRUEBA, SESN_CORRIENTE_PRUEBA_NOM, SESN_CORRIENTE_PRUEBA_MAX,SESV_METODO_FUNCIONAMIENTO_SC,SESV_METODO_ARRANQUE,SESV_METODO_EXACTITUD,SESV_METODO_VERIFICACION_CONST) 
    db.session.add(new_sesion)
    db.session.commit()


    #Insercion SEF_TDATOS_MEDIDORES
    data = request.get_json()
    cant_medidores = len(data['DATOS_MEDIDORES'])

    i=0

    while(i < cant_medidores):
        DMEV_ID_TANDA = request.json['SESSION']['ID_TANDA']
        DMEV_SERIAL = request.json['DATOS_MEDIDORES'][i]['SERIAL']
        DMEV_MARCA = request.json['DATOS_MEDIDORES'][i]['MARCA']
        DMEV_MODELO = request.json['DATOS_MEDIDORES'][i]['MODELO'] 
        DMEV_CONSTRUCCION = request.json['DATOS_MEDIDORES'][i]['CONSTRUCCION']
        DMEV_TIPO_DE_ENERGIA = request.json['DATOS_MEDIDORES'][i]['TIPO_DE_ENERGIA']
        DMEV_CLASE = request.json['DATOS_MEDIDORES'][i]['CLASE']
        DMEV_TIPO_CONEXION = request.json['DATOS_MEDIDORES'][i]['TIPO_CONEXION']
        DMEV_FABRICACION = request.json['DATOS_MEDIDORES'][i]['FABRICACION']
        DMEV_VOLTAJE_NOMINAL = request.json['DATOS_MEDIDORES'][i]['VOLTAJE_NOMINAL']
        DMEV_CORRIENTE_NOMINAL = request.json['DATOS_MEDIDORES'][i]['CORRIENTE_NOMINAL'] 
        DMEV_CORRIENTE_MAXIMA = request.json['DATOS_MEDIDORES'][i]['CORRIENTE_MAXIMA']
        DMEV_CONSTANTE = request.json['DATOS_MEDIDORES'][i]['CONSTANTE']
        DMEN_RESOLUCION_MEDIDOR = request.json['DATOS_MEDIDORES'][i]['RESOLUCION_MEDIDOR']


        
        id_tanda = db.session.query(SEF_TSESSION).filter_by(SESN_ID_TANDA=DMEV_ID_TANDA).first()
        

        if id_tanda:
            new_medidor = SEF_TDATOS_MEDIDORES(DMEV_ID_TANDA,DMEV_SERIAL, DMEV_MARCA, DMEV_MODELO, DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_CLASE,DMEV_TIPO_CONEXION,DMEV_FABRICACION,DMEV_VOLTAJE_NOMINAL,DMEV_CORRIENTE_NOMINAL,DMEV_CORRIENTE_MAXIMA,DMEV_CONSTANTE,DMEN_RESOLUCION_MEDIDOR)
            db.session.add(new_medidor)
            db.session.commit()
            
        
            id_medidor = db.session.query(SEF_TDATOS_MEDIDORES).order_by(SEF_TDATOS_MEDIDORES.DMEV_ID_SERIAL.desc()).first()

            # Inserción en SEF_TMEDICIONES
            DMEN_ID_SERIAL = id_medidor.DMEV_ID_SERIAL
            MEDV_VACIO = request.json['MEDICIONES'][i]['VACIO']
            MEDV_ARRANQUE = request.json['MEDICIONES'][i]['ARRANQUE']
            MEDN_IMIN_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['IMIN_RST_1_VALOR_MEDIO']
            MEDN_IMIN_RST_1_DESV_EST = request.json['MEDICIONES'][i]['IMIN_RST_1_DESV_EST']
            MEDN_5_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['5_RST_1_VALOR_MEDIO']
            MEDN_5_RST_1_DESV_EST = request.json['MEDICIONES'][i]['5_RST_1_DESV_EST']
            MEDN_100_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_RST_1_VALOR_MEDIO']
            MEDN_100_RST_1_DESV_EST = request.json['MEDICIONES'][i]['100_RST_1_DESV_EST']
            MEDN_100_R_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_R_1_VALOR_MEDIO']
            MEDN_100_R_1_DESV_EST = request.json['MEDICIONES'][i]['100_R_1_DESV_EST']
            MEDN_100_S_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_S_1_VALOR_MEDIO']
            MEDN_100_S_1_DESV_EST = request.json['MEDICIONES'][i]['100_S_1_DESV_EST']
            MEDN_100_T_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_T_1_VALOR_MEDIO']
            MEDN_100_T_1_DESV_EST = request.json['MEDICIONES'][i]['100_T_1_DESV_EST']
            MEDN_100_RST_0_5I_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_RST_0_5I_VALOR_MEDIO']
            MEDN_100_RST_0_5I_DESV_EST = request.json['MEDICIONES'][i]['100_RST_0_5I_DESV_EST']
            MEDN_100_RST_0_8C_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_RST_0_8C_VALOR_MEDIO']
            MEDN_100_RST_0_8C_DESV_EST = request.json['MEDICIONES'][i]['100_RST_0_8C_DESV_EST']
            MEDN_100_RST_0_5C_VALOR_MEDIO = request.json['MEDICIONES'][i]['100_RST_0_5I_VALOR_MEDIO']
            MEDN_100_RST_0_5C_DESV_EST = request.json['MEDICIONES'][i]['100_RST_0_5I_DESV_EST']
            MEDN_MAX_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i]['MAX_RST_1_VALOR_MEDIO']
            MEDN_MAX_RST_1_DESV_EST = request.json['MEDICIONES'][i]['MAX_RST_1_DESV_EST']
            MEDN_LECTURA_INICIAL_UNO = request.json['MEDICIONES'][i]['LECTURA_INICIAL_UNO']
            MEDN_LECTURA_FINAL_UNO = request.json['MEDICIONES'][i]['LECTURA_FINAL_UNO']
            MEDN_ENERGIA_APLICADA_UNO = request.json['MEDICIONES'][i]['ENERGIA_APLICADA_UNO']
            MEDN_LECTURA_INICIAL_DOS = request.json['MEDICIONES'][i]['LECTURA_INICIAL_DOS']
            MEDN_LECTURA_FINAL_DOS = request.json['MEDICIONES'][i]['LECTURA_FINAL_DOS']
            MEDN_ENERGIA_APLICADA_DOS = request.json['MEDICIONES'][i]['ENERGIA_APLICADA_DOS']
            MEDN_LECTURA_INICIAL_TRES = request.json['MEDICIONES'][i]['LECTURA_INICIAL_TRES']
            MEDN_LECTURA_FINAL_TRES =  request.json['MEDICIONES'][i]['LECTURA_FINAL_TRES']
            MEDN_ENERGIA_APLICADA_TRES = request.json['MEDICIONES'][i]['ENERGIA_APLICADA_TRES']


            if DMEN_ID_SERIAL:
                new_medicion = SEF_TMEDICIONES(DMEN_ID_SERIAL,MEDV_VACIO,MEDV_ARRANQUE,MEDN_IMIN_RST_1_VALOR_MEDIO, MEDN_IMIN_RST_1_DESV_EST, MEDN_5_RST_1_VALOR_MEDIO, MEDN_5_RST_1_DESV_EST, MEDN_100_RST_1_VALOR_MEDIO, MEDN_100_RST_1_DESV_EST, MEDN_100_R_1_VALOR_MEDIO, MEDN_100_R_1_DESV_EST, MEDN_100_S_1_VALOR_MEDIO, MEDN_100_S_1_DESV_EST, MEDN_100_T_1_VALOR_MEDIO, MEDN_100_T_1_DESV_EST, MEDN_100_RST_0_5I_VALOR_MEDIO, MEDN_100_RST_0_5I_DESV_EST, MEDN_100_RST_0_8C_VALOR_MEDIO, MEDN_100_RST_0_8C_DESV_EST, MEDN_100_RST_0_5C_VALOR_MEDIO, MEDN_100_RST_0_5C_DESV_EST, MEDN_MAX_RST_1_VALOR_MEDIO, MEDN_MAX_RST_1_DESV_EST, MEDN_LECTURA_INICIAL_UNO, MEDN_LECTURA_FINAL_UNO, MEDN_ENERGIA_APLICADA_UNO, MEDN_LECTURA_INICIAL_DOS, MEDN_LECTURA_FINAL_DOS, MEDN_ENERGIA_APLICADA_DOS, MEDN_LECTURA_INICIAL_TRES, MEDN_LECTURA_FINAL_TRES, MEDN_ENERGIA_APLICADA_TRES)
                db.session.add(new_medicion)
                db.session.commit()


        i+=1




    #Inserción en SEF_TOPCIONES_NORMA
    SESN_ID_TANDA = request.json['SESSION']['ID_TANDA']
    DMEV_CONSTRUCCION = request.json['DATOS_MEDIDORES'][0]['CONSTRUCCION']
    DMEV_TIPO_DE_ENERGIA = request.json['DATOS_MEDIDORES'][0]['TIPO_DE_ENERGIA']
    DMEV_FABRICACION = request.json['DATOS_MEDIDORES'][0]['FABRICACION']
    DMEV_TIPO_CONEXION = request.json['DATOS_MEDIDORES'][0]['TIPO_CONEXION']

    id_tanda = db.session.query(SEF_TSESSION).filter_by(SESN_ID_TANDA=SESN_ID_TANDA).first()


    if id_tanda:

        new_opnorma = SEF_TOPCIONES_NORMA(SESN_ID_TANDA,DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_FABRICACION,DMEV_TIPO_CONEXION)
        db.session.add(new_opnorma)
        db.session.commit()


    return str(id_tanda.SESN_ID_TANDA)



@app.route('/normas/verNorma',methods=['GET'])
def get_normas():

    all_filas = SEF_TNORMAS.query.all()
    result= normas_schema.dump(all_filas)

    return jsonify(result)


@app.route('/normas/buscarNorma/<id>',methods=['GET'])
def get_norma(id):
    norma = SEF_TNORMAS.query.get(id)
    return norma_schema.jsonify(norma)    


@app.route('/normas/actualizarNorma/<id>',methods=['PUT'])
def update_norma(id):

    norma = SEF_TNORMAS.query.get(id)

    NORN_ID_NORMA=request.json['id_norma']
    NORV_CODIGO_NORMA = request.json['codigo_norma']
    NORV_DETALLE = request.json['detalle']

    norma.NORN_ID_NORMA = NORN_ID_NORMA
    norma.NORV_CODIGO_NORMA = NORV_CODIGO_NORMA
    norma.NORV_DETALLE = NORV_DETALLE

    db.session.commit()

    return norma_schema.jsonify(norma)


@app.route('/normas/eliminarNorma/<id>',methods=['DELETE'])
def delete_norma(id):

    norma = SEF_TNORMAS.query.get(id)
    
    db.session.delete(norma)
    db.session.commit()

    return norma_schema.jsonify(norma)



if __name__ == "__main__":
    app.run(debug=True)