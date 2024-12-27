import math
from sqlalchemy import text
from utils.db import db
from scipy.stats import t
from modulos.incertidumbre import dosificacion as df




#Método principal
def main(tanda):
    
    





    #Consultar la cantidad de medidores por tanda
    medidores = db.session.execute(text(f'''SELECT COUNT(*) FROM SEF_TDATOS_MEDIDORES WHERE DMEV_ID_TANDA = {tanda}'''))
    num_medidores = medidores.fetchone()[0]
    print(f'num_medidores: {num_medidores}')

    #Consulta del id_serial
    serial = db.session.execute(text(f'''SELECT MIN(DMEV_ID_SERIAL)
                            FROM SEF_TSESSION SE
                            RIGHT JOIN SEF_TDATOS_MEDIDORES DM
                            ON SE.SESN_ID_TANDA = DM.DMEV_ID_TANDA
                            WHERE SESN_ID_TANDA = {tanda}'''))
    id_serial = serial.fetchone()[0]
    

    #Variable control ciclo cantidad de medidores
    vuelta=1

    while(vuelta <= num_medidores):

            

            #Consulta para hallar el id_norma
            datos= db.session.execute(text(f'''SELECT OPCNN_ID_NORMA,EQUN_ID_EPM,OPCNN_CANT_PUNTOS_CARGA
                            FROM SEF_TSESSION SE
                            RIGHT JOIN SEF_TOPCIONES_NORMA O 
                            ON SE.SESN_ID_TANDA = O.SESN_ID_TANDA
                            WHERE SE.SESN_ID_TANDA = {tanda}
                            '''))
            id_norma, epm,puntos_carga = datos.fetchall()[0]




            # epm = int(input('Digite epm: ')) #Este valor se trae del frontend(opcion del cliente)

            # #Consulta a la tabla SEF_TEQUIPOS_EPMS
            data_equipos = db.session.execute(text(f'''SELECT EQUN_INCERT_FP_1,EQUN_INCERT_FP_05I,EQUN_INCERT_FP_05C, EQUN_INCERT_FP_08C 
                                FROM SEF_TEQUIPOS_EPMS 
                                WHERE EQUN_ID_EPM={epm}'''))
            
            incertidumbre_B1,incertidumbre_B05I,incertidumbre_B05C, incertidumbre_B08C = data_equipos.fetchall()[0] #TRAER TODOS LOS TIPOS DE INCERTIDUMBRES
            incertidumbre_B = incertidumbre_B1/2 #fija


            # # #CONSULTA PARA TRAER LA CLASE Y DATOS DE MEDICION
            data_medicion = db.session.execute(text(f''' SELECT 
                                m.dmev_clase,ms.medn_imin_rst_1_valor_medio,ms.medn_imin_rst_1_desv_est,
                                ms.medn_5_rst_1_valor_medio,ms.medn_5_rst_1_desv_est,
                                ms.medn_100_rst_1_valor_medio,ms.medn_100_rst_1_desv_est,
                                ms.medn_100_r_1_valor_medio,ms.medn_100_r_1_desv_est,
                                ms.medn_100_s_1_valor_medio,ms.medn_100_s_1_desv_est,
                                ms.medn_100_t_1_valor_medio,ms.medn_100_t_1_desv_est,
                                ms.MEDN_100_RST_0_5I_VALOR_MEDIO,ms.medn_100_rst_0_5i_desv_est,
                                ms.medn_100_rst_0_8c_valor_medio,ms.medn_100_rst_0_8c_desv_est,
                                ms.medn_100_rst_0_5c_valor_medio,ms.medn_100_rst_0_5c_desv_est,
                                ms.medn_max_rst_1_valor_medio,ms.medn_max_rst_1_desv_est
                                FROM sef_tsession S 
                                    RIGHT JOIN SEF_TDATOS_MEDIDORES M
                                    ON S.SESN_ID = M.DMEV_ID_TANDA 
                                    RIGHT JOIN SEF_TMEDICIONES MS
                                    ON M.DMEV_ID_SERIAL = MS.DMEN_ID_SERIAL
                                WHERE  M.DMEV_ID_TANDA = {tanda} AND m.dmev_id_serial = {id_serial}'''))
            
            #El id_serial será incremental de acuerdo al numero de medidores por tanda

            
            CLASE,VALOR_MEDIO_MIN,DESVIACION_ESTANDAR_MIN,VALOR_MEDIO_5,DESVIACION_ESTANDAR_5,VALOR_MEDIO_100_RST,DESVIACION_ESTANDAR_100_RST,VALOR_MEDIO_1OO_R,DESVIACION_ESTANDAR_100_R,VALOR_MEDIO_100_S,DESVIACION_ESTANDAR_100_S,VALOR_MEDIO_100_T,DESVIACION_ESTANDAR_100_T,VALOR_MEDIO_05I,DESVIACION_ESTANDAR_05I,VALOR_MEDIO_08C,DESVIACION_ESTANDAR_08C,VALOR_MEDIO_05C,DESVIACION_ESTANDAR_05C,VALOR_MEDIO_MAX,DESVIACION_ESTANDAR_MAX = data_medicion.fetchall()[0] #TRAER TODAS LAS DESVIACIONES
            
            CLASE_VALOR = CLASE.replace('.','')


            
            # Loop que calcula la incertidumbre por cada punto de carga

        

            i=1 
            while(i <= puntos_carga ):

                print(f'punto de carga: {i}')
                if(puntos_carga == 10):

                    match(i):
                        case 1:
                            VALOR_MEDIO = VALOR_MEDIO_MIN
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_MIN
                        case 2:
                            VALOR_MEDIO = VALOR_MEDIO_5
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_5
                        case 3:
                            VALOR_MEDIO = VALOR_MEDIO_100_RST
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_RST
                        case 4:
                            VALOR_MEDIO = VALOR_MEDIO_1OO_R
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_R
                        case 5:
                            VALOR_MEDIO = VALOR_MEDIO_100_S
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_S
                        case 6:
                            VALOR_MEDIO = VALOR_MEDIO_100_T
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_T
                        case 7:
                            VALOR_MEDIO = VALOR_MEDIO_05I
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_05I
                        case 8:
                            VALOR_MEDIO = VALOR_MEDIO_08C
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_08C
                        case 9:
                            VALOR_MEDIO = VALOR_MEDIO_05C
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_05C
                        case 10:
                            VALOR_MEDIO = VALOR_MEDIO_MAX
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_MAX

                elif(puntos_carga == 7):
                    match(i):
                        case 1:
                            VALOR_MEDIO = VALOR_MEDIO_5
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_5
                        case 2:
                            VALOR_MEDIO = VALOR_MEDIO_100_RST
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_RST
                        case 3:
                            VALOR_MEDIO = VALOR_MEDIO_1OO_R
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_R
                        case 4:
                            VALOR_MEDIO = VALOR_MEDIO_100_S
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_S
                        case 5:
                            VALOR_MEDIO = VALOR_MEDIO_100_T
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_100_T
                        case 6:
                            VALOR_MEDIO = VALOR_MEDIO_05I
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_05I
                        case 7:
                            VALOR_MEDIO = VALOR_MEDIO_MAX
                            DESVIACION_ESTANDAR = DESVIACION_ESTANDAR_MAX

                
                # #condicion de cambio por el factor de potencia
                if(id_norma == 1 or id_norma == 2):
                    incertidumbre_B = incertidumbre_B05I/2 if i == 6 else incertidumbre_B1/2

                elif(id_norma >= 3 and id_norma <= 10):
                    match(i):
                        case 7:
                            incertidumbre_B = incertidumbre_B05I/2
                        case 8:
                            incertidumbre_B = incertidumbre_B08C/2
                        case 9:
                            incertidumbre_B = incertidumbre_B05C/2
                        case _:
                            incertidumbre_B = incertidumbre_B1/2
                

            #     #calculo de incertidumbre 
                incertidumbre_a = calcular_Ua(DESVIACION_ESTANDAR)
                    
                incertidumbre_c = calcular_Uc(incertidumbre_a,incertidumbre_B)


                valorEfectivo = calcular_Vef(incertidumbre_a,incertidumbre_c,incertidumbre_B)


                factorCobertura = calcular_K(valorEfectivo)

                print(f'VALOR_MEDIO: {VALOR_MEDIO}')
                print(f'DESVIACION_ESTANDAR: {DESVIACION_ESTANDAR}')
                print(f'incertidumbre_a: {incertidumbre_a}')
                print(f'incertidumbre_B: {incertidumbre_B}')
                print(f'incertidumbre_c: {incertidumbre_c}')
                print(f'valorEfectivo: {valorEfectivo}')
                print(f'factorCobertura : {factorCobertura}')

                print('fin de punto de carga------>')
                error_porcentual = calcular_limite_ep(CLASE_VALOR,id_norma,i)

                incertidumbre_exp = calcular_incertidumbre_Exp(incertidumbre_c,factorCobertura)

                lep_obtenido = calcular_lep_obtenido(error_porcentual,incertidumbre_c)

                resultadoC = conformidad(VALOR_MEDIO,lep_obtenido)

                #CALCULAR FACTOR_POTENCIA

                data_fp = db.session.execute(text(f'SELECT NORDV_TIPO_CARGA, NORDV_FACTOR_POTENCIA FROM SEF_TNORMAS_DETALLE WHERE NORN_ID_NORMA = {id_norma} AND NORDN_PUNTO_CARGA = {i}'))

                tipo_carga,factor_potencia = data_fp.fetchall()[0]



                try: 
                    #inserción de datos en la tabla SEF_TINCERTIDUMBRE
                    sql_insert = text(f'''INSERT 
                                INTO SEF_TINCERTIDUMBRE_EXACTITUD(
                                DMEN_ID_SERIAL,NORN_ID_NORMA,NORN_PUNTO_CARGA,
                                NORN_TIPO_CARGA,NORN_FACTOR_POTENCIA,
                                INCN_PROMEDIO_DATO,INCN_DESVIACION_ESTANDAR, 
                                INCN_INCERTIDUMBRE_TIPO_A, INCN_INCERTIDUMBRE_TIPO_B, 
                                INCN_INCERTIDUMBRE_COMBINADA, INCN_GRADOS_LIBERTAD, 
                                INCN_FACTOR_COBERTURA, INCN_INCERTIDUMBRE_EXPANDIDA, 
                                INCN_ERROR_MAX_PERMITIDO, INCN_CALCULO_REGLA_DECISION, 
                                INCV_CONFORMIDAD)
                                    VALUES ({id_serial},{id_norma},{i},'{tipo_carga}','{factor_potencia}',{VALOR_MEDIO},{DESVIACION_ESTANDAR}, {incertidumbre_a}, {incertidumbre_B}, {incertidumbre_c}, {valorEfectivo}, {factorCobertura}, {incertidumbre_exp}, {error_porcentual}, {lep_obtenido},'{resultadoC}') ''')
                    

                    db.session.execute(sql_insert)
                    db.session.commit()

                except Exception as e:

                    sql_insert = text(f'''INSERT 
                                INTO SEF_TINCERTIDUMBRE_EXACTITUD(
                                DMEN_ID_SERIAL,NORN_ID_NORMA,NORN_PUNTO_CARGA,
                                NORN_TIPO_CARGA,NORN_FACTOR_POTENCIA,
                                INCN_PROMEDIO_DATO,INCN_DESVIACION_ESTANDAR, 
                                INCN_INCERTIDUMBRE_TIPO_A, INCN_INCERTIDUMBRE_TIPO_B, 
                                INCN_INCERTIDUMBRE_COMBINADA, INCN_GRADOS_LIBERTAD, 
                                INCN_FACTOR_COBERTURA, INCN_INCERTIDUMBRE_EXPANDIDA, 
                                INCN_ERROR_MAX_PERMITIDO, INCN_CALCULO_REGLA_DECISION, 
                                INCV_CONFORMIDAD)
                                    VALUES ({id_serial},{id_norma},{i},'{tipo_carga}','{factor_potencia}',NULL,NULL, NULL, NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL) ''')

                    

                    db.session.execute(sql_insert)
                    db.session.commit()





                # Variable de control
                i+=1


            #Aqui se llama el calculo de dosificación


            df.main(epm,puntos_carga,id_serial) 
            
            
            

            id_serial+=1

            vuelta+=1
            



