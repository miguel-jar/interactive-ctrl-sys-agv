from flask import Flask, flash, request, redirect, render_template, jsonify
from proc_mapa.proc_mapa import get_mapa
from envio_dados import envia_pontos
import json, os, threading, yaml

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in configs['ALLOWED_EXTENSIONS']

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

    return render_template(configs['PAGINA_UPLOAD'])

@app.route('/submit-trajectory', methods=['POST', 'GET'])
def submit_trajectory():
    if request.method == 'POST':
        data = request.json

        global trajectory 
        trajectory = data.get('trajectory')

        # Aqui você pode processar a trajetória, enviá-la ao robô, etc.
        print("Trajetória recebida:", trajectory)
        return jsonify({"status": "success", "trajectory": trajectory})
    
    return render_template(configs['PAGINA_MAPA'])

@app.route('/get-configs', methods=['GET'])
def submit_configs():
    with open(configs['PATH_JSON'], 'r') as config:
        args = json.load(config)
    return args

@app.route('/start-stop', methods=['POST'])
def start_stop_robot():
    data = request.data.decode()
    global trajectory

    if data == 'start':
        stop_event.clear()
        args = (configs['PORTA_USB'], configs['BAUDRATE'], trajectory, 
                configs['START_SEQ'], configs['STOP_SEQ'], configs['HEADER'], stop_event)
        
        thread = threading.Thread(target=envia_pontos, args=args)
        thread.start()
        return 'Robo iniciado'

    elif data == 'stop':
        stop_event.set()
        return 'Robo desligado'


if __name__ == '__main__':
    
    with open('configs.yaml', 'r') as arquivo:
        configs = yaml.load(arquivo, yaml.SafeLoader)

    stop_event = threading.Event()
    
    app.secret_key = b'miguel'
    app.config['UPLOAD_FOLDER'] = configs['UPLOAD_FOLDER']
    app.run(host='0.0.0.0', port=5000)