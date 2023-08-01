import json

import psycopg2
from flask import Flask, redirect
from flask_restful import Api

application = Flask(__name__)
api = Api(application)


def connect_to_db():
    connection = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds.amazonaws.com",
        port='5432'
    )
    return connection


@application.route("/")
def index():
    return redirect("/sensors/")


@application.route("/sensors/", methods=['GET'])
def get_sensors():
    with connect_to_db() as connection:
        query = "SELECT time, name, measurement FROM sensors"
        cursor = connection.cursor()
        cursor.execute(query)
        sensors = cursor.fetchall()
    return json.dumps(sensors, indent=4, default=str), 200


@application.route("/sensors/<sensor_name>/", methods=['GET'])
def get_sensor(sensor_name: str):
    with connect_to_db() as connection:
        cursor = connection.cursor()
        query = "SELECT time, name, measurement FROM sensors WHERE id = %s"
        cursor.execute(query, sensor_name)
        sensor = cursor.fetchone()
        return json.dumps(sensor, indent=4, default=str), 200


if __name__ == "__main__":
    application.run(host='0.0.0.0', port='5000')
