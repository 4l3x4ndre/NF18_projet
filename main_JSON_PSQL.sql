CREATE SCHEMA IF NOT EXISTS schema_json_psql;
SET search_path = schema_json_psql;

DROP TABLE IF EXISTS schema_json_psql.VolNR;
DROP TYPE IF EXISTS schema_json_psql.TypeVolNR;
DROP TABLE IF EXISTS schema_json_psql.Porte;
DROP TABLE IF EXISTS schema_json_psql.Terminal;


CREATE TABLE schema_json_psql.Terminal (
    nom VARCHAR(50) PRIMARY KEY,
    longitude FLOAT CHECK (longitude BETWEEN -180 AND 180),
    latitude FLOAT CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT unique_long_lat UNIQUE (longitude, latitude)
);

CREATE TABLE schema_json_psql.Porte (
    terminal VARCHAR(50) REFERENCES schema_json_psql.Terminal(nom),
    num INT CHECK (num > 0),
    PRIMARY KEY (terminal, num)
);

CREATE TYPE schema_json_psql.TypeVolNR AS ENUM ('VolArrivee', 'VolDepart');
CREATE TABLE schema_json_psql.VolNR (
    	id VARCHAR(10),
	compagnieVol VARCHAR(50),
	porte_num INT NOT NULL,
	porte_term VARCHAR(50) NOT NULL,
	destination VARCHAR(100),
	heureDepart TIMESTAMP,
	heureEmbarquement TIMESTAMP,
	provenance VARCHAR(100),
	heureArrivee TIMESTAMP,
	type schema_json_psql.TypeVolNR NOT NULL,
	passager JSON,
	avion JSON NOT NULL,
	pilote1 JSON NOT NULL,
	pilote2 JSON NOT NULL,
	FOREIGN KEY (porte_term,porte_num) REFERENCES schema_json_psql.Porte(terminal,num),
	CHECK ( ((destination IS NOT NULL AND heureDepart IS NOT NULL AND heureEmbarquement IS NOT NULL AND heureEmbarquement < heureDepart AND type='VolDepart' ) AND (heureArrivee IS NULL AND provenance IS NULL)) OR ((heureArrivee IS NOT NULL AND provenance IS NOT NULL) AND (destination IS NULL AND heureDepart IS NULL AND heureEmbarquement IS NULL AND type='VolArrivee')) ),
	PRIMARY KEY(id)
);

-- Insertion dans la table Terminal
INSERT INTO schema_json_psql.Terminal (nom, longitude, latitude)
VALUES
    ('Terminal 1', 48.8566, 2.3522),
    ('Terminal 2', 45.7640, 4.8357),
    ('Terminal 3', 43.2965, 5.3698),
    ('Terminal 4', 40.4168, -3.7038);

-- Insertion dans la table Porte
INSERT INTO schema_json_psql.Porte (terminal, num)
VALUES
    ('Terminal 1', 1),
    ('Terminal 1', 2),
    ('Terminal 1', 3),
    ('Terminal 2', 1),
    ('Terminal 2', 2),
    ('Terminal 3', 1),
    ('Terminal 4', 1),
    ('Terminal 4', 2);

-- Exemple d'insertion dans la table flights
INSERT INTO schema_json_psql.VolNR VALUES
	
