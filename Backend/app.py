from flask import jsonify, Flask, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from Lecturaxml import lecturaxml
from EliminarDatos import Eliminar
import os


app = Flask(__name__)
CORS(app)

app.config["UPLOAD_FOLDER"] =  "ArchivosEntradas"
ALLOWED_EXTENSIONS = set(['xml'])


@app.route('/upload', methods=['POST'])
def subirArchivo():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"],filename))
    url = "ArchivosEntradas/"+filename
    lecturaxml(url)
    return jsonify({'archivo': filename, 'message': 'Carga exitosa'})


@app.route('/eliminarDatos', methods=['POST'])
def eliminarDatos():
    Eliminar().eliminarDatosFechas()
    return jsonify({'message': 'Se elimino correctamente'})


@app.route('/', methods=['POST'])
def postHome():
    return jsonify({'message': 'respuesta post'})


@app.route('/', methods=['GET']) 
def getHome():
    return jsonify({'message': 'respuesta get'})
        
if __name__ == '__main__':
    app.run(debug=True, port=3050)