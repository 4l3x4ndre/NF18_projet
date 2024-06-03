DROP TABLE IF EXISTS VolNR;
DROP TYPE IF EXISTS TypeVolNR;

CREATE TYPE TypeVolNR AS ENUM ('VolArrivee', 'VolDepart');
CREATE TABLE VolNR (
    	id VARCHAR(10),
	compagnieVol VARCHAR(50),
	porte_num INT NOT NULL,
	porte_term VARCHAR(50) NOT NULL,
	destination VARCHAR(100),
	heureDepart TIMESTAMP,
	heureEmbarquement TIMESTAMP,
	provenance VARCHAR(100),
	heureArrivee TIMESTAMP,
	type TypeVolNR NOT NULL,
	bagage JSON NOT NULL,
	passager JSON,
	avion JSON NOT NULL,
	PRIMARY KEY(id),
	CHECK ( ((destination IS NOT NULL AND heureDepart IS NOT NULL AND heureEmbarquement IS NOT NULL AND heureEmbarquement < heureDepart AND type='VolDepart' ) AND (heureArrivee IS NULL AND provenance IS NULL)) OR ((heureArrivee IS NOT NULL AND provenance IS NOT NULL) AND (destination IS NULL AND heureDepart IS NULL AND heureEmbarquement IS NULL AND type='VolArrivee')) ) 
);

-- Exemple d'insertion dans la table flights
INSERT INTO VolNR VALUES
	
('VOL001', 'Air France', 1, 'Terminal 1',  'New York', '2024-06-10 08:00:00', '2024-06-10 07:00:00', NULL, NULL, 'VolDepart', 
	'[{"passager_id":1, "nombreBagage":2, "poidsBagage":30.5}, {"passager_id":2, "nombreBagage":2, "poidsBagage":40.5}, {"passager_id":3, "nombreBagage":4, "poidsBagage":35}, {"passager_id":4, "nombreBagage":0, "poidsBagage":0}]', 
	'[{"passager_id":1, "nom":"Dupont", "prenom":"Jean", "dateNaiss":"1990-05-15", "rue":"123 Rue de la liberté", "codepostal":75001, "ville":"Paris", "pays":"France", "numeroTel":"0683058729"}, {"passager_id":2, "nom":"Andre", "prenom":"Jeanne", "dateNaiss":"1980-05-15", "rue":"124 Rue de la prison", "codepostal":75001, "ville":"Paris", "pays":"France", "numeroTel":"0692658294"}, {"passager_id":3, "nom":"Dupuit", "prenom":"Jean-Charles", "dateNaiss":"1950-05-15", "rue":"125 Rue de la paix", "codepostal":75002, "ville":"Paris", "pays":"France", "numeroTel":"0690572927"}, {"passager_id":4, "nom":"Dondon", "prenom":"Jean-Pierre", "dateNaiss":"1960-05-15", "rue":"126 Rue de la guerre", "codepostal":60002, "ville":"Compiègne", "pays":"France", "numeroTel":"0726492749"}]', 
	'{"avion_id":"ABC123","model":"A307", "compagnieFabrication":"Airbus", "nombrePlaces":400, "vitesseMax":1200.0, "type":"TurboReacteur", "pousseeMax":850.0}'),

('VOL002', 'Air France', 3, 'Terminal 1',  'Paris', '2024-05-10 08:00:00', '2024-05-10 07:00:00', NULL, NULL, 'VolDepart', 
	'[{"passager_id":1, "nombreBagage":2, "poidsBagage":30.5}, {"passager_id":2, "nombreBagage":4, "poidsBagage":60.5}]', 
	'[{"passager_id":1, "nom":"Dupont", "prenom":"Jean", "dateNaiss":"1990-05-15", "rue":"123 Rue de la liberté", "codepostal":75001, "ville":"Paris", "pays":"France", "numeroTel":"0683058729"}, {"passager_id":2, "nom":"Andre", "prenom":"Jeanne", "dateNaiss":"1980-05-15", "rue":"124 Rue de la prison", "codepostal":75001, "ville":"Paris", "pays":"France", "numeroTel":"0692658294"}]', 
	'{"avion_id":"DEF456","model":"B737", "compagnieFabrication":"Boeing", "nombrePlaces":450, "vitesseMax":1200.0, "type":"TurboPropulseur", "vitMaxRot":1040.0}'),

('VOL003', 'British Airways', 2, 'Terminal 2',  NULL, NULL, NULL, 'Istanbul', '2084-05-10 08:00:00', 'VolArrivee', 
	'[{"passager_id":3, "nombreBagage":4, "poidsBagage":35}, {"passager_id":4, "nombreBagage":0, "poidsBagage":0}]', 
	'[{"passager_id":3, "nom":"Dupuit", "prenom":"Jean-Charles", "dateNaiss":"1950-05-15", "rue":"125 Rue de la paix", "codepostal":75002, "ville":"Paris", "pays":"France", "numeroTel":"0690572927"}, {"passager_id":4, "nom":"Dondon", "prenom":"Jean-Pierre", "dateNaiss":"1960-05-15", "rue":"126 Rue de la guerre", "codepostal":60002, "ville":"Compiègne", "pays":"France", "numeroTel":"0726492749"}]', 
	'{"avion_id":"GHI789","model":"A307", "compagnieFabrication":"Airbus", "nombrePlaces":400, "vitesseMax":1200.0, "type":"TurboReacteur", "pousseeMax":850.0}');

