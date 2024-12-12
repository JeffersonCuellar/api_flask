from sqlalchemy import text
from statistics import mean as mn
from statistics import stdev 
import math
from scipy.stats import t
from utils.db import db


#Calculo de la dosificación

def main(epm,puntos_carga,id_serial):




    data_prueba = db.session.execute(text(f'''SELECT 
                            md.medn_lectura_inicial_uno,md.medn_lectura_inicial_dos,md.medn_lectura_inicial_tres,
                            md.medn_lectura_final_uno,md.medn_lectura_final_dos,md.medn_lectura_final_tres,
                            md.medn_energia_aplicada_uno,md.medn_energia_aplicada_dos,md.medn_energia_aplicada_tres,
                            md.medn_max_rst_1_valor_medio,ie.incn_incertidumbre_combinada,
                            ie.incn_error_max_permitido,m.dmen_resolucion_medidor,s.sesn_corriente_prueba_max,m.dmev_id_serial
                        FROM sef_tsession S 
                            RIGHT JOIN SEF_TDATOS_MEDIDORES M
                            ON S.SESN_ID_TANDA = M.DMEV_ID_TANDA
                            RIGHT JOIN SEF_TMEDICIONES MD
                            ON M.DMEV_ID_SERIAL = MD.DMEN_ID_SERIAL
                            RIGHT JOIN SEF_TINCERTIDUMBRE_EXACTITUD IE
                            ON M.DMEV_ID_SERIAL = IE.DMEN_ID_SERIAL
                        WHERE  IE.NORN_PUNTO_CARGA = {puntos_carga} AND md.dmen_id_serial={id_serial}'''))
    lectura_inicial1,lectura_inicial2,lectura_inicial3,lectura_final1,lectura_final2,lectura_final3,energia_aplicada1,energia_aplicada2,energia_aplicada3,error_medio_Imax,incertidumbre_combinada_max,lep_permisible,resolucion_medidor,corriente_max,id_serial=data_prueba.fetchall()[0]



    # Ep Error en prueba de exactitud, valor dado por laboratorio Imax
    # Incertidumbre tipo B clase 1

    lista_lectura_inicial = crearLista(lectura_inicial1,lectura_inicial2,lectura_inicial3)

    lista_lectura_final = crearLista(lectura_final1,lectura_final2,lectura_final3)

    lista_ea = crearLista(energia_aplicada1, energia_aplicada2, energia_aplicada3)


    #consulta tabla sef_tequipos_epms para obtener error, incertudumbre y deriva del epm
    
    data_equipo = db.session.execute(text(f'''SELECT EQUN_DERIVA_FP_1, EQUN_RESOLUCION_EPM,
                        EQUN_ERROR_EPM_2_AMP,EQUN_INCERT_EPM_2_AMP,
                        EQUN_ERROR_EPM_6_AMP,EQUN_INCERT_EPM_6_AMP,
                        EQUN_ERROR_EPM_10_AMP,EQUN_INCERT_EPM_10_AMP,
                        EQUN_ERROR_EPM_20_AMP,EQUN_INCERT_EPM_20_AMP,
                        EQUN_ERROR_EPM_30_AMP,EQUN_INCERT_EPM_30_AMP,
                        EQUN_ERROR_EPM_40_AMP,EQUN_INCERT_EPM_40_AMP,
                        EQUN_ERROR_EPM_45_AMP,EQUN_INCERT_EPM_45_AMP,
                        EQUN_ERROR_EPM_50_AMP,EQUN_INCERT_EPM_50_AMP,
                        EQUN_ERROR_EPM_60_AMP,EQUN_INCERT_EPM_60_AMP,
                        EQUN_ERROR_EPM_80_AMP,EQUN_INCERT_EPM_80_AMP,
                        EQUN_ERROR_EPM_100_AMP,EQUN_INCERT_EPM_100_AMP,
                        EQUN_ERROR_EPM_120_AMP,EQUN_INCERT_EPM_120_AMP
                        FROM SEF_TEQUIPOS_EPMS 
                        WHERE EQUN_ID_EPM = {epm}'''))
    
    deriva,resolucionEPM,error_2,incert_2,error_6,incert_6,error_10,incert_10,error_20,incert_20,error_30,incert_30,error_40,incert_40,error_45,incert_45,error_50,incert_50,error_60,incert_60,error_80,incert_80,error_100,incert_100,error_120,incert_120  = data_equipo.fetchall()[0]
    

    match(corriente_max):
            case 2:
                error_incertidumbre_EPM = error_2
                incertidumbre_EPM = incert_2
            case 6:
                error_incertidumbre_EPM = error_6
                incertidumbre_EPM = incert_6
            case 10:
                error_incertidumbre_EPM = error_10
                incertidumbre_EPM = incert_10
            case 20:
                error_incertidumbre_EPM = error_20
                incertidumbre_EPM = incert_20
            case 30:
                error_incertidumbre_EPM = error_30
                incertidumbre_EPM = incert_30
            case 40:
                error_incertidumbre_EPM = error_40
                incertidumbre_EPM = incert_40
            case 45:
                error_incertidumbre_EPM = error_45
                incertidumbre_EPM = incert_45
            case 50:
                error_incertidumbre_EPM = error_50
                incertidumbre_EPM = incert_50
            case 60:
                error_incertidumbre_EPM = error_60
                incertidumbre_EPM = incert_60
            case 80:
                error_incertidumbre_EPM = error_80
                incertidumbre_EPM = incert_80
            case 100:
                error_incertidumbre_EPM = error_100
                incertidumbre_EPM = incert_100
            case 120:
                error_incertidumbre_EPM = error_120
                incertidumbre_EPM = incert_120
            case __:
                error_incertidumbre_EPM = 0.00056
                incertidumbre_EPM = 0.00056

    lista_em = []
    lista_evc = []
    mediciones_em = []
    mediciones_ea = []
    mediciones_evc = []
    lista_reduccion = []
    datos_uxi = []
    datos_uyi = []
    distribucion = ['normal','rectangular', 'normal', 'rectanguar','rectangular','t-student','rectangular','t-student'] #se obtiene de la Normativa
    lista_grados_libertad = []

    #mediciones realizadas
    i = 0
    

    while(i < 3 ):


        em = calcular_Em(lista_lectura_final[i],lista_lectura_inicial[i])

        evc = calcular_Evc(em,lista_ea[i],error_medio_Imax)

        lista_em.append(em)
        lista_evc.append(evc)






        #variable de control
        i+=1
    
    


    
    

    listas = [lista_em, lista_ea, lista_evc]
    mediciones = [mediciones_em, mediciones_ea, mediciones_evc]

    # Cálculo de medias y desviaciones estándar
    for i, lista in enumerate(listas):
        media = calcular_promedio_e_medidas(lista)
        desviacion_estandar = calcular_desv_est_medidas(lista)
        desviacion_estandar_smed = calcular_desv_est_smed(desviacion_estandar)
        
        mediciones[i].append(media)
        mediciones[i].append(desviacion_estandar)
        mediciones[i].append(desviacion_estandar_smed)




    coeficiente_sensibilidad_Em = calcular_coeficiente_sensibilidad_Em(mediciones_ea[0])

    coeficiente_sensibilidad_Ea = calcular_coeficiente_sensibilidad_Ea(mediciones_em[0],mediciones_ea[0])

    coeficiente_sensibilidad_Ep = -1

    listaCoeficiente_sen = [coeficiente_sensibilidad_Em, coeficiente_sensibilidad_Ea, -1]
    




    em_repetibilidad_lecturas = mediciones_em[2]
    em_resolucion_medidor = resolucion_medidor/2
    ea_repetibilidad = mediciones_ea[2]
    ea_resolucion_EMP = resolucionEPM/2

    ea_error_medio = calcular_error_EPM(error_incertidumbre_EPM,mediciones_ea[0])
    ea_incertidumbre_EPM = calcular_incert_EPM(incertidumbre_EPM,mediciones_ea[0])
    ea_deriva = calcular_deriva_ud(deriva,mediciones_ea[0])
    ea_incertidumbre_combinada = incertidumbre_combinada_max
    tupla_duda = em_repetibilidad_lecturas, em_resolucion_medidor, ea_repetibilidad, ea_resolucion_EMP, ea_error_medio, ea_incertidumbre_EPM,ea_deriva, ea_incertidumbre_combinada

    lista_duda = list(tupla_duda)



    #calcular valores de incertidumbre por dosificacion

    i = 0

    while(i < 8):

        
        #calculando reducción

        lista_reduccion.append(calcular_reduccion(distribucion[i]))



        #calculo de variable Uxi
        uxi = calcular_uxi(lista_duda[i],lista_reduccion[i])
        datos_uxi.append(uxi)

        

        #calculo de variable Uyi
        if (i>=0 and i<=1):
            coeficiente_sensibilidad = coeficiente_sensibilidad_Em
        elif (i>=2 and i <= 6):
            coeficiente_sensibilidad = coeficiente_sensibilidad_Ea
        else:
            coeficiente_sensibilidad = -1


        uyi = calcular_uyi(uxi,coeficiente_sensibilidad)
        datos_uyi.append(uyi)



        #Calculo de grados de libertad en xi
        veff_xi = calcular_grado_efectivo(distribucion[i],lista_evc)
        lista_grados_libertad.append(veff_xi)


        i+=1


    
    #Calculo de la incertidumbre estandar combinada

    incertidumbre_estandarCombinada_evc = calcular_incertidumbre_estandar_evc(datos_uyi)





    #Calcular Veff, Incertidumbre estandar combinada e incertidumbre expandida

    cadena_uyi = 'Uy'
    cadena_veff_xi = 'grado_efectivo_libertadx'

    diccionarioUyi = crearDiccionario(datos_uyi,cadena_uyi)
    dicc_grado_libertad = crearDiccionario(lista_grados_libertad,cadena_veff_xi)

    veff = calcular_veff(diccionarioUyi,dicc_grado_libertad,incertidumbre_estandarCombinada_evc)


    #calcular factor de cubrimiento K
    factor_cubrimiento = calcular_factor_cubrimiento(veff)




    listaResultados = lista_em + mediciones_em + lista_evc + mediciones_evc + mediciones_ea + listaCoeficiente_sen + lista_duda + lista_reduccion + datos_uxi + datos_uyi + lista_grados_libertad

    listaResultados.append(id_serial)

    

    #Insertar en la tabla sef_tcalculos_incert_dosificacion

    
    sql_calculos_dosificacion = crear_query(listaResultados)


    db.session.execute(sql_calculos_dosificacion)
    db.session.commit()

    #Calcular la incertidumbre expandida (uE)

    incertidumbre_expandida_uE = calcular_incertidumbre_expandida(factor_cubrimiento,incertidumbre_estandarCombinada_evc)


    conformidad_dosificacion = esConforme(mediciones_evc[0], incertidumbre_estandarCombinada_evc,lep_permisible)
    
    

    sql_result_dosificacion = text(f'''INSERT 
                                    INTO SEF_TRESULT_INCERT_DOSIFICACION(
                                    DMEV_ID_SERIAL,RESDN_ERROR_DOSIF,
                                    RESDN_INCERT_DOSIF,RESDV_EVAL_CONFORM,
                                    RESDN_VALOR_EFECTIVO,RESDN_NIVEL_CONFIANZA,
                                    RESDN_INCERT_ESTAND_COMB,RESDN_FACTOR_CUBRIMIENTO)
                                    VALUES(
                                        {id_serial},{mediciones_evc[0] if lista_evc[0] is not None else 'NULL'},
                                        {incertidumbre_expandida_uE if incertidumbre_expandida_uE is not None else 'NULL'},'{conformidad_dosificacion}',
                                        {veff},{95.45},
                                        {incertidumbre_estandarCombinada_evc if incertidumbre_estandarCombinada_evc is not None else 'NULL'},
                                        {factor_cubrimiento})''')
    
    db.session.execute(sql_result_dosificacion)
    db.session.commit()





