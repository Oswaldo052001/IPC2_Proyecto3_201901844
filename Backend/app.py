from flask import jsonify, Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def postHome():
    return jsonify({'message': 'respuesta post'})


@app.route('/', methods=['GET']) 
def getHome():
    return jsonify({'message': 'respuesta get'})

@app.route('/adduser', methods=['POST'])
def addUser():
    if request.method == 'POST':
        nombreLeido = request.form['txbnombre']
        mipass = request.form['txbpass']

        return jsonify({'message': 'usuario agregado', 'nombre': nombreLeido, 'pass': mipass})
        
@app.route('/adduserbybody', methods=['POST'])

def addUserBody():
    micurso = request.json['curso']
    miseccion = request.json['seccion']
    return jsonify({'message': 'Curso agregado', 'curso': micurso, 'seccion': miseccion})    
   

if __name__ == '__main__':
    app.run(debug=True, port=3050)