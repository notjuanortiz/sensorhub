DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    measurement FLOAT NOT NULL,
    location TEXT NOT NULL
);

INSERT INTO sensors(measurement, location) values (100.0, 'plant-01');
INSERT INTO sensors(measurement, location) values (110.0, 'plant-01');
INSERT INTO sensors(measurement, location) values (100.0, 'plant-01');
INSERT INTO sensors(measurement, location) values (250.0, 'plant-01');
INSERT INTO sensors(measurement, location) values (210.0, 'plant-02');
INSERT INTO sensors(measurement, location) values (230.0, 'plant-02');