# CALCULO DE INCERTIDUMBRE DE EXACTITUD  ------->
# cada calculo es aplicado a cada punto de carga
def calcular_Ua(desv_est):
    if (desv_est is not None):
        desviacion_est = float(desv_est)
        raiz = math.sqrt(3)
        resultado = desviacion_est/raiz
    else:
        resultado = None
    
    return resultado


# Uc: Incertidumbre combinada:


def calcular_Uc(Ua,Ub):

    if (Ua is not None):
        Ub = float(Ub)
        resultado = math.sqrt(Ua**2 + Ub**2)
    else:
        resultado = None
    
    return resultado


# Vef: El valor efectivo es suministrado pr la formula t-student:


def calcular_Vef(Ua, Uc, Ub):
    print(f'Ua: {type(Ua)}')
    print(f'Ub: {type(Ub)}')
    print(f'Uc: {type(Uc)}')
    try:
        Ub = float(Ub)
        resultado = (Uc**4) / ((Ua**4 / 2) + (Ub**4 / 200))
    except Exception as e:
        resultado = 999999
    return resultado




# k: constante suminstrada por la formula t-student:(factor de cobertura)
#Inversa de la desviación estandar t-student de dos colas


def calcular_K(v_ef):

    try:
        resultado = t.ppf(1-0.0455/2,v_ef)
    except Exception as  e:
        resultado = 2.00

    return resultado