#Funciones


#Energia medida
def calcular_Em(lectura_final,lectura_inicial):

    return lectura_final -lectura_inicial



#Error ensayo verificacion de la constante
def calcular_Evc(em,ea,error_medio_Imax):

    if error_medio_Imax is not None:
        em=float(em)
        ea=float(ea)
        error_medio_Imax=float(error_medio_Imax)
        resultado = (((em - ea)/ ea) * 100) - (error_medio_Imax)
        return resultado
    else:
        return None


def calcular_promedio_e_medidas(lista):
    if None in lista:
        return None
    else:
        return mn(lista)


def calcular_desv_est_medidas(lista):
    if None in lista:
        return None
    else:
        return stdev(lista)


def calcular_desv_est_smed(desv_est_medidas):
    if desv_est_medidas is not None:
        desv_est_medidas = float(desv_est_medidas)
        return desv_est_medidas / math.sqrt(3)
    else:
        return None



def calcular_coeficiente_sensibilidad_Em(promedio):
    if promedio is not None:
        return float(100/promedio)
    else:
        return None

def calcular_coeficiente_sensibilidad_Ea(promedio_Em,promedio_Ea):
    resultado = -100*promedio_Em/(promedio_Ea **2)
    return resultado


def calcular_error_EPM(error_incertidumbre_EPM,media_ea):

    resultado = (error_incertidumbre_EPM/100)*media_ea
    
    return resultado