('VOL001', 'Air France', 1, 'Terminal 1',  'New York', '2024-06-10 08:00:00', '2024-06-10 07:00:00', NULL, NULL, 'VolDepart', 
	'[{"id_personne":1, "nom":"Dupont", "prenom":"Jean", "dateNaiss":"1990-05-15", "rue":"123 Rue de la liberté", "codepostal":"75001", "ville":"Paris", "pays":"France", "numeroTel":"0683058729", "bagages":{"nombreBagage":2, "poidsBagage":30.5}}, {"id_personne":2, "nom":"Andre", "prenom":"Jeanne", "dateNaiss":"1980-05-15", "rue":"124 Rue de la prison", "codepostal":"75001", "ville":"Paris", "pays":"France", "numeroTel":"0692658294", "bagages":{"nombreBagage":2, "poidsBagage":40.5}}, {"id_personne":3, "nom":"Dupuit", "prenom":"Jean-Charles", "dateNaiss":"1950-05-15", "rue":"125 Rue de la paix", "codepostal":"75002", "ville":"Paris", "pays":"France", "numeroTel":"0690572927", "bagages":{"nombreBagage":4, "poidsBagage":35}}, {"id_personne":4, "nom":"Dondon", "prenom":"Jean-Pierre", "dateNaiss":"1960-05-15", "rue":"126 Rue de la guerre", "codepostal":"60002", "ville":"Compiègne", "pays":"France", "numeroTel":"0726492749", "bagages":{"nombreBagage":0, "poidsBagage":0}}, {("id_personne":45, "prenom":"Kim", "nom":"Min-ji", "dateNaiss":"1987-04-12", "rue":"456 Jongno-gu", "codepostale":"06000", "ville":"Séoul", "pays":"Corée du Sud", "numeroTel":"0692744275", "bagages":{"nombreBagage":10, "poidsBagage":250.45}}]', 
	'{"avion_id":"ABC123","model":{"nom":"A307", "compagnieFabrication":"Airbus", "nombrePlaces":400, "vitesseMax":1200.0, "type":"TurboReacteur", "pousseeMax":850.0}}', 
	'{"id_personne":6, "numeroTel":"0657283758", "nom":"Sully", "prenom":"Jake", "dateNaiss":"1970-05-20", "rue":"12 St. of Peace", "codepostal":"10100", "ville":"New-York", "pays":"Etats-Unis"}',
	'{"id_personne":7, "numeroTel":"0746289274", "nom":"Olang", "prenom":"Paul", "dateNaiss":"1975-12-20", "rue":"11B St. Baker Street", "codepostal":"12001", "ville":"Londres", "pays":"Angleterre"}'),

('VOL002', 'Air France', 3, 'Terminal 1',  'Paris', '2024-05-10 08:00:00', '2024-05-10 07:00:00', NULL, NULL, 'VolDepart', 
	'[{"id_personne":1, "nom":"Dupont", "prenom":"Jean", "dateNaiss":"1990-05-15", "rue":"123 Rue de la liberté", "codepostal":"75001", "ville":"Paris", "pays":"France", "numeroTel":"0683058729", "bagages":{"nombreBagage":2, "poidsBagage":30.5}}, {"id_personne":2, "nom":"Andre", "prenom":"Jeanne", "dateNaiss":"1980-05-15", "rue":"124 Rue de la prison", "codepostal":"75001", "ville":"Paris", "pays":"France", "numeroTel":"0692658294", "bagages":{"nombreBagage":4, "poidsBagage":60.5}}, {"id_personne":44, "nom":"Fernández", "prenom":"José", "dateNaiss":"1973-09-30", "rue":"123 Passeig de Gràcia", "codepostal":"08001", "ville":"Barcelone", "pays":"Espagne", "numeroTel":"0690741341", "bagages":{"nombreBagage":1, "poidsBagage":23.0}}, {"id_personne":43, "nom":"Nguyen", "prenom":"Linh", "dateNaiss":"1989-06-14", "rue":"789 Hoàng Sa", "codepostal":"70000", "ville":"Ho Chi Minh Ville", "pays":"Vietnam", "numeroTel":"0669590319", "bagages":{"nombreBagage":2, "poidsBagage":46.5}}, {"nom":42, "nom":"Meyer", "prenom":"Sophie", "dateNaiss":"1984-01-25", "rue":"101 Hauptstraße", "codepostal":"10178", "ville":"Berlin", "pays":"Allemagne", "numeroTel":"0620717810", "bagages":{nombreBagage:1, poidsBagage:15.7}}]', 
	'{"avion_id":"DEF456","model":{"nom":"B737", "compagnieFabrication":"Boeing", "nombrePlaces":450, "vitesseMax":1200.0, "type":"TurboPropulseur", "vitMaxRot":1040.0}}',
	'{"id_personne":8, "numeroTel":"0746289274", "nom":"Schneider", "prenom":"Anna", "dateNaiss":"1978-02-20", "rue":"101 Rue du Commerce", "codepostal":"75002", "ville":"Paris", "pays":"France"}',
	'{"id_personne":7, "numeroTel":"0746289274", "nom":"Olang", "prenom":"Paul", "dateNaiss":"1975-12-20", "rue":"11B St. Baker Street", "codepostal":"12001", "ville":"Londres", "pays":"Angleterre"}'),

