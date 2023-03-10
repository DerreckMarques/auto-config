DROP TABLE IF EXISTS hosts;
CREATE TABLE hosts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL,
    ip TEXT NOT NULL
);


DROP TABLE IF EXISTS scripts;
CREATE TABLE scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);