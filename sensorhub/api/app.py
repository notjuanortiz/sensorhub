import json

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect
from flask_cors import CORS, cross_origin
from psycopg2.extras import RealDictCursor

load_dotenv()
application = Flask(__name__)
CORS(application)


def connect_to_db():
    connection = psycopg2.connect(
        user="postgres",
        password="postgres",
        host="sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds.amazonaws.com",
        port=5432
    )
    return connection


@application.route("/")
@cross_origin(send_wildcard=True)
def index():
    return redirect("/sensors/")


@application.get("/sensors/")
@cross_origin(send_wildcard=True)
def get_sensor_list():
    with connect_to_db() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                    SELECT
                        S.sensor_id,
                        S.sensor_name,
                        S.manufacturer_id,
                        CASE WHEN max(SD.sensor_time) >= now() - interval '10 seconds' THEN TRUE ELSE FALSE END AS is_online
                    FROM
                        sensors AS S
                    JOIN
                        sensor_data AS SD ON S.sensor_id = SD.sensor_id
                    GROUP BY
                        S.sensor_id, S.sensor_name, S.manufacturer_id;
                    """
            cursor.execute(query)
            sensors = cursor.fetchall()
    return json.dumps(sensors, indent=4, separators=(",", ": ")), 200


@application.get("/sensors/<id>/")
def get_sensor(id):
    with connect_to_db() as c:
        with c.cursor(cursor_factory=RealDictCursor) as cursor:
            query = "SELECT sensor_id, measurement, sensor_time FROM sensor_data WHERE sensor_id = (%s)"
            cursor.execute(query, id)
            measurements = cursor.fetchall()
    return json.dumps(measurements, indent=4, separators=(",", ": "), default=str), 200


if __name__ == "__main__":
    application.run(host='0.0.0.0',
                    debug=True,
                    ssl_context='adhoc'
                    )
