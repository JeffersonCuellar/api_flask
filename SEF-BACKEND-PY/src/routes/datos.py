from flask import Blueprint,request,jsonify, send_file
from utils.db import db
from datetime import datetime
from models.sesion import SEF_TSESSION
from models.datos_medidores import SEF_TDATOS_MEDIDORES
from models.mediciones import SEF_TMEDICIONES
from models.opciones_norma import SEF_TOPCIONES_NORMA
from modulos.incertidumbre import exacitud as cex
from datetime import datetime
from modulos.GEN_CERTIF import generar_cert as gc
from modulos.autorizar_certificado import aprobacion_certificado as check
import os


datos = Blueprint("datos",__name__)


@datos.route('/') 
def index():
    return jsonify({"message":"API Working Successfully"})



@datos.route('/certificados/insertarDatosJson',methods=['POST'])
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

    #Conversion de nomenclatura para tipo de tipo de energia 
    if SESV_TIPO_DE_ENERGIA == 'AC':
        SESV_TIPO_DE_ENERGIA = 'Activa'
    elif SESV_TIPO_DE_ENERGIA == 'RC':
        SESV_TIPO_DE_ENERGIA = 'Reactiva'
    else:
        SESV_TIPO_DE_ENERGIA = None


    # Conversion flujo de energia
    if SESV_FLUJO_ENERGIA == 'IMP':
        SESV_FLUJO_ENERGIA = 'Importada'
    elif SESV_FLUJO_ENERGIA == 'EXP':
        SESV_FLUJO_ENERGIA = 'Exportada'
    else:
        SESV_FLUJO_ENERGIA = None


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
        DMEV_CANTIDAD_FASES = request.json['DATOS_MEDIDORES'][i]['CANTIDAD_FASES']
        DMEV_CANTIDAD_HILOS = request.json['DATOS_MEDIDORES'][i]['CANTIDAD_HILOS']
        DMEV_FABRICACION = request.json['DATOS_MEDIDORES'][i]['FABRICACION']
        DMEV_VOLTAJE_NOMINAL = request.json['DATOS_MEDIDORES'][i]['VOLTAJE_NOMINAL']
        DMEV_CORRIENTE_NOMINAL = request.json['DATOS_MEDIDORES'][i]['CORRIENTE_NOMINAL'] 
        DMEV_CORRIENTE_MAXIMA = request.json['DATOS_MEDIDORES'][i]['CORRIENTE_MAXIMA']
        DMEV_CONSTANTE = request.json['DATOS_MEDIDORES'][i]['CONSTANTE']
        DMEN_RESOLUCION_MEDIDOR = request.json['DATOS_MEDIDORES'][i]['RESOLUCION_MEDIDOR']

        #Conversion de nomenclatura para tipo de tipo de energia medidores
        if DMEV_TIPO_DE_ENERGIA == 'AC':
            DMEV_TIPO_DE_ENERGIA = 'Activa'
        elif DMEV_TIPO_DE_ENERGIA == 'RC':
            DMEV_TIPO_DE_ENERGIA = 'Reactiva'
        else:
            DMEV_TIPO_DE_ENERGIA = None

        #Conversion para dmev_construccion de medidor
        if DMEV_CONSTRUCCION == 'ES':
            DMEV_CONSTRUCCION = 'Estatico'
        elif DMEV_CONSTRUCCION == 'EM':
            DMEV_CONSTRUCCION = 'Electromecanico'
        else:
            DMEV_CONSTRUCCION = None


        #Conversion para DMEV_TIPO_CONEXION de medidor
        if DMEV_TIPO_CONEXION == 'CD':
            DMEV_TIPO_CONEXION = 'Conexion Directa'
        elif DMEV_TIPO_CONEXION == 'CT':
            DMEV_TIPO_CONEXION = 'Conexion por Transformador'
        else:
            DMEV_TIPO_CONEXION = None


        #Convertir nomenclatura de fabricacion para SEF_TDATOS_MEDIDORES
        if DMEV_FABRICACION == 'ANT':
            DMEV_FABRICACION = 'Antes 2022'
        elif DMEV_FABRICACION == 'POS':
            DMEV_FABRICACION = 'Despues 2022'
        else:
            DMEV_FABRICACION = None



        #Conversión para DMEN_RESOLUCION_MEDIDOR
        DMEN_RESOLUCION_MEDIDOR = calcular_resolucion_medidor(int(DMEN_RESOLUCION_MEDIDOR[0]))


        
        id_tanda = db.session.query(SEF_TSESSION).filter_by(SESN_ID_TANDA=DMEV_ID_TANDA).first()
        

        if id_tanda:
            new_medidor = SEF_TDATOS_MEDIDORES(DMEV_ID_TANDA,DMEV_SERIAL, DMEV_MARCA, DMEV_MODELO, DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_CLASE,DMEV_TIPO_CONEXION,DMEV_CANTIDAD_FASES,DMEV_CANTIDAD_HILOS,DMEV_FABRICACION,DMEV_VOLTAJE_NOMINAL,DMEV_CORRIENTE_NOMINAL,DMEV_CORRIENTE_MAXIMA,DMEV_CONSTANTE,DMEN_RESOLUCION_MEDIDOR)
            db.session.add(new_medidor)
            db.session.commit()
            
        
            id_medidor = db.session.query(SEF_TDATOS_MEDIDORES).order_by(SEF_TDATOS_MEDIDORES.DMEV_ID_SERIAL.desc()).first()

            # Inserción en SEF_TMEDICIONES
            DMEN_ID_SERIAL = id_medidor.DMEV_ID_SERIAL
            MEDV_VACIO = request.json['MEDICIONES'][i]['VACIO']
            MEDV_ARRANQUE = request.json['MEDICIONES'][i]['ARRANQUE']
            MEDN_IMIN_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('IMIN_RST_1_VALOR_MEDIO', None)
            MEDN_IMIN_RST_1_DESV_EST = request.json['MEDICIONES'][i].get('IMIN_RST_1_DESV_EST', None)
            MEDN_5_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('5_RST_1_VALOR_MEDIO', None)
            MEDN_5_RST_1_DESV_EST = request.json['MEDICIONES'][i].get('5_RST_1_DESV_EST', None)
            MEDN_100_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_RST_1_VALOR_MEDIO', None)
            MEDN_100_RST_1_DESV_EST = request.json['MEDICIONES'][i].get('100_RST_1_DESV_EST', None)
            MEDN_100_R_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_R_1_VALOR_MEDIO', None)
            MEDN_100_R_1_DESV_EST = request.json['MEDICIONES'][i].get('100_R_1_DESV_EST', None)
            MEDN_100_S_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_S_1_VALOR_MEDIO', None)
            MEDN_100_S_1_DESV_EST = request.json['MEDICIONES'][i].get('100_S_1_DESV_EST', None)
            MEDN_100_T_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_T_1_VALOR_MEDIO', None)
            MEDN_100_T_1_DESV_EST = request.json['MEDICIONES'][i].get('100_T_1_DESV_EST', None)
            MEDN_100_RST_0_5I_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_RST_0_5I_VALOR_MEDIO', None)
            MEDN_100_RST_0_5I_DESV_EST = request.json['MEDICIONES'][i].get('100_RST_0_5I_DESV_EST', None)
            MEDN_100_RST_0_8C_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_RST_0_8C_VALOR_MEDIO', None)
            MEDN_100_RST_0_8C_DESV_EST = request.json['MEDICIONES'][i].get('100_RST_0_8C_DESV_EST', None)
            MEDN_100_RST_0_5C_VALOR_MEDIO = request.json['MEDICIONES'][i].get('100_RST_0_5C_VALOR_MEDIO', None)
            MEDN_100_RST_0_5C_DESV_EST = request.json['MEDICIONES'][i].get('100_RST_0_5C_DESV_EST', None)
            MEDN_MAX_RST_1_VALOR_MEDIO = request.json['MEDICIONES'][i].get('MAX_RST_1_VALOR_MEDIO', None)
            MEDN_MAX_RST_1_DESV_EST = request.json['MEDICIONES'][i].get('MAX_RST_1_DESV_EST', None)
            MEDN_LECTURA_INICIAL_UNO = request.json['MEDICIONES'][i].get('LECTURA_INICIAL_UNO', None)
            MEDN_LECTURA_FINAL_UNO = request.json['MEDICIONES'][i].get('LECTURA_FINAL_UNO', None)
            MEDN_ENERGIA_APLICADA_UNO = request.json['MEDICIONES'][i].get('ENERGIA_APLICADA_UNO', None)
            MEDN_LECTURA_INICIAL_DOS = request.json['MEDICIONES'][i].get('LECTURA_INICIAL_DOS', None)
            MEDN_LECTURA_FINAL_DOS = request.json['MEDICIONES'][i].get('LECTURA_FINAL_DOS', None)
            MEDN_ENERGIA_APLICADA_DOS = request.json['MEDICIONES'][i].get('ENERGIA_APLICADA_DOS', None)
            MEDN_LECTURA_INICIAL_TRES = request.json['MEDICIONES'][i].get('LECTURA_INICIAL_TRES', None)
            MEDN_LECTURA_FINAL_TRES =  request.json['MEDICIONES'][i].get('LECTURA_FINAL_TRES', None)
            MEDN_ENERGIA_APLICADA_TRES = request.json['MEDICIONES'][i].get('ENERGIA_APLICADA_TRES', None)

            
            # Conversion de nomenclatura de vacio
            if MEDV_VACIO == 'pasó':
                MEDV_VACIO = 'CEFC'
            elif MEDV_VACIO == 'falló':
                MEDV_VACIO = 'NCEFC'
            else:
                MEDV_VACIO = None

            # Conversion de nomenclatura de arranque
            if MEDV_ARRANQUE == 'pasó':
                MEDV_ARRANQUE = 'CEAR'
            elif MEDV_ARRANQUE == 'falló':
                MEDV_ARRANQUE = 'NCEAR'
            else:
                MEDV_ARRANQUE = None



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

    # convertir nomenclatura de tipo de energia en TOPCIONES_NORMA
    if DMEV_TIPO_DE_ENERGIA == 'AC':
        DMEV_TIPO_DE_ENERGIA = 'Activa'
    elif DMEV_TIPO_DE_ENERGIA == 'RC':
        DMEV_TIPO_DE_ENERGIA = 'Reactiva'
    else:
        DMEV_TIPO_DE_ENERGIA = None


    #Convertir nomenclatura de tipo_conexion para TOPCIONES_NORMA
    if DMEV_TIPO_CONEXION == 'CD':
        DMEV_TIPO_CONEXION = 'Conexion Directa'
    elif DMEV_TIPO_CONEXION == 'CT':
        DMEV_TIPO_CONEXION = 'Conexion por Transformador'
    else:
        DMEV_TIPO_CONEXION = None

    #Convertir nomenclatura de fabricacion para TOPCIONES_NORMA
    if DMEV_FABRICACION == 'ANT':
        DMEV_FABRICACION = 'Antes 2022'
    elif DMEV_FABRICACION == 'POS':
        DMEV_FABRICACION = 'Despues 2022'
    else:
        DMEV_FABRICACION = None

    #Convertir nomenclatura de construccion para TOPCIONES_NORMA
    if DMEV_CONSTRUCCION == 'ES':
        DMEV_CONSTRUCCION = 'Estatico'
    elif DMEV_CONSTRUCCION == 'EM':
        DMEV_CONSTRUCCION = 'Electromecanico'
    else:
        DMEV_CONSTRUCCION = None


    id_tanda = db.session.query(SEF_TSESSION).filter_by(SESN_ID_TANDA=SESN_ID_TANDA).first()
    

    if id_tanda:

        new_opnorma = SEF_TOPCIONES_NORMA(SESN_ID_TANDA,DMEV_CONSTRUCCION,DMEV_TIPO_DE_ENERGIA,DMEV_FABRICACION,DMEV_TIPO_CONEXION)
        db.session.add(new_opnorma)
        db.session.commit()

    tanda = id_tanda.SESN_ID_TANDA 

    
    #realizar calculos de incertidumbre y dosificación

    cex.main(tanda)


    conn1 = db.get_engine(bind='db1')
    conn2 = db.get_engine(bind='db2')
    
    list_certificados = gc.main_certificado(tanda,conn1,conn2)


    return jsonify({"message": f"Tanda {tanda} Procesada",
                    "list_certificados": list_certificados}),200





