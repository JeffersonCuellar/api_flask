import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.styles import Font
import win32com.client as cpdf
from decimal import Decimal
from datetime import datetime
from utils.db import db
from sqlalchemy import text
import pythoncom
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../..'))


def main_certificado(DMEV_ID_TANDA,conn1,conn2):

    list_certificados = []

    id_tanda = DMEV_ID_TANDA


    db_sefmec = conn1
    db_sac = conn2


    CANT_MEDIDORES = 0



        
    with db_sefmec.connect() as connection_sef:
        query = (text(f'''SELECT COUNT(*) FROM SEF_TDATOS_MEDIDORES 
                                    WHERE DMEV_ID_TANDA = :id_tanda''') )
            
        CANT_MEDIDORES   = connection_sef.execute(query,{'id_tanda': id_tanda}).fetchone()[0]


    


    with db_sefmec.connect() as connection_sef:


        query = (text(f'''SELECT DMEV_ID_SERIAL
                                    FROM SEF_TDATOS_MEDIDORES
                                    WHERE  DMEV_ID_TANDA={id_tanda} ORDER BY DMEV_ID_SERIAL ASC'''))
            
        id_serial = connection_sef.execute(query,{'id_tanda': id_tanda}).fetchone()[0]




    # Inicio
    f = 0

    j=1



    while (j<=CANT_MEDIDORES):

        # CONSULTA A LA BASE DE DATOS DE SEFMEC
        

        id_serial =  id_serial + f



        id_tanda = id_tanda

        




        # Programa principal de consultas a SEFMEC

        with db_sefmec.connect() as connection_sef:
            # Datos de medidor

            data_medidor = connection_sef.execute(text(f'''SELECT DMEV_MARCA, DMEV_MODELO, DMEV_SERIAL, DMEV_CONSTRUCCION, DMEV_TIPO_DE_ENERGIA, DMEV_CORRIENTE_NOMINAL, DMEV_CORRIENTE_MAXIMA, DMEV_TIPO_DE_ENERGIA, DMEV_CLASE, DMEV_CONSTRUCCION, DMEV_CANTIDAD_FASES, DMEV_CANTIDAD_HILOS
                                            FROM SEF_TDATOS_MEDIDORES
                                            WHERE DMEV_ID_SERIAL={id_serial} ORDER BY DMEV_ID_SERIAL ASC'''))

            MARCA, MODELO, SERIAL, CONSTRUCCION, TIPO_ENERGIA, CORRIENTE_NOMINAL, CORRIENTE_MAXIMA, TIPO_DE_ENERGIA, CLASE, CONSTRUCCION, CANT_FASES, CANT_HILOS = data_medidor.fetchall()[0]

            #Datos de la tanda

            data_tanda = connection_sef.execute(text(f'''SELECT SESD_FECHA_FIN, SESN_TEMPERATURA, SESV_CALIBRADOR, SESV_TIPO_DE_ENERGIA, SESV_FLUJO_ENERGIA, SESN_TENSION_PRUEBA, SESN_CORRIENTE_PRUEBA_NOM
                                            FROM SEF_TSESSION
                                            WHERE SESN_ID_TANDA={id_tanda}'''))

            FECHA_FIN, TEMPERATURA, CALIBRADOR, TIPO_DE_ENERGIA, FLUJO_ENERGIA, TENSION_PRUEBA, CORRIENTE_PRUEBA_NOM  = data_tanda.fetchall()[0]

            # Trazabilidad

            data_trazabilidad = connection_sef.execute(text(f'''SELECT   EP.EQUN_ID_EPM, EP.EQUV_TRAZABILIDAD                              
                                        FROM SEF_TSESSION S, SEF_TEQUIPOS_EPMS EP
                                        WHERE  S.EQUN_ID_EPM = EP.EQUN_ID_EPM
                                        AND S.SESN_ID_TANDA ={id_tanda}'''))

            ID_EPM, TRAZA_EPM  = data_trazabilidad.fetchall()[0]

            # Numerales de los métodos NTC 4856
            # Funcionamiento sin Carga

            data_numeral = connection_sef.execute(text(f'''SELECT NU.METN_NUMERAL_METODO                               
                                        FROM SEF_TSESSION S, SEF_TMETODOS_ENSAYOS NU
                                        WHERE  S.SESV_METODO_FUNCIONAMIENTO_SC = NU.METN_ID_METODO
                                        AND S.SESN_ID_TANDA={id_tanda}'''))

            NUMERAL_FUNCIONAMIENTO_CARGA   = data_numeral.fetchone()[0]

            # Arranque

            data_arranque = connection_sef.execute(text(f'''SELECT NU.METN_NUMERAL_METODO                               
                                        FROM SEF_TSESSION S, SEF_TMETODOS_ENSAYOS NU
                                        WHERE  S.SESV_METODO_ARRANQUE = NU.METN_ID_METODO
                                        AND S.SESN_ID_TANDA={id_tanda}'''))

            NUMERAL_ARRANQUE   = data_arranque.fetchone()[0]

            # Exactitud

            data_exactitud = connection_sef.execute(text(f'''SELECT   NU.METN_NUMERAL_METODO                               
                                        FROM SEF_TSESSION S, SEF_TMETODOS_ENSAYOS NU
                                        WHERE  S.SESV_METODO_EXACTITUD = NU.METN_ID_METODO
                                        AND S.SESN_ID_TANDA={id_tanda}'''))

            NUMERAL_EXACTITUD = data_exactitud.fetchone()[0]

            # Dosificacion

            data_dosificacion = connection_sef.execute(text(f'''SELECT   NU.METN_NUMERAL_METODO                               
                                        FROM SEF_TSESSION S, SEF_TMETODOS_ENSAYOS NU
                                        WHERE  S.SESV_METODO_VERIFICACION_CONST = NU.METN_ID_METODO
                                        AND S.SESN_ID_TANDA={id_tanda}'''))

            NUMERAL_DOSIFICACION = data_dosificacion.fetchone()[0]


            # Datos Metrológicos Dosificacion

            data_calculos = connection_sef.execute(text(f'''SELECT RESDN_ERROR_DOSIF, RESDN_INCERT_DOSIF, RESDV_EVAL_CONFORM
                                            FROM SEF_TRESULT_INCERT_DOSIFICACION
                                            WHERE DMEV_ID_SERIAL={id_serial} ORDER BY DMEV_ID_SERIAL ASC'''))

            ERROR_DOSIF, INCERT_DOSIF, EVAL_CONFORM   = data_calculos.fetchall()[0]

            format_incert_dosif = format_cifras_significativas(INCERT_DOSIF,2) if INCERT_DOSIF is not None else INCERT_DOSIF
            cant_decimales = contar_decimales(format_incert_dosif)
            format_error_dosif = f'{ERROR_DOSIF:.{cant_decimales}f}' if ERROR_DOSIF is not None else ERROR_DOSIF

            # Datos Mediciones dosificacion y ensayos

            data_mediciones = connection_sef.execute(text(f'''SELECT MEDV_VACIO, MEDV_ARRANQUE, MEDN_LECTURA_INICIAL_UNO, MEDN_LECTURA_FINAL_UNO, MEDN_ENERGIA_APLICADA_UNO, MEDN_LECTURA_INICIAL_DOS, MEDN_LECTURA_FINAL_DOS, MEDN_ENERGIA_APLICADA_DOS, MEDN_LECTURA_INICIAL_TRES, MEDN_LECTURA_FINAL_TRES, MEDN_ENERGIA_APLICADA_TRES
                                            FROM SEF_TMEDICIONES
                                            WHERE DMEN_ID_SERIAL={id_serial} ORDER BY DMEN_ID_SERIAL ASC'''))

            VACIO, ARRANQUE, LECTURA_INICIAL_UNO, LECTURA_FINAL_UNO, ENERGIA_APLICADA_UNO, LECTURA_INICIAL_DOS, LECTURA_FINAL_DOS, ENERGIA_APLICADA_DOS, LECTURA_INICIAL_TRES, LECTURA_FINAL_TRES, ENERGIA_APLICADA_TRES   = data_mediciones.fetchall()[0]

            # Datos Metrológicos exactitud

            data_calculos_exact= connection_sef.execute(text(f'''SELECT COUNT(*) FROM SEF_TINCERTIDUMBRE_EXACTITUD 
                                            WHERE DMEN_ID_SERIAL = {id_serial} ORDER BY DMEN_ID_SERIAL ASC''') )

            CANT_PUNTO_CARGA   = data_calculos_exact.fetchone()[0]

            i=1

            lista_promedio = []
            lista_incertidumbre = []
            lista_factor_cobertura = []
            lista_error_permitido = []
            lista_conformidad = []



            while (i<=CANT_PUNTO_CARGA):


                data = connection_sef.execute(text(f'''SELECT INCN_PROMEDIO_DATO, INCN_INCERTIDUMBRE_EXPANDIDA, INCN_FACTOR_COBERTURA, INCN_ERROR_MAX_PERMITIDO, INCV_CONFORMIDAD
                                                FROM SEF_TINCERTIDUMBRE_EXACTITUD
                                                WHERE DMEN_ID_SERIAL={id_serial} AND NORN_PUNTO_CARGA={i}  ORDER BY DMEN_ID_SERIAL ASC''') )


                PROMEDIO_DATO, INCERTIDUMBRE_EXPANDIDA, FACTOR_COBERTURA, ERROR_MAX_PERMITIDO, CONFORMIDAD = data.fetchall()[0]

                format_factor_cobert = f'{FACTOR_COBERTURA:.2f}' if FACTOR_COBERTURA is not None else FACTOR_COBERTURA
                incertidumbre_format = format_cifras_significativas(INCERTIDUMBRE_EXPANDIDA,2) if INCERTIDUMBRE_EXPANDIDA is not None else INCERTIDUMBRE_EXPANDIDA
                cant_decimales = contar_decimales(incertidumbre_format)
                error_medio_format = f'{PROMEDIO_DATO:.{cant_decimales}f}' if PROMEDIO_DATO is not None else PROMEDIO_DATO
                
                
                lista_promedio.append(error_medio_format)
                lista_incertidumbre.append(incertidumbre_format)
                lista_factor_cobertura.append(format_factor_cobert)
                lista_error_permitido.append(ERROR_MAX_PERMITIDO)
                lista_conformidad.append(CONFORMIDAD)  

                i+=1


            

            # Calibrador
            
            data_calibrador = connection_sef.execute(text(f'''SELECT   CA.CALN_CODIGO_SAC_CALIBRADOR                               
                                        FROM SEF_TSESSION S, SEF_TCALIBRADOR CA
                                        WHERE  S.SESV_CALIBRADOR = CA.CALN_ID_CALIBRADOR
                                        AND S.SESN_ID_TANDA={id_tanda}'''))

            CALIBRADOR   = data_calibrador.fetchone()[0]

            # Datos generales del Certificado

            data_general = connection_sef.execute(text(f'''SELECT   DATCV_METODOS_ENSAYOS, DATCV_INCERTIDUMBRE_MEDICION, DATCV_CONDICIONES_AMBIENTALES, DATCV_DESCARGO_RESPONSABILIDADES                              
                                        FROM SEF_TDATOS_CERTIFICADOS '''))


            METODOS_ENSAYOS, INCERTIDUMBRE_MEDICION, CONDICIONES_AMBIENTALES, DESCARGO_RESPONSABILIDADES   = data_general.fetchall()[0]

            # Insercion en tabla calibración
            # Hora y fecha actual del sistema

            fecha_hora_actual = datetime.now()
            fecha = fecha_hora_actual.date()
            hora = fecha_hora_actual.time()
            sql_insert = text(f'''INSERT INTO SEF_TCERTIFICADOS_CALIBRACION(DMEV_ID_TANDA, EQUN_ID_EPM, DMEV_ID_SERIAL, CCD_FECHA_EMISION,CCN_EST_APROBACION)
                                    VALUES ({id_tanda}, {ID_EPM}, {id_serial}, TO_DATE('{fecha}','YYYY-MM-DD'),0)''')


            connection_sef.execute(sql_insert)
            connection_sef.commit()

            # Consulta numero del certificado

            data_n_cert = connection_sef.execute(text(f'''SELECT   CCN_NUM_CERTIFICADO                               
                                        FROM SEF_TCERTIFICADOS_CALIBRACION
                                        WHERE  DMEV_ID_SERIAL = {id_serial} ORDER BY DMEV_ID_SERIAL ASC'''))

            NUM_CERTIFICADO   = data_n_cert.fetchone()[0]


        




        # CONSULTAS A BASE DE DATOS DEL SAC



        

        with db_sac.connect() as connection_sac:
            # Consulta sellos instalados

            data_sellos = connection_sac.execute(text(f'''SELECT COUNT (*) 
                                FROM SAC.SELLOS S, SAC.MEDIDORES M
                                WHERE S.MEDIDOR_ID=m.MEDIDOR_ID  
                                AND M.NUMERO_MEDIDOR='{SERIAL}'
                                AND S.ESTADO IN ('I')
                                AND S.UBICACION = 1
                                AND (S.FECHA_DESINSTALADO >= SYSDATE-60 OR S.FECHA_DESINSTALADO IS NULL)'''))

            CANT_SELLOS_INST = data_sellos.fetchone()[0]

            # funcion validacion lista
            def asignar_valores(lista):
                v1, v2, v3 = "", "", ""
            
                if len(lista) >= 1: v1 = lista[0]
                if len(lista) >= 2: v2 = lista[1]
                if len(lista) >= 3: v3 = lista[2]
            
                return v1, v2, v3
            

            k=0

            lista_inst_numero_sello = []
            lista_inst_estado_sello = []
            lista_inst_tipo_sello = []
            lista_inst_D_tipo_sello = []
            lista_inst_ubicacion_sello = []
            lista_inst_D_ubicacion_sello = []
            lista_inst_color_sello = []
            lista_inst_D_color_sello = []

            
            while (k<CANT_SELLOS_INST):


                data_sellos_i = connection_sac.execute(text(f'''SELECT NUMERO_SELLO, 
                                            S.ESTADO,
                                            TIPO,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_TIPO' AND M.CODIGO_NUM=S.TIPO) AS D_TIPO,
                                            S.UBICACION,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_UBICACION' AND M.CODIGO_NUM=S.UBICACION)AS D_UBICACION,
                                            S.COLOR,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_COLOR' AND M.CODIGO_NUM=S.COLOR)AS D_COLOR
                                            FROM SAC.SELLOS S, SAC.MEDIDORES M
                                            WHERE S.MEDIDOR_ID=M.MEDIDOR_ID
                                            AND M.NUMERO_MEDIDOR='{SERIAL}'
                                            AND S.ESTADO IN ('I')
                                            AND S.UBICACION = 1
                                            AND (S.FECHA_DESINSTALADO >= SYSDATE-60 OR S.FECHA_DESINSTALADO IS NULL)''') )
                

                NUMERO_SELLO, ESTADO_SELLO, TIPO_SELLO, D_TIPO_SELLO, UBICACION_SELLO, D_UBICACION_SELLO, COLOR_SELLO, D_COLOR_SELLO = data_sellos_i.fetchall()[k]
                        
                lista_inst_numero_sello.append(NUMERO_SELLO)
                lista_inst_estado_sello.append(ESTADO_SELLO)
                lista_inst_tipo_sello.append(TIPO_SELLO)
                lista_inst_D_tipo_sello.append(D_TIPO_SELLO)
                lista_inst_ubicacion_sello.append(UBICACION_SELLO) 
                lista_inst_D_ubicacion_sello.append(D_UBICACION_SELLO)
                lista_inst_color_sello.append(COLOR_SELLO)
                lista_inst_D_color_sello.append(D_COLOR_SELLO)

                k+=1

            n1, n2, n3 = asignar_valores(lista_inst_numero_sello)
            e1, e2, e3 = asignar_valores(lista_inst_estado_sello)
            t1, t2, t3 = asignar_valores(lista_inst_tipo_sello)
            dt1, dt2, dt3 = asignar_valores(lista_inst_D_tipo_sello)
            u1, u2, u3 = asignar_valores(lista_inst_ubicacion_sello)
            du1, du2, du3 = asignar_valores(lista_inst_D_ubicacion_sello)
            c1, c2, c3 = asignar_valores(lista_inst_color_sello)
            dc1, dc2, dc3 = asignar_valores(lista_inst_D_color_sello)

            # Consultga sellos retirados

            data_cant_sellos= connection_sac.execute(text(f'''SELECT COUNT (*) 
            FROM SAC.SELLOS S, SAC.MEDIDORES M
            WHERE S.MEDIDOR_ID=m.MEDIDOR_ID  
            AND M.NUMERO_MEDIDOR='{SERIAL}'
            AND S.ESTADO IN ('R')
            AND S.UBICACION = 1
            AND (S.FECHA_DESINSTALADO >= SYSDATE-60 OR S.FECHA_DESINSTALADO IS NULL)'''))

            CANT_SELLOS_RETIR = data_cant_sellos.fetchone()[0]

            l=0

            lista_retir_numero_sello = []
            lista_retir_estado_sello = []
            lista_retir_tipo_sello = []
            lista_retir_D_tipo_sello = []
            lista_retir_ubicacion_sello = []
            lista_retir_D_ubicacion_sello = []
            lista_retir_color_sello = []
            lista_retir_D_color_sello = []



            while (l<CANT_SELLOS_RETIR):


                data_sellos_r= connection_sac.execute(text(f'''SELECT NUMERO_SELLO, 
                                            S.ESTADO,
                                            TIPO,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_TIPO' AND M.CODIGO_NUM=S.TIPO) AS D_TIPO,
                                            S.UBICACION,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_UBICACION' AND M.CODIGO_NUM=S.UBICACION)AS D_UBICACION,
                                            S.COLOR,
                                            (SELECT M.DESCRIPCION FROM MULTITABLA M WHERE M.TABLA='SEL_COLOR' AND M.CODIGO_NUM=S.COLOR)AS D_COLOR
                                            FROM SAC.SELLOS S, SAC.MEDIDORES M
                                            WHERE S.MEDIDOR_ID=M.MEDIDOR_ID
                                            AND M.NUMERO_MEDIDOR='{SERIAL}'
                                            AND S.ESTADO IN ('R')
                                            AND S.UBICACION = 1
                                            AND (S.FECHA_DESINSTALADO >= SYSDATE-60 OR S.FECHA_DESINSTALADO IS NULL)''') )
                

                NUMERO_SELLO_RETIR, ESTADO_SELLO_RETIR, TIPO_SELLO_RETIR, D_TIPO_SELLO_RETIR, UBICACION_SELLO_RETIR, D_UBICACION_SELLO_RETIR, COLOR_SELLO_RETIR, D_COLOR_SELLO_RETIR = data_sellos_r.fetchall()[l]
                        
                lista_retir_numero_sello.append(NUMERO_SELLO_RETIR)
                lista_retir_estado_sello.append(ESTADO_SELLO_RETIR)
                lista_retir_tipo_sello.append(TIPO_SELLO_RETIR)
                lista_retir_D_tipo_sello.append(D_TIPO_SELLO_RETIR)
                lista_retir_ubicacion_sello.append(UBICACION_SELLO_RETIR) 
                lista_retir_D_ubicacion_sello.append(D_UBICACION_SELLO_RETIR)
                lista_retir_color_sello.append(COLOR_SELLO_RETIR)
                lista_retir_D_color_sello.append(D_COLOR_SELLO_RETIR)

                l+=1

            nr1, nr2, nr3 = asignar_valores(lista_retir_numero_sello)
            er1, er2, er3 = asignar_valores(lista_retir_estado_sello)
            tr1, tr2, tr3 = asignar_valores(lista_retir_tipo_sello)
            dtr1, dtr2, dtr3 = asignar_valores(lista_retir_D_tipo_sello)
            ur1, ur2, ur3 = asignar_valores(lista_retir_ubicacion_sello)
            dur1, dur2, dur3 = asignar_valores(lista_retir_D_ubicacion_sello)
            cr1, cr2, cr3 = asignar_valores(lista_retir_color_sello)
            dcr1, dcr2, dcr3 = asignar_valores(lista_retir_D_color_sello)


            # Consulta de datos de usuario y medidor

            data_usuario= connection_sac.execute(text(f'''SELECT C.CLIENTE_ID,
                            C.NOMBRE,
                            C.DIRECCION,
                            M.NUMERO_MEDIDOR,
                            M.FRECUENCIA_NOMINAL,
                            M.TENSION_NOMINAL,
                            M.CONSTANTE,
                            M.UNIDAD_CONSTANTE,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='MED_CONSTANTE' AND MU.CODIGO_NUM=M.UNIDAD_CONSTANTE)AS D_UNIDAD_CONSTANTE,
                            M.SENTIDO_MEDICION,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='MED_SENTIDO' AND MU.CODIGO_NUM=M.SENTIDO_MEDICION)AS D_SENTIDO_MEDICION,
                            M.TIPO_REGISTRADOR,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='MED_REGISTRADOR' AND MU.CODIGO_NUM=M.TIPO_REGISTRADOR)AS D_TIPO_REGISTRADOR,
                            M.ENTEROS,
                            M.DECIMALES,
                            M.NRO_FASES,
                            M.NRO_HILOS,
                            M.COMPONENTES,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='MED_COMPONENTES' AND MU.CODIGO_NUM=M.COMPONENTES)AS D_COMPONENTES,
                            M.FABRICANTE,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='ELE_FABRICANTES' AND MU.CODIGO_NUM=M.FABRICANTE)AS D_FABRICANTE,
                            M.MODELO,
                            (SELECT MU.DESCRIPCION FROM MULTITABLA MU WHERE MU.TABLA='MED_MODELO' AND MU.CODIGO_NUM=M.MODELO)AS D_MODELO,
                            (SELECT TO_CHAR(TO_DATE(MAX (MA.FECHA_ACCION),'J'), 'dd/mm/yyyy')AS FECHA_ACCION FROM SAC.MED_ACCIONES MA WHERE MA.CLIENTE_ID=M.CLIENTE_ID AND MA.MEDIDOR_ID=M.MEDIDOR_ID AND ACCION_MEDIDOR='E')AS FECHA_ACCION
                            ,(select MU.DESCRIPCION from  SAC.MED_ACCIONES ME, MULTITABLA MU where ME.medidor_id=M.MEDIDOR_ID and ME.accion_medidor='D'
                                AND MU.TABLA='OFICINAS' AND ME.oficina=MU.codigo_car and ME.FECHA_ACCION = (SELECT MAX (MA.FECHA_ACCION) FROM SAC.MED_ACCIONES MA WHERE MA.CLIENTE_ID=C.CLIENTE_ID AND MA.MEDIDOR_ID=M.MEDIDOR_ID AND ACCION_MEDIDOR='D'))AS OFICINA
                            FROM SAC.CLIENTES C,SAC.MEDIDORES M
                            WHERE C.CLIENTE_ID=M.CLIENTE_ID
                            AND M.NUMERO_MEDIDOR='{SERIAL}' '''))
                    
            CLIENTE_ID, NOMBRE_CLIENTE, DIRECCION, NUMERO_MEDIDOR, FRECUENCIA_NOMINAL, TENSION_NOMINAL, CONSTANTE, UNIDAD_CONSTANTE, D_UNIDAD_CONSTANTE, SENTIDO_MEDICION, D_SENTIDO_MEDICION, TIPO_REGISTRADOR, D_TIPO_REGISTRADOR, REGISTRO_ENTEROS, REGISTRO_DECIMALES, NUMERO_FASES, NUMERO_HILOS, COMPONENTES, D_COMPONENTES, FABRICANTE, D_FABRICANTE, MODELO, D_MODELO, FECHA_RECEPCION, OFICINA   = data_usuario.fetchall()[0]


        # cursor1.close()
        # cfs.connection.close()




        # GENERACION DE CERTIFICADOS DE CALIBRACIÓN

        workbook = openpyxl.load_workbook('src/templates/plantillas_excel/certificado_calibracion.xlsx')

        img = Image('src/images/Logos_cert.png')



        img.width = int(338)
        img.height = int(85)


        sheet = workbook.active

        # numero_certificado

        NUM_CERTIFICADO = NUM_CERTIFICADO

        # Hora y fecha actual del sistema

        fecha_recepcion = datetime.strptime(FECHA_RECEPCION,"%d/%m/%Y")
        fecha_entrada = fecha_recepcion.strftime("%Y-%m-%d")

        # numero_certificado

        CLIENTE = NOMBRE_CLIENTE
        DIRECCION = DIRECCION
        ID_TANDA = id_tanda
        FECHA_RECEPCION = fecha_entrada
        FECHA_FIN = FECHA_FIN
        fecha_emision = fecha
        OFICINA = OFICINA


        MARCA = MARCA
        MODELO = MODELO
        SERIAL = SERIAL
        NUMERO_FASES = CANT_FASES
        NUMERO_HILOS = CANT_HILOS
        FRECUENCIA = FRECUENCIA_NOMINAL
        TENSION_MEDIDOR = TENSION_NOMINAL
        CORRIENTE_NOMINAL = CORRIENTE_NOMINAL
        CORRIENTE_MAXIMA = CORRIENTE_MAXIMA
        DMEV_TIPO_DE_ENERGIA = TIPO_ENERGIA
        CLASE = CLASE
        CONSTANTE = CONSTANTE
        CONSTANTE_UNIDAD = D_UNIDAD_CONSTANTE
        CONSTRUCCION = CONSTRUCCION
        SENTIDO_MEDICION = D_SENTIDO_MEDICION
        REGISTRADOR = D_TIPO_REGISTRADOR
        REGISTRADOR_ENTEROS = REGISTRO_ENTEROS 
        REGISTRADOR_DECIMALES = REGISTRO_DECIMALES
        COMPONENTES = D_COMPONENTES
        FABRICANTE = D_FABRICANTE 
        FABRICACION = D_MODELO

        METODOS_ENSAYOS = METODOS_ENSAYOS
        TRAZABILIDAD = TRAZA_EPM
        INCERTIDUMBRE_MEDICION = INCERTIDUMBRE_MEDICION
        CONDICIONES_AMBIENTALES = CONDICIONES_AMBIENTALES
        DESCARGO_RESPONSABILIDADES = DESCARGO_RESPONSABILIDADES


        TEMPERATURA = TEMPERATURA
        HUMEDAD = 'N.A'
        SESV_TIPO_DE_ENERGIA = TIPO_DE_ENERGIA
        FLUJO_ENERGIA = FLUJO_ENERGIA
        TENSION_PRUEBA = tension_cant_fases(TENSION_PRUEBA,CANT_FASES)
        CORRIENTE_PRUEBA_NOM = CORRIENTE_PRUEBA_NOM
        ARRANQUE = ARRANQUE
        VACIO = VACIO
        RESDV_EVAL_CONFORM = EVAL_CONFORM
        RESDN_ERROR_DOSIF = format_error_dosif
        RESDN_INCERT_DOSIF = format_incert_dosif
        CALDN_LECTURA_INICIAL_UNO = LECTURA_INICIAL_UNO
        CALDN_LECTURA_FINAL_UNO = LECTURA_FINAL_UNO
        CALDN_ENERGIA_APLICADA_UNO = ENERGIA_APLICADA_UNO
        CALDN_LECTURA_INICIAL_DOS = LECTURA_INICIAL_DOS
        CALDN_LECTURA_FINAL_DOS = LECTURA_FINAL_DOS
        CALDN_ENERGIA_APLICADA_DOS = ENERGIA_APLICADA_DOS
        CALDN_LECTURA_INICIAL_TRES = LECTURA_INICIAL_TRES
        CALDN_LECTURA_FINAL_TRES = LECTURA_FINAL_TRES
        CALDN_ENERGIA_APLICADA_TRES = ENERGIA_APLICADA_TRES

        NUMERAL_FSC = NUMERAL_FUNCIONAMIENTO_CARGA
        NUMERAL_ARRANQUE = NUMERAL_ARRANQUE
        NUMERAL_EXACTITUD = NUMERAL_EXACTITUD
        NUMERAL_DOSIFICACION = NUMERAL_DOSIFICACION



    
        if(CANT_PUNTO_CARGA == 10):

            INCN_PROMEDIO_DATO_IMIN = lista_promedio[0]
            INCN_INCERTIDUMBRE_EXPANDIDA_IMIN = lista_incertidumbre[0]
            INCN_FACTOR_COBERTURA_IMIN = lista_factor_cobertura[0]
            INCN_ERROR_MAX_PERMITIDO_IMIN = lista_error_permitido[0]
            INCV_CONFORMIDAD_IMIN = lista_conformidad[0]


            INCN_PROMEDIO_DATO_5 = lista_promedio[1]
            INCN_INCERTIDUMBRE_EXPANDIDA_5 = lista_incertidumbre[1]
            INCN_FACTOR_COBERTURA_5 = lista_factor_cobertura[1]
            INCN_ERROR_MAX_PERMITIDO_5 = lista_error_permitido[1]
            INCV_CONFORMIDAD_5 = lista_conformidad[1]


            INCN_PROMEDIO_DATO_100 = lista_promedio[2]
            INCN_INCERTIDUMBRE_EXPANDIDA_100 = lista_incertidumbre[2]
            INCN_FACTOR_COBERTURA_100 = lista_factor_cobertura[2]
            INCN_ERROR_MAX_PERMITIDO_100 = lista_error_permitido[2]
            INCV_CONFORMIDAD_100 = lista_conformidad[2]


            INCN_PROMEDIO_DATO_100R = lista_promedio[3]
            INCN_INCERTIDUMBRE_EXPANDIDA_100R = lista_incertidumbre[3]
            INCN_FACTOR_COBERTURA_100R = lista_factor_cobertura[3]
            INCN_ERROR_MAX_PERMITIDO_100R = lista_error_permitido[3]
            INCV_CONFORMIDAD_100R = lista_conformidad[3]


            INCN_PROMEDIO_DATO_100S = lista_promedio[4]
            INCN_INCERTIDUMBRE_EXPANDIDA_100S = lista_incertidumbre[4]
            INCN_FACTOR_COBERTURA_100S = lista_factor_cobertura[4]
            INCN_ERROR_MAX_PERMITIDO_100S = lista_error_permitido[4]
            INCV_CONFORMIDAD_100S = lista_conformidad[4]


            INCN_PROMEDIO_DATO_100T = lista_promedio[5]
            INCN_INCERTIDUMBRE_EXPANDIDA_100T = lista_incertidumbre[5]
            INCN_FACTOR_COBERTURA_100T = lista_factor_cobertura[5]
            INCN_ERROR_MAX_PERMITIDO_100T = lista_error_permitido[5]
            INCV_CONFORMIDAD_100T = lista_conformidad[5]


            INCN_PROMEDIO_DATO_5I = lista_promedio[6]
            INCN_INCERTIDUMBRE_EXPANDIDA_5I = lista_incertidumbre[6]
            INCN_FACTOR_COBERTURA_5I = lista_factor_cobertura[6]
            INCN_ERROR_MAX_PERMITIDO_5I = lista_error_permitido[6]
            INCV_CONFORMIDAD_5I = lista_conformidad[6]


            INCN_PROMEDIO_DATO_8C = lista_promedio[7]
            INCN_INCERTIDUMBRE_EXPANDIDA_8C = lista_incertidumbre[7]
            INCN_FACTOR_COBERTURA_8C = lista_factor_cobertura[7]
            INCN_ERROR_MAX_PERMITIDO_8C = lista_error_permitido[7]
            INCV_CONFORMIDAD_8C = lista_conformidad[7]


            INCN_PROMEDIO_DATO_5C = lista_promedio[8]
            INCN_INCERTIDUMBRE_EXPANDIDA_5C = lista_incertidumbre[8]
            INCN_FACTOR_COBERTURA_5C = lista_factor_cobertura[8]
            INCN_ERROR_MAX_PERMITIDO_5C = lista_error_permitido[8]
            INCV_CONFORMIDAD_5C = lista_conformidad[8]


            INCN_PROMEDIO_DATO_IMAX = lista_promedio[9]
            INCN_INCERTIDUMBRE_EXPANDIDA_IMAX = lista_incertidumbre[9]
            INCN_FACTOR_COBERTURA_IMAX = lista_factor_cobertura[9]
            INCN_ERROR_MAX_PERMITIDO_IMAX = lista_error_permitido[9]
            INCV_CONFORMIDAD_IMAX = lista_conformidad[9]

        elif(CANT_PUNTO_CARGA == 7):
            
            INCN_PROMEDIO_DATO_IMIN = None
            INCN_INCERTIDUMBRE_EXPANDIDA_IMIN = None
            INCN_FACTOR_COBERTURA_IMIN = None
            INCN_ERROR_MAX_PERMITIDO_IMIN = None
            INCV_CONFORMIDAD_IMIN = None


            INCN_PROMEDIO_DATO_5 = lista_promedio[0]
            INCN_INCERTIDUMBRE_EXPANDIDA_5 = lista_incertidumbre[0]
            INCN_FACTOR_COBERTURA_5 = lista_factor_cobertura[0]
            INCN_ERROR_MAX_PERMITIDO_5 = lista_error_permitido[0]
            INCV_CONFORMIDAD_5 = lista_conformidad[0]


            INCN_PROMEDIO_DATO_100 = lista_promedio[1]
            INCN_INCERTIDUMBRE_EXPANDIDA_100 = lista_incertidumbre[1]
            INCN_FACTOR_COBERTURA_100 = lista_factor_cobertura[1]
            INCN_ERROR_MAX_PERMITIDO_100 = lista_error_permitido[1]
            INCV_CONFORMIDAD_100 = lista_conformidad[1]


            INCN_PROMEDIO_DATO_100R = lista_promedio[2]
            INCN_INCERTIDUMBRE_EXPANDIDA_100R = lista_incertidumbre[2]
            INCN_FACTOR_COBERTURA_100R = lista_factor_cobertura[2]
            INCN_ERROR_MAX_PERMITIDO_100R = lista_error_permitido[2]
            INCV_CONFORMIDAD_100R = lista_conformidad[2]


            INCN_PROMEDIO_DATO_100S = lista_promedio[3]
            INCN_INCERTIDUMBRE_EXPANDIDA_100S = lista_incertidumbre[3]
            INCN_FACTOR_COBERTURA_100S = lista_factor_cobertura[3]
            INCN_ERROR_MAX_PERMITIDO_100S = lista_error_permitido[3]
            INCV_CONFORMIDAD_100S = lista_conformidad[3]


            INCN_PROMEDIO_DATO_100T = lista_promedio[4]
            INCN_INCERTIDUMBRE_EXPANDIDA_100T = lista_incertidumbre[4]
            INCN_FACTOR_COBERTURA_100T = lista_factor_cobertura[4]
            INCN_ERROR_MAX_PERMITIDO_100T = lista_error_permitido[4]
            INCV_CONFORMIDAD_100T = lista_conformidad[4]


            INCN_PROMEDIO_DATO_5I = lista_promedio[5]
            INCN_INCERTIDUMBRE_EXPANDIDA_5I = lista_incertidumbre[5]
            INCN_FACTOR_COBERTURA_5I = lista_factor_cobertura[5]
            INCN_ERROR_MAX_PERMITIDO_5I = lista_error_permitido[5]
            INCV_CONFORMIDAD_5I = lista_conformidad[5]


            INCN_PROMEDIO_DATO_8C = None
            INCN_INCERTIDUMBRE_EXPANDIDA_8C = None
            INCN_FACTOR_COBERTURA_8C = None
            INCN_ERROR_MAX_PERMITIDO_8C =None
            INCV_CONFORMIDAD_8C = None


            INCN_PROMEDIO_DATO_5C = None
            INCN_INCERTIDUMBRE_EXPANDIDA_5C = None
            INCN_FACTOR_COBERTURA_5C = None
            INCN_ERROR_MAX_PERMITIDO_5C = None
            INCV_CONFORMIDAD_5C = None


            INCN_PROMEDIO_DATO_IMAX = lista_promedio[6]
            INCN_INCERTIDUMBRE_EXPANDIDA_IMAX = lista_incertidumbre[6]
            INCN_FACTOR_COBERTURA_IMAX = lista_factor_cobertura[6]
            INCN_ERROR_MAX_PERMITIDO_IMAX = lista_error_permitido[6]
            INCV_CONFORMIDAD_IMAX = lista_conformidad[6]
            

        NUMERO_SELLO_1 = n1
        NUMERO_SELLO_2 = n2
        NUMERO_SELLO_3 = n3
        ESTADO_SELLO_1 = e1
        ESTADO_SELLO_2 = e2
        ESTADO_SELLO_3 = e3
        TIPO_SELLO_1 = t1
        TIPO_SELLO_2 = t2
        TIPO_SELLO_3 = t3
        D_TIPO_SELLO_1 = dt1
        D_TIPO_SELLO_2 = dt2
        D_TIPO_SELLO_3 = dt3
        UBICACION_SELLO_1 = u1
        UBICACION_SELLO_2 = u2
        UBICACION_SELLO_3 = u3
        D_UBICACION_SELLO_1 = du1
        D_UBICACION_SELLO_2 = du2
        D_UBICACION_SELLO_3 = du3
        COLOR_SELLO_1 = c1
        COLOR_SELLO_2 = c2
        COLOR_SELLO_3 = c3
        D_COLOR_SELLO_1 = dc1
        D_COLOR_SELLO_2 = dc2
        D_COLOR_SELLO_3 = dc3

        NUMERO_SELLO_RETIR_1 = nr1
        NUMERO_SELLO_RETIR_2 = nr2
        NUMERO_SELLO_RETIR_3 = nr3
        ESTADO_SELLO_RETIR_1 = er1
        ESTADO_SELLO_RETIR_2 = er2
        ESTADO_SELLO_RETIR_3 = er3
        TIPO_SELLO_RETIR_1 = tr1
        TIPO_SELLO_RETIR_2 = tr2
        TIPO_SELLO_RETIR_3 = tr3
        D_TIPO_SELLO_RETIR_1 = dtr1
        D_TIPO_SELLO_RETIR_2 = dtr2
        D_TIPO_SELLO_RETIR_3 = dtr3
        UBICACION_SELLO_RETIR_1 = ur1
        UBICACION_SELLO_RETIR_2 = ur2
        UBICACION_SELLO_RETIR_3 = ur3
        D_UBICACION_SELLO_RETIR_1 = dur1
        D_UBICACION_SELLO_RETIR_2 = dur2
        D_UBICACION_SELLO_RETIR_3 = dur3
        COLOR_SELLO_RETIR_1 = cr1
        COLOR_SELLO_RETIR_2 = cr2
        COLOR_SELLO_RETIR_3 = cr3
        D_COLOR_SELLO_RETIR_1 = dcr1
        D_COLOR_SELLO_RETIR_2 = dcr2
        D_COLOR_SELLO_RETIR_3 = dcr3



        SESV_CALIBRADOR = CALIBRADOR


        sheet['O3'] = NUM_CERTIFICADO
        sheet['F4'] = CLIENTE
        sheet['F5'] = DIRECCION
        sheet['AG4'] = ID_TANDA
        sheet['F6'] = FECHA_RECEPCION
        sheet['O6'] = FECHA_FIN
        sheet['AA6'] = fecha_emision
        sheet['AG6'] = OFICINA


        sheet['F8'] = MARCA
        sheet['F9'] = MODELO
        sheet['F10'] = SERIAL
        sheet['F11'] = NUMERO_FASES
        sheet['H11'] = NUMERO_HILOS
        sheet['F12'] = FRECUENCIA
        sheet['M8'] = TENSION_MEDIDOR
        sheet['M9'] = CORRIENTE_NOMINAL
        sheet['O9'] = CORRIENTE_MAXIMA
        sheet['M10'] = DMEV_TIPO_DE_ENERGIA
        sheet['M11'] = CLASE
        sheet['M12'] = CONSTANTE
        sheet['O12'] = CONSTANTE_UNIDAD
        sheet['W8'] = CONSTRUCCION # Tecnologia
        sheet['W9'] = SENTIDO_MEDICION
        sheet['W10'] = REGISTRADOR
        sheet['W11'] = REGISTRADOR_ENTEROS
        sheet['W12'] = REGISTRADOR_DECIMALES
        sheet['AF8'] = COMPONENTES
        sheet['AF9'] = FABRICANTE
        sheet['AF10'] = FABRICACION

        sheet['A18'] = TRAZABILIDAD
        sheet['A15'] = METODOS_ENSAYOS
        sheet['A21'] = INCERTIDUMBRE_MEDICION
        sheet['E24'] = TEMPERATURA
        #sheet['N24'] = HUMEDAD

        sheet['K27'] = SESV_TIPO_DE_ENERGIA
        sheet['N27'] = FLUJO_ENERGIA
        sheet['K28'] = TENSION_PRUEBA
        sheet['K29'] = CORRIENTE_PRUEBA_NOM
        sheet['K31'] = ARRANQUE
        sheet['C31'] = NUMERAL_ARRANQUE
        sheet['K32'] = VACIO
        sheet['C32'] = NUMERAL_FSC
        sheet['K33'] = RESDV_EVAL_CONFORM
        sheet['C33'] = NUMERAL_DOSIFICACION
        sheet['H34'] = RESDN_ERROR_DOSIF
        sheet['N34'] = RESDN_INCERT_DOSIF
        sheet['F38'] = CALDN_LECTURA_INICIAL_UNO
        sheet['F39'] = CALDN_LECTURA_FINAL_UNO
        sheet['F40'] = CALDN_ENERGIA_APLICADA_UNO
        sheet['I38'] = CALDN_LECTURA_INICIAL_DOS
        sheet['I39'] = CALDN_LECTURA_FINAL_DOS
        sheet['I40'] = CALDN_ENERGIA_APLICADA_DOS
        sheet['M38'] = CALDN_LECTURA_INICIAL_TRES
        sheet['M39'] = CALDN_LECTURA_FINAL_TRES
        sheet['M40'] = CALDN_ENERGIA_APLICADA_TRES


        sheet['X27'] = NUMERAL_EXACTITUD
        sheet['X31'] = INCN_PROMEDIO_DATO_IMIN
        sheet['Z31'] = INCN_INCERTIDUMBRE_EXPANDIDA_IMIN
        sheet['AD31'] = INCN_FACTOR_COBERTURA_IMIN
        sheet['AF31'] = INCN_ERROR_MAX_PERMITIDO_IMIN
        sheet['AH31'] = INCV_CONFORMIDAD_IMIN


        sheet['X32'] = INCN_PROMEDIO_DATO_5
        sheet['Z32'] = INCN_INCERTIDUMBRE_EXPANDIDA_5
        sheet['AD32'] = INCN_FACTOR_COBERTURA_5
        sheet['AF32'] = INCN_ERROR_MAX_PERMITIDO_5
        sheet['AH32'] = INCV_CONFORMIDAD_5


        sheet['X33'] = INCN_PROMEDIO_DATO_100
        sheet['Z33'] = INCN_INCERTIDUMBRE_EXPANDIDA_100
        sheet['AD33'] = INCN_FACTOR_COBERTURA_100
        sheet['AF33'] = INCN_ERROR_MAX_PERMITIDO_100
        sheet['AH33'] = INCV_CONFORMIDAD_100


        sheet['X35'] = INCN_PROMEDIO_DATO_100R
        sheet['Z35'] = INCN_INCERTIDUMBRE_EXPANDIDA_100R
        sheet['AD35'] = INCN_FACTOR_COBERTURA_100R
        sheet['AF35'] = INCN_ERROR_MAX_PERMITIDO_100R
        sheet['AH35'] = INCV_CONFORMIDAD_100R


        sheet['X38'] = INCN_PROMEDIO_DATO_100S
        sheet['Z38'] = INCN_INCERTIDUMBRE_EXPANDIDA_100S
        sheet['AD38'] = INCN_FACTOR_COBERTURA_100S
        sheet['AF38'] = INCN_ERROR_MAX_PERMITIDO_100S
        sheet['AH38'] = INCV_CONFORMIDAD_100S


        sheet['X40'] = INCN_PROMEDIO_DATO_100T
        sheet['Z40'] = INCN_INCERTIDUMBRE_EXPANDIDA_100T
        sheet['AD40'] = INCN_FACTOR_COBERTURA_100T
        sheet['AF40'] = INCN_ERROR_MAX_PERMITIDO_100T
        sheet['AH40'] = INCV_CONFORMIDAD_100T


        sheet['X41'] = INCN_PROMEDIO_DATO_5I
        sheet['Z41'] = INCN_INCERTIDUMBRE_EXPANDIDA_5I
        sheet['AD41'] = INCN_FACTOR_COBERTURA_5I
        sheet['AF41'] = INCN_ERROR_MAX_PERMITIDO_5I
        sheet['AH41'] = INCV_CONFORMIDAD_5I


        sheet['X43'] = INCN_PROMEDIO_DATO_8C
        sheet['Z43'] = INCN_INCERTIDUMBRE_EXPANDIDA_8C
        sheet['AD43'] = INCN_FACTOR_COBERTURA_8C
        sheet['AF43'] = INCN_ERROR_MAX_PERMITIDO_8C
        sheet['AH43'] = INCV_CONFORMIDAD_8C


        sheet['X45'] = INCN_PROMEDIO_DATO_5C
        sheet['Z45'] = INCN_INCERTIDUMBRE_EXPANDIDA_5C
        sheet['AD45'] = INCN_FACTOR_COBERTURA_5C
        sheet['AF45'] = INCN_ERROR_MAX_PERMITIDO_5C
        sheet['AH45'] = INCV_CONFORMIDAD_5C


        sheet['X47'] = INCN_PROMEDIO_DATO_IMAX
        sheet['Z47'] = INCN_INCERTIDUMBRE_EXPANDIDA_IMAX
        sheet['AD47'] = INCN_FACTOR_COBERTURA_IMAX
        sheet['AF47'] = INCN_ERROR_MAX_PERMITIDO_IMAX
        sheet['AH47'] = INCV_CONFORMIDAD_IMAX

        sheet['F44'] = NUMERO_SELLO_1
        sheet['I44'] = D_TIPO_SELLO_1
        sheet['L44'] = D_COLOR_SELLO_1
        sheet['N44'] = 'N.A'
        sheet['F45'] = NUMERO_SELLO_2
        sheet['I45'] = D_TIPO_SELLO_2
        sheet['L45'] = D_COLOR_SELLO_2
        sheet['N45'] = 'N.A'
        sheet['F46'] = NUMERO_SELLO_3
        sheet['I46'] = D_TIPO_SELLO_3
        sheet['L46'] = D_COLOR_SELLO_3
        sheet['N46'] = 'N.A'

        sheet['F48'] = NUMERO_SELLO_RETIR_1
        sheet['I48'] = D_TIPO_SELLO_RETIR_1
        sheet['L48'] = D_COLOR_SELLO_RETIR_1
        sheet['N48'] = ESTADO_SELLO_RETIR_1

        sheet['F50'] = NUMERO_SELLO_RETIR_2
        sheet['I50'] = D_TIPO_SELLO_RETIR_2
        sheet['L50'] = D_COLOR_SELLO_RETIR_2
        sheet['N50'] = ESTADO_SELLO_RETIR_2
        
        sheet['F51'] = NUMERO_SELLO_RETIR_3
        sheet['I51'] = D_TIPO_SELLO_RETIR_3
        sheet['L51'] = D_COLOR_SELLO_RETIR_3
        sheet['N51'] = ESTADO_SELLO_RETIR_3


        sheet['A56'] = DESCARGO_RESPONSABILIDADES

        sheet['F66'] = SESV_CALIBRADOR


        sheet.add_image(img, 'B2')

        sheet['Q1'].font = Font(bold=True,size=8.5)


        pythoncom.CoInitialize()

        ruta_excel = os.path.join(base_dir,'src','certificados_calibracion','certificados_excel',f'{fecha}_certificado_{NUM_CERTIFICADO}.xlsx')

        ruta_pdf = os.path.join(base_dir,'src','certificados_calibracion','certificados_pdf',f'{fecha}_certificado_{NUM_CERTIFICADO}.pdf')

        os.makedirs(os.path.dirname(ruta_excel),exist_ok=True)
        os.makedirs(os.path.dirname(ruta_pdf),exist_ok=True)

        workbook.save(ruta_excel)

        excel = cpdf.Dispatch("Excel.Application")
        excel.Visible = False

        libro = excel.Workbooks.Open(ruta_excel)

        libro.ExportAsFixedFormat(0, ruta_pdf)


        libro.Close()
        excel.Quit()

        del libro
        del excel


        archivo_excel = ruta_excel
        archivo_pdf = ruta_pdf


        pythoncom.CoUninitialize()

        list_certificados.append(NUM_CERTIFICADO)
        
        id_serial = id_serial - f
        

        j+=1

        f+=1

    return list_certificados


#Manejo de cifras significativas
def format_cifras_significativas(num,cant_cifras):
    return f'{Decimal(num):.{cant_cifras}g}'

def contar_decimales(numero):
    numero_str = str(numero)

    if '.' in numero_str:
        decimales = len(numero_str.split('.')[1])

    else:
        decimales = 0

    return decimales


#Tension de prueba con cant de fases
def tension_cant_fases(tension_prueba, cant_fases):
    if cant_fases == '1F':
        tension_prueba = str(tension_prueba)
    elif cant_fases == '2F':
        tension_prueba = f'2X{tension_prueba}/208'
    elif cant_fases == '3F':
        tension_prueba = f'3X{tension_prueba}/208'
    else:
        tension_prueba = ''

    return tension_prueba 





if __name__=='__main__':
    main_certificado()