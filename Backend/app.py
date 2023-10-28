from flask import jsonify, Flask, request, send_file
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename
from flask_cors import CORS
from Lecturaxml import lecturaxml, Eliminar
from Peticiones import peticiones
import os
import re

app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] =  "ArchivosEntradas"
ALLOWED_EXTENSIONS = set(['xml'])


@app.route('/grabarMensajes', methods=['POST'])
def subirArchivo():
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    url = "ArchivosEntradas/"+filename
    '''try:
        lecturaxml(url)
        return jsonify({'archivo': filename, 'message': 'Carga exitosa'})
    except:
        return jsonify({'archivo': filename, 'message': 'Ocurrió un error'})'''
    return jsonify({'archivo': filename, 'message': 'Carga exitosa'})

@app.route('/limpiarDatos', methods=['POST'])
def eliminarDatos():
    Eliminar()
    return jsonify({'message': 'Se elimino correctamente'})

@app.route('/devolverHashtags', methods=['POST'])
def peticionHastags():
    if request.method == 'POST':
        try:
            ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"
            fechainicio = request.form['fechainicio']
            fechainicioSeparada = fechainicio.split()

            for fecha in fechainicioSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaInicioEncontrada = fecha



            fechafin = request.form['fechafin']
            fechafinSeparada = fechafin.split()

            for fecha in fechafinSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaFinEncontrada = fecha

            peticiones("consultarHashtags",fechaInicioEncontrada,fechaFinEncontrada)
            return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PeticionesHashtags.xml')
        except:
            return jsonify({'message': 'Error en el formato de las fechas: dd/mm/yyyy revise que la fecha sea correcta'}) 


@app.route('/devolverMenciones', methods=['POST'])
def peticionMencion():
    if request.method == 'POST':
        try:
            ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"
            fechainicio = request.form['fechainicio']
            fechainicioSeparada = fechainicio.split()

            for fecha in fechainicioSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaInicioEncontrada = fecha



            fechafin = request.form['fechafin']
            fechafinSeparada = fechafin.split()

            for fecha in fechafinSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaFinEncontrada = fecha

            peticiones("consultarMenciones",fechaInicioEncontrada,fechaFinEncontrada)
            return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PeticionesMenciones.xml')
        except:
            return jsonify({'message': 'Error en el formato de las fechas: dd/mm/yyyy revise que la fecha sea correcta'}) 
        

@app.route('/devolverSentimientos', methods=['POST'])
def peticionSentimientos():
    if request.method == 'POST':
        try:
            ER_fecha = r"\b(0[1-9]|[12]\d|3[01])[/](0[1-9]|1[0-2])[/](19\d\d|20\d\d)\b"
            fechainicio = request.form['fechainicio']
            fechainicioSeparada = fechainicio.split()

            for fecha in fechainicioSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaInicioEncontrada = fecha


            fechafin = request.form['fechafin']
            fechafinSeparada = fechafin.split()

            for fecha in fechafinSeparada:
                if re.findall(ER_fecha,fecha):
                    fechaFinEncontrada = fecha

            peticiones("consultarSentimientos",fechaInicioEncontrada,fechaFinEncontrada)
            return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PeticionesSentimientos.xml')
        except:
            return jsonify({'message': 'Error en el formato de las fechas: dd/mm/yyyy revise que la fecha sea correcta'}) 
#------------------------------------------- FUNCIONES POST PARA PEDIR BASE DE DATOS ------------------------------------------------

@app.route('/DB_Mensajes', methods=['GET']) 
def getMensajes():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/Fechas.xml')

@app.route('/DB_PalabrasPositivas', methods=['GET']) 
def getPalabrasPositivas():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PalabrasPositivas.xml')

@app.route('/DB_PalabrasNegativas', methods=['GET']) 
def getPalabrasNegativas():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PalabrasNegativas.xml')
    
@app.route('/DB_PalabrasPositivasRechazadas', methods=['GET']) 
def getPalabrasPositivasRechazadas():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PalabrasPosiRechazadas.xml')

@app.route('/DB_PalabrasNegativasRechazadas', methods=['GET']) 
def getPalabrasNegativasRechazadas():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/DateBase/PalabrasNegaRechazadas.xml')


@app.route('/ResumenMensajes', methods=['GET']) 
def getResumenMensajes():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/ArchivosSalidas/resumenMensajes.xml')


@app.route('/ResumenConfig', methods=['GET']) 
def getResumenConfig():
    return send_file('C:/Users/bryan/Documents/Oswaldo/USAC/2023/SEGUNDO SEMESTRE 2023/IPC 2/LABORATORIO/Proyecto3_IPC2/Proyecto3/IPC2_Proyecto3_201901844/ArchivosSalidas/resumenConfig.xml')

if __name__ == '__main__':
    app.run(debug=True, port=3050)