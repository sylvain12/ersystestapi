DROP TABLE IF EXISTS clients_providers;
DROP TABLE IF EXISTS clients;
DROP TABLE IF EXISTS providers;

CREATE TABLE clients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL UNIQUE,
  phone TEXT NOT NULL
);

CREATE TABLE providers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name NOT NULL
);

CREATE TABLE clients_providers (
  client_id INTEGER NOT NULL,
  provider_id INTEGER NOT NULL,
  FOREIGN KEY (client_id) REFERENCES clients (id),
  FOREIGN KEY (provider_id) REFERENCES providers (id)
)