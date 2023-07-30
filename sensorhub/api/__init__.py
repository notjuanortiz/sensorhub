import json
import sqlite3

from flask import Flask, redirect
from flask_restful import Api

app = Flask(__name__)
api = Api(app)


def create_db():
    with connect_to_db() as connection:
        with open('schema.sql') as file:
            connection.executescript(file.read())

        connection.commit()


def connect_to_db():
    connection = sqlite3.connect("database.db")
    return connection


@app.route("/")
def index():
    return redirect("/sensors/")


@app.route("/sensors/", methods=['GET'])
def get_sensors():
    with connect_to_db() as connection:
        connection.row_factory = sqlite3.Row
        query = "SELECT id, measurement, location FROM sensors"
        sensors = connection.execute(query).fetchall()
    return format_rows_as_json(sensors), 200


@app.route("/sensors/<sensor_id>/", methods=['GET'])
def get_sensor(sensor_id: int):
    with connect_to_db() as connection:
        connection.row_factory = sqlite3.Row
        query = "SELECT id, measurement, location FROM sensors WHERE id = ?"
        sensor = connection.execute(query, sensor_id).fetchone()
        return format_row_as_json(sensor), 200


def format_row_as_json(sensor):
    return json.dumps(dict(zip(sensor.keys(), sensor)))


def format_rows_as_json(sensors):
    sensor_list = []
    for sensor in sensors:
        d = dict(zip(sensor.keys(), sensor))
        sensor_list.append(d)
    return json.dumps(sensor_list)


create_db()
app.run(host='localhost', port=5000, debug=True)
