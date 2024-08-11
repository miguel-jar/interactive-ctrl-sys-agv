from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pagina.html')

@app.route('/submit-trajectory', methods=['POST'])
def submit_trajectory():
    data = request.json
    trajectory = data.get('trajectory')
    
    # Aqui você pode processar a trajetória, enviá-la ao robô, etc.
    print("Trajetória recebida:", trajectory)
    
    return jsonify({"status": "success", "trajectory": trajectory})

if __name__ == '__main__':
    app.run(host='192.168.1.2', port=5000)