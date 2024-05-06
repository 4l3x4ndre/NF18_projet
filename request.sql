-- Quelle est le poids des bagages venant et partant pour Istanbul ?
-- Prendre le poids total de tous les bagages

SELECT SUM(poidsBagage) AS poids_total
FROM Bagage B JOIN Vol V ON B.vol = V.id
WHERE V.provenance = 'Istanbul' OR V.destination = 'Istanbul';

-- Requête s'il n'y a pas de vol de telle ville
SELECT SUM(poidsBagage) AS poids_total
FROM Bagage B JOIN Vol V ON B.vol = V.id
WHERE V.provenance = 'Istanbuleee' OR V.destination = 'Istanbuleee';

-- Quel est le nombre de steward de chaque avion de modèle A307

SELECT Avion.id, COUNT(DISTINCT STEWARTTRAVAIL.stewart) AS nb_stew
FROM STEWARTTRAVAIL
JOIN Vol on vol.id = STEWARTTRAVAIL.vol
RIGHT OUTER JOIN Avion ON Avion.id = vol.avion
JOIN Model ON Model.nom = Avion.model
WHERE Model.nom = 'A307'
GROUP BY Avion.id;

-- Quelles sont les 10 compagnies qui ont eu le plus de passagers sur les vols en partance de l'aéroport ?

SELECT vol.compagnie, COUNT(DISTINCT bagage.passager) AS nb_pass
FROM Vol LEFT OUTER JOIN BAGAGE ON Vol.id = BAGAGE.vol
WHERE Vol.type = 'VolDepart'
GROUP BY vol.compagnie
ORDER BY nb_pass DESC
LIMIT 3;
-- Nous avons entré 5 compagnies, nous mettons LIMIT 3 pour avoir les 3 avec le plus de passagers
