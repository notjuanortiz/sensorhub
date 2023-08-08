import datetime
from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2
from psycopg2 import pool


@dataclass
class Sensor:
    name: str = None
    measurement: int = 0
    taken_on: datetime.datetime = None
    '''
    Time the measurement was taken.
    '''


class SensorService:
    def __init__(self):
        self.pool = psycopg2.pool.ThreadedConnectionPool(1, 3,
                                                         database='postgres',
                                                         user='postgres',
                                                         password='postgres',
                                                         host='sensorhub-postgresql.c5jrbbbr7rhi.us-east-2.rds'
                                                              '.amazonaws.com',
                                                         port='5432'
                                                         )
        pass

    @contextmanager
    def get_connection(self):
        con = self.pool.getconn()
        try:
            yield con
        finally:
            self.pool.putconn(con)

    def save(self, sensor: Sensor):
        with self.get_connection() as conn:
            cursor = conn.cursor()

            create_sensor_if_not_found_query = """
                INSERT INTO 
                    sensors (sensor_name)
                SELECT
                CASE
                    WHEN EXISTS (SELECT 1 FROM sensors WHERE sensor_name = %(name)s) THEN %(name)s
                    ELSE %(name)s
                END
                WHERE NOT EXISTS (SELECT 1 FROM sensors WHERE sensor_name = %(name)s);
            """
            cursor.execute(create_sensor_if_not_found_query, {'name': sensor.name})
            conn.commit()

            insert_sensor_data_query = """
            INSERT INTO
                sensor_data(sensor_id, measurement)
            SELECT
                sensor_id, %s
            FROM
                sensors
            WHERE
                sensor_name = %s
            """
            cursor.execute(insert_sensor_data_query, [sensor.measurement, sensor.name])
            conn.commit()
            cursor.close()
