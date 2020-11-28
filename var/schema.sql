DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS admins;

CREATE TABLE questions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	question TEXT NOT NULL,
	answer TEXT NOT NULL,
	week TEXT NOT NULL
);


CREATE TABLE admins (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT NOT NULL,
	second_name TEXT NOT NULL,
	email TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL
);
