from utils.db import db,ma

class SEF_CERTIFICADOS_CALIBRACION():
    __bind_key__ = 'db_sac'
    CCN_ID_CERTIFICADO = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    CCN_NUM_CERTIFICADO = db.Columb(db.Integer)
    DMEV_ID_TANDA = db.Column(db.Integer)
    DMEV_ID_SERIAL = db.Column(db.Integer)
    EQUN_ID_EPM = db.Column(db.Integer)
    CCD_FECHA_EMISION = db.Column(db.Date)


    def __init__(self,CCN_ID_CERTIFICADO,CCN_NUM_CERTIFICADO,DMEV_ID_TANDA,DMEV_ID_SERIAL,CCD_FECHA_EMISION):
        self.CCN_ID_CERTIFICADO = CCN_ID_CERTIFICADO
        self.CCN_NUM_CERTIFICADO = CCN_NUM_CERTIFICADO
        self.DMEV_ID_TANDA = DMEV_ID_TANDA
        self.DMEV_ID_SERIAL = DMEV_ID_SERIAL
        self.CCD_FECHA_EMISION = CCD_FECHA_EMISION

class CertifcadoSchema(ma.Schema):
    class Meta:
        fields = ('CCN_ID_CERTIFICADO','CCN_NUM_CERTIFICADO','DMEV_ID_TANDA','DMEV_ID_SERIAL','CCD_FECHA_EMISION')


certificado_schema = CertifcadoSchema()
certificados_schema = CertifcadoSchema(many=True)