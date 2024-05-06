-- Quelle est le poids des bagages venant et partant pour Istanbul ?
-- Prendre le poids total de tous les bagages

SELECT SUM(poidsBagage) AS poids_total
FROM Bagage B JOIN Vol V ON B.vol = V.id
WHERE V.provenance = "Istanbul" OR V.destination = "Istanbul"

-- Quel est le nombre de steward de chaque avion de modèle A307

SELECT vol, COUNT(*) AS nb_stew
FROM STEWARTTRAVAIL
JOIN Avion ON Avion.id = STEWARTTRAVAIL.vol
JOIN Model ON Model.nom = Avion.model
WHERE Model.nom = 'A307'
GROUP BY vol;

-- Quelles sont les 10 compagnies qui ont eu le plus de passagers sur les vols en partance de l'aéroport ?


SELECT compagnie, COUNT(*) AS nb_pass
FROM Vol
WHERE type = 'VolDepart'
GROUP BY compagnie
ORDER BY nb_pass DESC
LIMIT 10;

