CREATE TABLE Personne (
    id_personne INT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    prenom VARCHAR(255) NOT NULL,
    dateNaiss DATE CHECK (dateNaiss < CURRENT_DATE),
    rue VARCHAR(255) NOT NULL,
    codepostal INT CHECK (codepostal > 0),
    ville VARCHAR(255) NOT NULL,
    pays VARCHAR(255) NOT NULL
);

CREATE TABLE Passager (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Pilote (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Technique (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    terminal VARCHAR(50) NOT NULL REFERENCES Terminal(nom),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Stewart (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE HoteAccueil (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Terminal (
    nom VARCHAR(50) PRIMARY KEY,
    longitude FLOAT CHECK (longitude BETWEEN -180 AND 180),
    latitude FLOAT CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT unique_long_lat UNIQUE (longitude, latitude)
);

CREATE TABLE Porte (
    terminal VARCHAR(50) REFERENCES Terminal(nom),
    num INT CHECK (num > 0),
    PRIMARY KEY (terminal, num)
);
