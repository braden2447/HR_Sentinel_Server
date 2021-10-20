from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


@app.route("/", methods=["GET"])
def status():
    return "Server is on"


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    return None, 500


@app.route("/api/new_attending", methods=["POST"])
def new_attending():
    return None, 500


@app.route("/api/heart_rate", methods=["POST"])
def heart_rate():
    return None, 500


@app.route("/api/status/<patient_id>", methods=["GET"])
def status_pid(patient_id):
    return None, 500


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def heart_rate_pid(patient_id):
    return None, 500


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def heart_rate_avg_pid(patient_id):
    return None, 500


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def heart_rate_interval_avg():
    return None, 500


@app.route("/api/patients/<attending_username>", methods=["GET"])
def patients_attending_username(attending_username):
    return None, 500


if __name__ == "__main__":
    app.run()
