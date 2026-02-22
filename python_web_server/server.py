import json
import os
import threading

import yaml
from flask import Flask, flash, jsonify, redirect, render_template, request

from data_sender import send_points
from map_processing.map_processing import generate_map

app = Flask(__name__)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in settings["ALLOWED_EXTENSIONS"]
    )


@app.route("/", methods=["GET", "POST"])
def index():
    return redirect("/upload_map")


@app.route("/upload_map", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            dxf_path = os.path.join(app.config["UPLOAD_FOLDER"], "map.DXF")
            file.save(dxf_path)
            generate_map(dxf_path)
            return redirect("/submit-trajectory")

    return render_template(settings["UPLOAD_PAGE"])


@app.route("/submit-trajectory", methods=["POST", "GET"])
def submit_trajectory():
    if request.method == "POST":
        global trajectory
        trajectory = request.json.get("trajectory")

        # Here you can process the trajectory, send it to the robot, etc.
        print("Trajectory received:", trajectory)
        return jsonify({"status": "success", "trajectory": trajectory})

    return render_template(settings["MAP_PAGE"])


@app.route("/get-configs", methods=["GET"])
def get_settings():
    with open(settings["PATH_JSON"], "r") as config_file:
        args = json.load(config_file)
    return args


@app.route("/set-origin", methods=["POST"])
def set_origin():
    global origin
    origin = request.json.get("origin")
    print("Origin received:", origin)
    return "Origin defined!"


@app.route("/start-stop", methods=["POST"])
def start_stop_robot():
    action = request.json.get("action")
    msg = ""

    if not origin:
        msg = "Could not start robot. Origin not defined."
    elif not trajectory:
        msg = "Could not start robot. Trajectory not defined."

    elif action == "start":
        stop_event.clear()
        args = (
            settings["USB_PORT"],
            settings["BAUDRATE"],
            origin,
            trajectory,
            settings["HEADER"],
            settings["START_SEQ"],
            settings["STOP_SEQ"],
            stop_event,
            settings["SAVE_PATH"],
            settings["SAVE_PATH_ALL"],
        )

        thread = threading.Thread(target=send_points, args=args)
        thread.start()
        msg = "Robot started"

    elif action == "stop":
        stop_event.set()
        msg = "Robot stopped"

    return msg


@app.route("/get-chart", methods=["GET"])
def get_chart():
    return render_template(settings["CHART_PAGE"])


if __name__ == "__main__":
    # Load standardized settings file
    with open("settings.yaml", "r") as file:
        settings = yaml.load(file, yaml.SafeLoader)

    stop_event = threading.Event()
    origin, trajectory = [], []

    app.secret_key = "28b866b0a4ebd0c09f2ab98981155ce9070229463f6810df"
    app.config["UPLOAD_FOLDER"] = settings["UPLOAD_FOLDER"]
    app.run(host="0.0.0.0", port=5000)