def calcular_incert_EPM(incertidumbre_EPM,media_ea):

    resultado = (incertidumbre_EPM/100)*media_ea
    
    return resultado

def calcular_deriva_ud(deriva,media_ea):
    resultado = (deriva/100)*media_ea
    
    return resultado

def calcular_uxi(duda,reduccion):
        
    if duda is not None and reduccion is not None:
        duda = float(duda)
        reduccion = float(reduccion)
        if duda !=0:
            return (duda/reduccion)
        else:
            return 0.0
    else:
        return None

def calcular_uyi(uxi,coeficiente_sensibilidad):
    
    if uxi is not None and coeficiente_sensibilidad is not None:
        uxi = float(uxi)
        coeficiente_sensibilidad = float(coeficiente_sensibilidad)
        return uxi*coeficiente_sensibilidad
    else:
        return None


def crearDiccionario(lista, valor):
    diccionario = dict()

    for index,i in enumerate(lista):
        
        diccionario[f'{valor}{index+1}'] = i
    return diccionario



def calcular_veff(diccionarioUyi, dicc_grado_libertad, incertidumbreExpandida_evc):

    try:
        suma1 = sum([math.pow(diccionarioUyi['Uy1'], 4) / dicc_grado_libertad['grado_efectivo_libertadx1'], math.pow(diccionarioUyi['Uy2'], 4) / dicc_grado_libertad['grado_efectivo_libertadx2']])

        suma2 = sum([math.pow(diccionarioUyi['Uy3'], 4) / dicc_grado_libertad['grado_efectivo_libertadx3'], math.pow(diccionarioUyi['Uy4'], 4) / dicc_grado_libertad['grado_efectivo_libertadx4'], math.pow(diccionarioUyi['Uy5'], 4) / dicc_grado_libertad['grado_efectivo_libertadx5'], math.pow(diccionarioUyi['Uy6'], 4) / dicc_grado_libertad['grado_efectivo_libertadx6'], math.pow(diccionarioUyi['Uy7'], 4) / dicc_grado_libertad['grado_efectivo_libertadx7']])
            
        suma3 = math.pow(diccionarioUyi['Uy8'], 4) / dicc_grado_libertad['grado_efectivo_libertadx8']

        resultado = math.pow(incertidumbreExpandida_evc, 4) / (suma1 + suma2 + suma3)

        return resultado
    
    except Exception as e:
        resultado = 9999

    return resultado

