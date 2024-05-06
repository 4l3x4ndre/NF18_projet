SELECT SUM(poidsBagage) AS poids_total
FROM Bagage B JOIN Vol V ON B.vol = V.id
WHERE V.provenance = "Istanbul" OR V.destination = "Istanbul"
