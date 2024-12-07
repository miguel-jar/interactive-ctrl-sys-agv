from flask import Flask, flash, request, redirect, render_template, jsonify
from proc_mapa.proc_mapa import get_mapa
import os, json

paginaUpload = 'upload_mapa.html'
paginaMapa = 'mapa.html'
pathJson = 'static/config.json'

UPLOAD_FOLDER = 'proc_mapa/mapas'
ALLOWED_EXTENSIONS = {'dxf'}

app = Flask(__name__)
app.secret_key = b'miguel'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            caminhoDXF = os.path.join(app.config['UPLOAD_FOLDER'], 'mapa.DXF')
            file.save(caminhoDXF)
            get_mapa(caminhoDXF)
            return redirect('/submit-trajectory')

    return render_template(paginaUpload)

@app.route('/submit-trajectory', methods=['POST', 'GET'])
def submit_trajectory():
    if request.method == 'POST':
        data = request.json
        trajectory = data.get('trajectory')
        
        # Aqui você pode processar a trajetória, enviá-la ao robô, etc.
        print("Trajetória recebida:", trajectory)
        return jsonify({"status": "success", "trajectory": trajectory})
    
    return render_template(paginaMapa)

@app.route('/get-configs', methods=['GET'])
def submit_configs():
    with open(pathJson, 'r') as configs:
        args = json.load(configs)
    return args

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)