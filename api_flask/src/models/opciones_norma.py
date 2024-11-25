from utils.db import db,ma



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


opNorma_schema = OpNormaSchema()
opNormas_schema = OpNormaSchema(many=True)