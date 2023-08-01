DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
  	time timestamp default now(),
  	name TEXT NOT NULL,
    measurement REAL NOT NULL
);

--INSERT INTO sensors(name, measurement) VALUES ('sensor-a', 230.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-a', 200.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-a', 245.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-a', 100.5);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-b', 230.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-b', 200.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-b', 245.0);
--INSERT INTO sensors(name, measurement) VALUES ('sensor-b', 100.5);