#El uso de *args me permite agregar tantos parametros como sea posible
def calcular_incertidumbre_estandar_comb(*args):
    tuplaValores = args
    listaValores = []

    for i in tuplaValores:
        valor = i**2
        listaValores.append(valor)

    resultado = math.sqrt(sum(listaValores))

    return resultado


def calcular_incertidumbre_estandar_evc(lista):
    resultados = []
    if None in lista:
        return None
    else:
        for i in lista:
            resultados.append(i**2)

        result = math.sqrt(sum(resultados))
        return result


def calcular_factor_cubrimiento(veff):

    if (veff > 100):
        resultado = 2.00
    else:
        resultado = t.ppf(1-0.0455/2,round(veff,0))

    return resultado




def calcular_incertidumbre_expandida(factor_cubrimiento, incertidumbre_estandarCombinada_evc):
    
    if factor_cubrimiento is not None and incertidumbre_estandarCombinada_evc is not None:
        return factor_cubrimiento*incertidumbre_estandarCombinada_evc
    else: 
        return None


def calcular_reduccion(valor_distribucion):

    if valor_distribucion is not None:

        match valor_distribucion:
            case 'normal':
                resultado = 1.00
            case 'rectangular':
                resultado = float(math.sqrt(3))
            case 'triangular':
                resultado = float(math.sqrt(6))
            case _:
                resultado = 1.96

        return resultado
    else:
        return None


