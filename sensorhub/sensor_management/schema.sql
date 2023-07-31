DROP TABLE IF EXISTS sensors;

CREATE TABLE sensors (
    name TEXT PRIMARY KEY NOT NULL,
    taken_on TIMESTAMP NOT NULL,
    measurement FLOAT NOT NULL,
);
