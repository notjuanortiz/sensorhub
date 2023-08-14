DROP TABLE IF EXISTS sensor_data;
DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
    sensor_id serial primary key,
    sensor_name varchar(50) UNIQUE NOT NULL,
    manufacturer_id INTEGER DEFAULT 0

);

CREATE TABLE sensor_data(
    sensor_time TIMESTAMP DEFAULT now(),
    sensor_id INTEGER NOT NULL,
    measurement DOUBLE PRECISION NOT NULL,
    FOREIGN KEY (sensor_id) REFERENCES sensors(sensor_id) ON DELETE CASCADE
);

--INSERT INTO sensors(sensor_name, manufacturer_id) VALUES('sensor-a', 1);
--INSERT INTO sensors(sensor_name, manufacturer_id) VALUES('sensor-b', 1);

--INSERT INTO sensor_data(sensor_id, measurement) VALUES(1, 100.0);
--INSERT INTO sensor_data(sensor_id, measurement) VALUES(1, 75.0);
--INSERT INTO sensor_data(sensor_id, measurement) VALUES(1, 85.0);
--INSERT INTO sensor_data(sensor_id, measurement) VALUES(2, 50.5);
--INSERT INTO sensor_data(sensor_id, measurement) VALUES(2, 45.3);
--INSERT INTO sensor_data(sensor_id, measurement) VALUES(2, 52.5);

--CREATE TABLE manufacturers (
--    manufacturer_id  serial primary key,
--    name    varchar(100),
--    email   varchar()
--)