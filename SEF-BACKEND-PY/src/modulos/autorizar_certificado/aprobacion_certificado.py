
import openpyxl
from openpyxl.drawing.image import Image
import win32com.client as cpdf
from sqlalchemy import text
import pythoncom
import os


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

def main(id_tanda, list_certificados, conn1):
    
    
    aprobado = ''
    data_certificados = []

    
    with conn1.connect() as connection_sef:

        cant_certificados = len(list_certificados)

        i=0
        while(i<cant_certificados):
            
            pythoncom.CoInitialize()
            
            query = (text(f'''SELECT DISTINCT cc.ccd_fecha_emision, cc.ccn_est_aprobacion
                            FROM SEF_TDATOS_MEDIDORES dt, SEF_TCERTIFICADOS_CALIBRACION cc
                            WHERE dt.dmev_id_tanda = :id_tanda AND cc.ccn_num_certificado = :list_certificados'''))

            obj_fecha, est_certificado = connection_sef.execute(query, {'id_tanda': id_tanda, 'list_certificados': list_certificados[i]}).fetchone()
            fecha = obj_fecha.strftime("%Y-%m-%d")

            data_cert = list_certificados[i],fecha

            data_certificados.append(data_cert)

            if est_certificado == 0:
                
                    excel_file = os.path.join(base_dir, 'src', 'certificados_calibracion', 'certificados_excel', f'{fecha}_certificado_{list_certificados[i]}.xlsx')

                    workbook = openpyxl.load_workbook(excel_file)
                    sheet = workbook.active

                    # Insertamos firma
                    img_path = os.path.join(base_dir,'src','images','firma.png')
                    firma = Image(img_path)

                    firma.width = 150  
                    firma.height = 50

                    sheet.add_image(firma, 'T54')  

                    pdf_file_temp = os.path.join(base_dir, 'src','certificados_calibracion', 'certificados_pdf', f'{fecha}_certificado_{list_certificados[i]}.xlsx')  

                    temp_excel_file = pdf_file_temp
                    workbook.save(temp_excel_file)



                    pdf_file = os.path.join(base_dir, 'src','certificados_calibracion', 'certificados_pdf', f'{fecha}_certificado_{list_certificados[i]}.pdf')  

                    excel = cpdf.Dispatch("Excel.Application")
                    excel.Visible = False  

                    workbook_excel = excel.Workbooks.Open(temp_excel_file)


                    workbook_excel.ExportAsFixedFormat(0, pdf_file)

                    workbook_excel.Close(SaveChanges=False)
                    excel.Quit()

                
                    os.remove(temp_excel_file)

                    pythoncom.CoUninitialize()

                    sql_insert = text(f'''UPDATE SEF_TCERTIFICADOS_CALIBRACION
                                            SET CCN_EST_APROBACION = 1
                                            WHERE CCN_NUM_CERTIFICADO = {list_certificados[i]}
                                            ''')
                    connection_sef.execute(sql_insert)
                    connection_sef.commit()
                    if len(list_certificados) == 1:
                        aprobado = F'Certificado {list_certificados} aprobado'
                    else:
                        aprobado = F'Certificados {list_certificados} aprobados'
                    
                        
                        
            else:
                aprobado = 'Este certificado ya ha sido firmado anteriormente'
                
            i+=1


        return data_certificados,aprobado


if __name__ == '__main__':
    main(debug=True)