def calcular_grado_efectivo(distribucion,lista_evc):
    

    match(distribucion):

        case 'normal':
            resultado = float(len(lista_evc)-1)
        case 'rectangular':
            resultado = 1000000
        case 'triangular':
            resultado = 1000000
        case _:
            resultado =  1000000

    return resultado


def esConforme(ensayo_verificacion,incertidumbre_estandarCombinada_evc,lep_permisible):

    try:
        incertidumbre_estandarCombinada_evc = float(incertidumbre_estandarCombinada_evc)
        ensayo_verificacion = float(ensayo_verificacion)
        lep_permisible = float(lep_permisible)

        expresionEvaluacion = (1.64 * abs(incertidumbre_estandarCombinada_evc))

            
        if abs(ensayo_verificacion) <= (abs(lep_permisible) - (1.64 * abs(expresionEvaluacion))):
                
            return 'CEVC'
        else:
        
            return 'NCEVC'

        
    except Exception as e:

        result = 'NCEVC'

    return result
    
    


# para tomar un numero n de valores y transformarlos en una lista
def crearLista(*args):
    lista = list(args)
    return lista





def crear_query(lista):
    
    valores_str = ', '.join(['NULL' if valor is None else str(valor) for valor in lista])

    if valores_str is not None:



        query = text(f'''INSERT INTO SEF_TCALCULOS_INCERT_DOSIFICACION(
                                CALDN_ENERG_MEDIDA_UNO, CALDN_ENERG_MEDIDA_DOS, 
                                CALDN_ENERG_MEDIDA_TRES, CALDN_ENERG_MEDIDA_MEDIA,
                                CALDN_DESV_ESTD_MEDIDAS, CALDN_DESV_ESTD_ENERG_MED,
                                CALDN_ERROR_VERF_CONST_UNO,CALDN_ERROR_VERF_CONST_DOS,
                                CALDN_ERROR_VERF_CONST_TRES, CALDN_ERROR_MEDIA,
                                CALDN_DES_EST_ERROR, CALDN_DES_EST_ERROR_MEDIA,
                                CALDN_ENERG_APLIC_MEDIA, CALDN_DES_EST_ENERG_APLIC,
                                CALDN_DES_EST_ENERG_APLIC_MEDIA, CALDN_COEF_SENS_ENERG_MEDIDA,
                                CALDN_COEF_SENS_ENERG_APLICADA, CALDN_COEF_SENS_INCERT_COMB,
                                CALDN_DUDA_ENERG_MEDIDA_REPT, CALDN_DUDA_ENERG_MEDIDA_RESOL_MED,
                                CALDN_DUDA_ENERG_APLIC_REPT, CALDN_DUDA_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_DUDA_ERROR_EPM, CALDN_DUDA_INCERT_EPM,
                                CALDN_DUDA_DERIVA, CALDN_DUDA_INCERT_COMB,
                                CALDN_REDUC_ENERG_MEDIDA_REPT, CALDN_REDUC_ENERG_MEDIDA_RESOL_MED,
                                CALDN_REDUC_ENERG_APLIC_REPT, CALDN_REDUC_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_REDUC_ERROR_EPM, CALDN_REDUC_INCERT_EPM,
                                CALDN_REDUC_DERIVA, CALDN_REDUC_INCERT_COMB,
                                CALDN_UXI_ENERG_MEDIDA_REPT, CALDN_UXI_ENERG_MEDIDA_RESOL_MED,
                                CALDN_UXI_ENERG_APLIC_REPT, CALDN_UXI_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_UXI_ERROR_EPM, CALDN_UXI_INCERT_EPM,
                                CALDN_UXI_DERIVA, CALDN_UXI_INCERT_COMB,
                                CALDN_UYI_ENERG_MEDIDA_REPT, CALDN_UYI_ENERG_MEDIDA_RESOL_MED,
                                CALDN_UYI_ENERG_APLIC_REPT, CALDN_UYI_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_UYI_ERROR_EPM, CALDN_UYI_INCERT_EPM,
                                CALDN_UYI_DERIVA, CALDN_UYI_INCERT_COMB,
                                CALDN_GRAD_LIB_ENERG_MED_REPT, CALDN_GRAD_LIB_ENERG_MED_RESOL_MED,
                                CALDN_GRAD_LIB_ENERG_APLIC_REPT, CALDN_GRAD_LIB_ENERG_MED_RESOL_EPM,
                                CALDN_GRAD_LIB_ERROR_EPM, CALDN_GRAD_LIB_INCERT_EPM,
                                CALDN_GRAD_LIB_DERIVA, CALDN_GRAD_LIB_INCERT_COMB, DMEV_ID_SERIAL) 
                                VALUES({valores_str})''')
    

    else:
        query = text(f'''INSERT INTO SEF_TCALCULOS_INCERT_DOSIFICACION(
                                CALDN_ENERG_MEDIDA_UNO, CALDN_ENERG_MEDIDA_DOS, 
                                CALDN_ENERG_MEDIDA_TRES, CALDN_ENERG_MEDIDA_MEDIA,
                                CALDN_DESV_ESTD_MEDIDAS, CALDN_DESV_ESTD_ENERG_MED,
                                CALDN_ERROR_VERF_CONST_UNO,CALDN_ERROR_VERF_CONST_DOS,
                                CALDN_ERROR_VERF_CONST_TRES, CALDN_ERROR_MEDIA,
                                CALDN_DES_EST_ERROR, CALDN_DES_EST_ERROR_MEDIA,
                                CALDN_ENERG_APLIC_MEDIA, CALDN_DES_EST_ENERG_APLIC,
                                CALDN_DES_EST_ENERG_APLIC_MEDIA, CALDN_COEF_SENS_ENERG_MEDIDA,
                                CALDN_COEF_SENS_ENERG_APLICADA, CALDN_COEF_SENS_INCERT_COMB,
                                CALDN_DUDA_ENERG_MEDIDA_REPT, CALDN_DUDA_ENERG_MEDIDA_RESOL_MED,
                                CALDN_DUDA_ENERG_APLIC_REPT, CALDN_DUDA_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_DUDA_ERROR_EPM, CALDN_DUDA_INCERT_EPM,
                                CALDN_DUDA_DERIVA, CALDN_DUDA_INCERT_COMB,
                                CALDN_REDUC_ENERG_MEDIDA_REPT, CALDN_REDUC_ENERG_MEDIDA_RESOL_MED,
                                CALDN_REDUC_ENERG_APLIC_REPT, CALDN_REDUC_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_REDUC_ERROR_EPM, CALDN_REDUC_INCERT_EPM,
                                CALDN_REDUC_DERIVA, CALDN_REDUC_INCERT_COMB,
                                CALDN_UXI_ENERG_MEDIDA_REPT, CALDN_UXI_ENERG_MEDIDA_RESOL_MED,
                                CALDN_UXI_ENERG_APLIC_REPT, CALDN_UXI_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_UXI_ERROR_EPM, CALDN_UXI_INCERT_EPM,
                                CALDN_UXI_DERIVA, CALDN_UXI_INCERT_COMB,
                                CALDN_UYI_ENERG_MEDIDA_REPT, CALDN_UYI_ENERG_MEDIDA_RESOL_MED,
                                CALDN_UYI_ENERG_APLIC_REPT, CALDN_UYI_ENERG_MEDIDA_RESOL_EPM,
                                CALDN_UYI_ERROR_EPM, CALDN_UYI_INCERT_EPM,
                                CALDN_UYI_DERIVA, CALDN_UYI_INCERT_COMB,
                                CALDN_GRAD_LIB_ENERG_MED_REPT, CALDN_GRAD_LIB_ENERG_MED_RESOL_MED,
                                CALDN_GRAD_LIB_ENERG_APLIC_REPT, CALDN_GRAD_LIB_ENERG_MED_RESOL_EPM,
                                CALDN_GRAD_LIB_ERROR_EPM, CALDN_GRAD_LIB_INCERT_EPM,
                                CALDN_GRAD_LIB_DERIVA, CALDN_GRAD_LIB_INCERT_COMB, DMEV_ID_SERIAL) 
                                VALUES( NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL,NULL,
                                        NULL,NULL,NULL,NULL)''')

    return query







if __name__=="__main__":
    main()
