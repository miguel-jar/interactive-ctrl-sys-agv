<!-- # path-follower-robot
Desenha-se o trajeto em uma interface web e o robô segue a trajetória desenhada.

* [Ensaio 1](https://youtu.be/cj4z1ridE08)
* [Ensaio 2](https://youtu.be/_qWvqBL0OQY)
* [Ensaio 3](https://youtu.be/jRkqLKHnnJs)

Link para o [artigo](https://biblioteca.inatel.br/cict/acervo%20publico/Sumarios/Artigos%20de%20TCC/TCC_Gradua%C3%A7%C3%A3o/Engenharia%20de%20Controle%20e%20Automa%C3%A7%C3%A3o/2024/Sistema%20de%20Controle%20Interativo.pdf) (PT-BR)

Artigo traduzido e publicado no Congresso Internacional ICCMA 2025 (IEEE), realizado em Paris (França). -->

# Autonomous Path-Following Robot 🤖🛰️

This project consists of an integrated system for an autonomous robot that follows trajectories generated from DXF/SVG maps. It combines **Arduino** for hardware control, **Flask** for the web interface, and **YOLOv8** for trajectory error analysis.

---

## 🛠️ System Architecture

The project is divided into three main modules:

1.  **Firmware (Arduino):** Low-level control using C++ to manage robot actuators and sensors.
2.  **Web Server (Python/Flask):** A dashboard to upload maps, define paths, and start/stop the robot.
3.  **Vision & Analytics (YOLO/Matplotlib):** A post-processing pipeline that uses YOLOv8 to detect the robot and the path, calculating the **MSE** and **RMSE** of the execution.

---

## 📂 Project Structure

```text
├── arduino_code/
│   └── arduino_code.ino      # C++ Robot logic
├── python_web_server/
    ├── templates/              # HTML dashboards
    ├── static/                 # CSS/JS and generated graphs
│   ├── server.py               # Flask application
│   ├── data_sender.py          # Serial communication logic
│   ├── map_processing/         # DXF to SVG conversion
│   └── settings.yaml           # Global configurations
├── vision_module/
    ├── models/                 # YOLOv8 trained weights (.pt)
    ├── predict.py              # Inference script
    └── error_analysis.ipynb    # Accuracy metrics (MSE/RMSE)
```

---

## ⚙️ Installation

### 1. Prerequisites

**Python 3.11+**

### 2. Cloning the Repository

```bash
git clone https://github.com/miguel-jar/path-follower-robot.git
```

### 3. Installing Required Packages

Install dependencies using your preferred environment method (conda or pip). Open a terminal, inside robot-combate-pts-sys folder, and type:

```bash
pip install -r requirements.txt
```

or

```bash
conda env create -f environment.yml
```

---

## 🖥️ Run

Inside project folder, type:

```bash
cd python_web_servery
python server.py
```

---

## 📊 Performance Analysis
The system includes a evaluation module. After each run, the vision system detects the robot's real-time position against the target path to calculate precision:

Mean Squared Error (MSE): Measures the average squared difference between estimated and actual positions.

Root Mean Squared Error (RMSE): Provides the error margin in centimeters (CM).