# Uep: Incertidumbre expandida:
def calcular_incertidumbre_Exp(u_c,k):


    if(k is not None and u_c is not None):

        resultado = u_c*k
    else:
        resultado = None

    return resultado


# Lep:El limite de error porcentual: Formula dada por normativa
def calcular_limite_ep(CLASE_VALOR,id_norma,i):

    

    data = db.session.execute(text(f'SELECT NORDN_CLASE_{CLASE_VALOR} FROM SEF_TNORMAS_DETALLE WHERE NORN_ID_NORMA = {id_norma} AND NORDN_PUNTO_CARGA = {i}'))
    lep = data.fetchone()[0]



    if(lep is not None):
        resultado = lep
    else:
        resultado = None


    return resultado


    

# Lep - 1,64|Uc|: primera condición para la evalucación del resultado:
def calcular_lep_obtenido(error_porcentual, Uc):
    

    if(error_porcentual is not None and Uc):
        error_porcentual = float(error_porcentual)
        resultado = abs(error_porcentual) - 1.64 * abs(Uc)
    else:
        resultado = None

    return resultado


# conformidad: resultado de evaluación, conforme - no conforme -->
def conformidad(error_medio, limiteEP_obtenido):
    if error_medio is None or limiteEP_obtenido is None:
        return 'NCEEX'
    return 'CEEX' if abs(error_medio) <= limiteEP_obtenido else 'NCEEX'




#llamado método principal
if __name__ == "__main__":
    main()
