DROP TABLE IF EXISTS client;
DROP TABLE IF EXISTS gig;
DROP TABLE IF EXISTS worker;

CREATE TABLE client (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT  NOT NULL,
  oauth TEXT NOT NULL,
  balance REAL NOT NULL
);


CREATE TABLE gig (
  gid TEXT PRIMARY KEY,
  cid INTEGER NOT NULL,
  wid INTEGER,
  submitted_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  timeout_ts TIMESTAMP NOT NULL,
  accepted_ts TIMESTAMP NULL,
  completed_ts TIMESTAMP NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  location TEXT NOT NULL,
  price REAL NOT NULL,
  FOREIGN KEY (cid) REFERENCES client (id),
  FOREIGN KEY (wid) REFERENCES worker (id)
);

CREATE TABLE worker (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  balance REAL NOT NULL
);

INSERT INTO client VALUES 
(0, 'Bird', '823jidfs9023rj', 50.34),
(1, 'Pizza Hut', '132434sdfi', 20.15),
(2, 'ACME Corp', '8392idfdsf90', 0.00),
(3, 'Apple', '2390uisfdsd90', 0.00);

INSERT INTO worker VALUES
(0, 'Burak Icel', 0.00),
(1, 'Eilon Lavi', 1.00),
(2, 'Aryan G', 3.14);