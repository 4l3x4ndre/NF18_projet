CREATE TABLE Personne (
    id_personne INT PRIMARY KEY,
    nom VARCHAR(30) NOT NULL,
    prenom VARCHAR(30) NOT NULL,
    dateNaiss DATE CHECK (dateNaiss < CURRENT_DATE),
    rue VARCHAR(255) NOT NULL,
    codepostal INT CHECK (codepostal > 0),
    ville VARCHAR(50) NOT NULL,
    pays VARCHAR(50) NOT NULL
);

CREATE TABLE Passager (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Pilote (
    id_personne INT PRIMARY KEY REFERENCES Personne(id_personne),
    numeroTel VARCHAR(12) CHECK (LENGTH(numeroTel) BETWEEN 10 AND 12)
);

CREATE TABLE Terminal (
    nom VARCHAR(50) PRIMARY KEY,
    longitude FLOAT CHECK (longitude BETWEEN -180 AND 180),
    latitude FLOAT CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT unique_long_lat UNIQUE (longitude, latitude)
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



CREATE TABLE Porte (
    terminal VARCHAR(50) REFERENCES Terminal(nom),
    num INT CHECK (num > 0),
    PRIMARY KEY (terminal, num)
);


CREATE TABLE CompagnieFabrique (
	nom VARCHAR(50) PRIMARY KEY
);

CREATE TABLE CompagnieVol (
	nom VARCHAR(50) PRIMARY KEY
);

CREATE TYPE TypeAvion AS ENUM ('Turbopropulseur', 'Turboreacteur');
CREATE TABLE Model (
	nom VARCHAR(20),
	nombrePlaces INT,
	vitesseMax FLOAT NOT NULL,
	type TypeAvion NOT NULL,
	vitMaxRot FLOAT,
	pousseeMax FLOAT,
	compagnieFabrication VARCHAR(255) NOT NULL,
	FOREIGN KEY (compagnieFabrication) REFERENCES CompagnieFabrique(nom),
	CHECK (nombrePlaces >= 0),
	CHECK ((type = 'Turbopropulseur' AND vitMaxRot IS NOT NULL AND vitMaxRot > 0) OR (type = 'Turboreacteur' AND pousseeMax IS NOT NULL AND pousseeMax > 0)),
	PRIMARY KEY (nom)
);

CREATE TABLE Avion (
	id VARCHAR(10),
	model VARCHAR(20),
	FOREIGN KEY (model) REFERENCES Model(nom),
	PRIMARY KEY (id)
);

CREATE TYPE TypeVol AS ENUM ('VolArrivee', 'VolDepart');
CREATE TABLE Vol (
	id VARCHAR(10),
	avion VARCHAR(10) NOT NULL,
	compagnie VARCHAR(50) NOT NULL,
	pilote1 INT NOT NULL,
	pilote2 INT NOT NULL,
	porte_num INT NOT NULL,
	porte_term VARCHAR(50) NOT NULL,
	destination VARCHAR(100),
	heureDepart TIMESTAMP,
	heureEmbarquement TIMESTAMP,
	hote1 INT,
	hote2 INT,
	provenance VARCHAR(100),
	heureArrivee TIMESTAMP,
	type TypeVol NOT NULL,
	FOREIGN KEY (avion) REFERENCES Avion(id),
	FOREIGN KEY (compagnie) REFERENCES CompagnieVol(nom),
	FOREIGN KEY (pilote1) REFERENCES Pilote(id_personne),
	FOREIGN KEY (pilote2) REFERENCES Pilote(id_personne),
	FOREIGN KEY (porte_term,porte_num) REFERENCES Porte(terminal,num),
	FOREIGN KEY (hote1) REFERENCES HoteAccueil(id_personne),
	FOREIGN KEY (hote2) REFERENCES HoteAccueil(id_personne),
	CHECK ( ((destination IS NOT NULL AND heureDepart IS NOT NULL AND heureEmbarquement IS NOT NULL AND hote1 IS NOT NULL AND hote2 IS NOT NULL AND heureEmbarquement < heureDepart AND type='VolDepart' AND hote1 <> hote2) AND (heureArrivee IS NULL AND provenance IS NULL)) OR ((heureArrivee IS NOT NULL AND provenance IS NOT NULL) AND (destination IS NULL AND heureDepart IS NULL AND heureEmbarquement IS NULL AND hote1 IS NULL AND hote2 IS NULL AND type='VolArrivee')) ) ,
	CHECK (pilote1 != pilote2),
	PRIMARY KEY (id)
);

CREATE TABLE Bagage (
	vol VARCHAR(10) NOT NULL,
	passager INT NOT NULL,
	nombreBagage INT NOT NULL,
	poidsBagage FLOAT NOT NULL,
	FOREIGN KEY (vol) REFERENCES Vol(id),
	FOREIGN KEY (passager) REFERENCES Passager(id_personne),
	PRIMARY KEY (vol, passager),
	CHECK (nombreBagage >= 0 AND poidsBagage >= 0)
);

CREATE TABLE STEWARTTRAVAIL (
	stewart INT NOT NULL,
	vol VARCHAR(10) NOT NULL,
	FOREIGN KEY (stewart) REFERENCES Stewart(id_personne),
	FOREIGN KEY (vol) REFERENCES Vol(id),
	PRIMARY KEY (stewart, vol)
);

CREATE TABLE PeutAccueillir (
	porte_num INT NOT NULL,
	porte_term VARCHAR(50) NOT NULL,
	model VARCHAR(20) NOT NULL,
	FOREIGN KEY (porte_num, porte_term) REFERENCES Porte(num, terminal),
	FOREIGN KEY (model) REFERENCES Model(nom),
	PRIMARY KEY (porte_num, porte_term, model)
);
