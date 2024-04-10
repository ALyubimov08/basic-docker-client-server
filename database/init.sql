CREATE DATABASE lab;

\c lab;

CREATE TABLE accounting (
    id SERIAL    PRIMARY KEY,
    client_name  VARCHAR(100),
	items_bought INTEGER,
	balance      INTEGER
);
