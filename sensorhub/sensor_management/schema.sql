DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
  	time timestamp,
  	name TEXT NOT NULL,
    measurement REAL NOT NULL
);

INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-a', 230.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-a', 200.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-a', 245.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-a', 100.5);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-b', 230.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-b', 200.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-b', 245.0);
INSERT INTO sensors(time, name, measurement) VALUES (current_timestamp, 'sensor-b', 100.5);