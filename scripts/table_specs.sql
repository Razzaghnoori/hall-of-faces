CREATE DATABASE IF NOT EXISTS faceland;
use faceland
CREATE TABLE IF NOT EXISTS people (
	id varchar(36) NOT NULL UNIQUE,
	category varchar(50),
	name varchar(100),
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS images (
	id varchar(36) NOT NULL,
	pathphoto varchar(500),
	encoding varchar(300),
	PRIMARY KEY (id, pathphoto),	
	FOREIGN KEY (id) REFERENCES people(id)
);