@datos.route('/certificados/firma_certificado/',methods=['PUT'])
def update_norma():





    SESN_ID_TANDA=request.json['id_tanda']
    list_CCN_NUM_CERTIFICADO=request.json['list_certificados']
    documento = request.json['documento']

    URL_NODE = f'https://cens-wdl04:8011/api/seg/getFirma/{documento}'
    
    conn1 = db.get_engine(bind='db1')


    data = check.main(SESN_ID_TANDA,list_CCN_NUM_CERTIFICADO,conn1,URL_NODE)



    return jsonify({"message": data[1],
                    "list_certificados":data[0]}),200


@datos.route('/certificados/verPDF', methods=['POST'])
def verPDF():
    

    id_certi = request.json.get('id_certi')
    fecha_certi = request.json.get('fecha_certi')


    directorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "certificados_calibracion", "certificados_pdf"))

    rutaPDF = os.path.join(directorio_base, f"{fecha_certi}_Certificado_{id_certi}.pdf")

    

    return send_file(rutaPDF, mimetype='application/pdf')

    
    



@datos.route('/certificados/verExcel', methods=['POST'])
def verExcel():

    id_certi = request.json.get('id_certi')
    fecha_certi = request.json.get('fecha_certi')

    directorio_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "certificados_calibracion", "certificados_excel"))

    rutaExcel = os.path.join(directorio_base, f"{fecha_certi}_Certificado_{id_certi}.xlsx")


    
    return send_file(rutaExcel, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    







def calcular_resolucion_medidor(value):

    try:
        if value == 1:
            return 0.1
        else:
            return round(0.1*calcular_resolucion_medidor(value-1),5)
    except Exception as e:
    
        raise ValueError('El valor que recibe por parametro no corresponde a la resolcuion medidor')


#Para usar en una nueva version

# @datos.route('/normas/verNorma',methods=['GET'])
# def get_normas():

#     all_filas = SEF_TNORMAS.query.all()
#     result= normas_schema.dump(all_filas)

#     return jsonify(result)


# @datos.route('/normas/buscarNorma/<id>',methods=['GET'])
# def get_norma(id):
#     norma = SEF_TNORMAS.query.get(id)
#     return norma_schema.jsonify(norma)    


# @datos.route('/normas/actualizarNorma/<id>',methods=['PUT'])
# def update_norma(id):

#     norma = SEF_TNORMAS.query.get(id)

#     NORN_ID_NORMA=request.json['id_norma']
#     NORV_CODIGO_NORMA = request.json['codigo_norma']
#     NORV_DETALLE = request.json['detalle']

#     norma.NORN_ID_NORMA = NORN_ID_NORMA
#     norma.NORV_CODIGO_NORMA = NORV_CODIGO_NORMA
#     norma.NORV_DETALLE = NORV_DETALLE

#     db.session.commit()

#     return norma_schema.jsonify(norma)


# @datos.route('/normas/eliminarNorma/<id>',methods=['DELETE'])
# def delete_norma(id):

#     norma = SEF_TNORMAS.query.get(id)
    
#     db.session.delete(norma)
#     db.session.commit()

#     return norma_schema.jsonify(norma)