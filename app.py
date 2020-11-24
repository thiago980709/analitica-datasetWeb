from flask import Flask, jsonify,request,render_template,send_file
import requests
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage




app = Flask(__name__,template_folder='templates')

app.config['UPLOAD_FOLDER'] ='./Archivos'

listaProyectos = [{"id":1,"nombre":"Analisis producción de el mes"},{"id":2,"nombre":"Identificación de sobre producción"},{"id":3,"nombre":"Predecir comportamiento de el cultivo"}]

encargados = ['Santiago Castaneda','Camilo Sanmartin','Andres Arango','Juan Bernardo']
@app.route('/listarDatasets',methods=['GET'])
def listarDatasets():
    datasets = requests.get('https://analiticadataset-api.ue.r.appspot.com/dataSet').json()
    return render_template('listarDatasets.html',datasets=datasets)

@app.route('/crearDatset',methods=['GET'])
def crearDatset():
    return render_template('crearDataset.html',proyectos=listaProyectos,encargados=encargados)

@app.route('/eliminar/<id>')
def eliminar(id):
    requests.delete('https://analiticadataset-api.ue.r.appspot.com/dataSet/delete/'+id)
    return listarDatasets()

@app.route('/descargarArchivo/<string:archivo>')
def descargarArchivo (archivo):
    path = "Archivos/"+archivo
    return send_file(path, as_attachment=True)

@app.route("/guardarDataset",methods=['POST'])
def guardarDataset():
    dataset = dict(request.values)
    proyectoInfo = dataset['idProyecto'].split("-")
    dataset['nombreProyecto'] = str(proyectoInfo[1])
    dataset['idProyecto'] = int(proyectoInfo[0])

    f = request.files['archivo']
    nombreArchivo = secure_filename(f.filename)
    ##f.save(os.path.join(app.config['UPLOAD_FOLDER'],nombreArchivo))
    ruta = './Archivos/'+nombreArchivo
    dataset['archivoDir'] = ruta
    dataset['archivoNombre'] = nombreArchivo

    requests.post('https://analiticadataset-api.ue.r.appspot.com/dataSet',json=dataset)
    return(listarDatasets())

