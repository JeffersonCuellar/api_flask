from utils.db import db,ma



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

medicion_schema = MedicionSchema()
mediciones_schema = MedicionSchema(many=True)