('VOL003', 'British Airways', 2, 'Terminal 2',  NULL, NULL, NULL, 'Istanbul', '2084-05-10 08:00:00', 'VolArrivee', 
	'[{"id_personne":3, "nom":"Dupuit", "prenom":"Jean-Charles", "dateNaiss":"1950-05-15", "rue":"125 Rue de la paix", "codepostal":"75002", "ville":"Paris", "pays":"France", "numeroTel":"0690572927", "bagages":{"nombreBagage":4, "poidsBagage":35}}, {"id_personne":4, "nom":"Dondon", "prenom":"Jean-Pierre", "dateNaiss":"1960-05-15", "rue":"126 Rue de la guerre", "codepostal":"60002", "ville":"Compiègne", "pays":"France", "numeroTel":"0726492749", "bagages":{"nombreBagage":0, "poidsBagage":0}}, {"id_personne":41, "prenom":"Lee", "nom":"Ji-hyun", "dateNaiss":"1980-07-18", "rue":"456 Gangnam-daero", "codepostal":"06000", "ville":"Séoul", "pays":"Corée du Sud", "numeroTel":"0603212565", "bagages":{nombreBagage:3, "poidsBagage":60.1}}, {"id_personne":40, "nom":"Smith", "prenom":"Olivia", "dateNaiss":"1995-10-05", "rue":"123 Fifth Avenue", "codepostal":"10001", "ville":"New York", "pays":"États-Unis", "numeroTel":"0658392074", "bagages":{"nombreBagage":2, "poidsBagage":37.3}}]', 
	'{"avion_id":"GHI789","model":{"nom":"A307", "compagnieFabrication":"Airbus", "nombrePlaces":400, "vitesseMax":1200.0, "type":"TurboReacteur", "pousseeMax":850.0}}',
	'{"id_personne":6, "numeroTel":"0657283758", "nom":"Sully", "prenom":"Jake", "dateNaiss":"1970-05-20", "rue":"12 St. of Peace", "codepostal":"10100", "ville":"New-York", "pays":"Etats-Unis"}',
	'{"id_personne":7, "numeroTel":"0746289274", "nom":"Olang", "prenom":"Paul", "dateNaiss":"1975-12-20", "rue":"11B St. Baker Street", "codepostal":"12001", "ville":"Londres", "pays":"Angleterre"}'),

('VOL007', 'Lufthansa', 2, 'Terminal 4', NULL, NULL, NULL, 'Istanbul', '2024-05-11 19:00:00', 'VolArrivee',

	'[passagers]',

	'{"avion_id":"DEF456", "model":{"nom":"B737", "compagnieFrabrication":"Boeing", "nombrePlaces":160, "vitesseMax":850, "type":"TurboReacteur", "pousseeMax":110000}}',

	'{"id_personne":39, "numeroTel":"0654515875", "nom":"Martinez", "prenom":"Antonio", "dateNaiss":"1982-03-10", "rue":"789 Calle Mayor", "codepostal":"28004", "ville":"Madrid", "pays":"Espagne"}',

	'{"id_personne":38, "numeroTel":"0673405478", "nom":"Andersen", "prenom":"Ingrid", "dateNaiss":"1977-08-22", "rue":"456 Amagerbrogade", "codepostal":"1051", "ville":"Copenhague","pays":"Danemark"}'),

('VOL004', 'Delta Airlines', 1, 'Terminal 3', 'Rome', '2024-05-13 14:00:00', '2024-05-13 13:00:00', NULL, NULL, 'VolDepart',

	'[passagers]',

	'{"avion_id":"JKL012", "model":{"nom":"A307", "compagnieFrabrication":"Airbus", "nombrePlaces":180, "vitesseMax":900, "type":"TurboReacteur", "pousseeMax":120000}}',

	'{"id_personne":39, "numeroTel":"0654515875", "nom":"Martinez", "prenom":"Antonio", "dateNaiss":"1982-03-10", "rue":"789 Calle Mayor", "codepostal":"28004", "ville":"Madrid", "pays":"Espagne"}',
	
	'{"id_personne":7, "numeroTel":"0746289274", "nom":"Olang", "prenom":"Paul", "dateNaiss":"1975-12-20", "rue":"11B St. Baker Street", "codepostal":"12001", "ville":"Londres", "pays":"Angleterre"}');

