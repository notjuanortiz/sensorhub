from dataclasses import dataclass

from .storage_connectors import Connector


@dataclass
class Sensor:
    name: str = None
    measurement: int = 0
    taken_on: str = None
    '''
    Time the measurement was taken.
    '''


class SensorService:
    repository = None

    def __init__(self, repository: Connector):
        self.repository = repository
        pass

    def save(self, sensor: Sensor):
        sensor_id: int = 0
        try:
            cursor = self.repository.cursor()
            query = "INSERT INTO sensors(name, measurement) VALUES (%s, %s)"
            cursor.execute(query, (sensor.name, sensor.measurement))
            self.repository.commit()
            cursor.close()
            self.repository.close()
        except Exception as error:
            print(error)
        finally:
            if self.repository.db_connection is not None:
                self.repository.close()
        return sensor_id
