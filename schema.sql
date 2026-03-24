CREATE TABLE cursos_prov_a (
  id INT NOT NULL AUTO_INCREMENT,
  curso VARCHAR(255) NOT NULL,
  url TEXT NOT NULL,
  informacion TEXT,
  estado_url VARCHAR(50),
  PRIMARY KEY (id),
  UNIQUE KEY unique_url (url(255))
);

CREATE TABLE cursos_prov_b (
  id INT NOT NULL AUTO_INCREMENT,
  curso VARCHAR(255) NOT NULL,
  url TEXT NOT NULL,
  informacion TEXT,
  estado_url VARCHAR(50),
  PRIMARY KEY (id),
  UNIQUE KEY unique_url (url(255))
);

CREATE TABLE cursos_prov_c (
  id INT NOT NULL AUTO_INCREMENT,
  curso VARCHAR(255) NOT NULL,
  url TEXT NOT NULL,
  informacion TEXT,
  estado_url VARCHAR(50),
  PRIMARY KEY (id),
  UNIQUE KEY unique_url (url(255))
);