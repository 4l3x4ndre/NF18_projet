| Information                   | Valeur                               |
| --                            | --                                   |
| Version du document           | 1.0.0                                |
| Dernière modification         | 2024-06-12                           |
| Auteurs | AMRANI Alexandre, DELBECQUE Lucas, DELMAERE Mathis, LAMY Léo |

---


On s'intéresse à la Normalisation fonctionnelle de {idVol, nomCompagnieVol, pilote1Vol, pilote2Vol, destinationVol, heureDepartVol, heureEmbarquementVol, hoteAccueil1Vol, hoteAccueil2Vol, provenanceVol, heureArriveeVol, typeVol, idAvion, modelAvion, nombreBagage, poidsBagage, idPassager, numeroTelPassager, numPorte, nomTerminal, longitudeTerminal, latitudeTerminal}

# Dépendances fonctionnelles

Les dépendances fonctionnelles que nous pouvons extraire de cet ensemble sont : {idVol → nomCompagnieVol, idVol → pilote1Vol, idVol → pilote2Vol, idVol → destinationVol, idVol → heureDepartVol, idVol → heureEmbarquementVol, idVol → hoteAccueil1Vol, idVol → hoteAccueil2Vol, idVol → provenanceVol, idVol → heureArriveeVol, idVol → typeVol, idVol → idAvion, idAvion → modelAvion, idPassager → numeroTelPassager, (idVol, idPassager) → nombreBagage, (idVol, idPassager) → poidsBagage, idVol → numPorte, idVol → nomTerminal, nomTerminal → longitudeTerminal, nomTerminal → latitudeTerminal}

# Fermeture Transitive

La fermeture transitive F+ est {idVol → nomCompagnieVol, idVol → pilote1Vol, idVol → pilote2Vol, idVol → destinationVol, idVol → heureDepartVol, idVol → heureEmbarquementVol, idVol → hoteAccueil1Vol, idVol → hoteAccueil2Vol, idVol → provenanceVol, idVol → heureArriveeVol, idVol → typeVol, idVol → idAvion, idAvion → modelAvion, idVol → modelAvion, idPassager → numeroTelPassager, (idVol, idPassager) → nombreBagage, (idVol, idPassager) → poidsBagage, idVol → numPorte, idVol → nomTerminal, nomTerminal → longitudeTerminal, idVol → longitudeTerminal, nomTerminal → latitudeTerminal, idVol → latitudeTerminal}

# Couverture minimale

La CM de ces DF est celle trouvée en premier lieu : {idVol → nomCompagnieVol, idVol → pilote1Vol, idVol → pilote2Vol, idVol → destinationVol, idVol → heureDepartVol, idVol → heureEmbarquementVol, idVol → hoteAccueil1Vol, idVol → hoteAccueil2Vol, idVol → provenanceVol, idVol → heureArriveeVol, idVol → typeVol, idVol → idAvion, idAvion → modelAvion, idPassager → numeroTelPassager, (idVol, idPassager) → nombreBagage, (idVol, idPassager) → poidsBagage, idVol → numPorte, idVol → nomTerminal, nomTerminal → longitudeTerminal, nomTerminal → latitudeTerminal}

En effet, toutes les DF sont de toute évidence élémentaire sauf 2 : (idVol, idPassager) → nombreBagage, (idVol, idPassager) → poidsBagage

Or si l'on retire l'un des deux éléments à gauche de la DF, on ne retrouve plus la partie droite (un idVol ne détermine pas à lui seul ne poids des bagages d'un passager).

Les DF sont donc toutes élémentaires.

# Clé

La clé que nous pouvons extraire est : (idVol, idPassager) car ces deux attributs permettent de retrouver tous les autres à partir des DF. Elles sont également minimales car aucun attribut ne les définis (ils doivent donc à tout prix être dans la clé)

# Relations

On se retrouve alors avec la relation R : (#idVol, #idPassager, numeroTelPassager, nomCompagnieVol, pilote1Vol, pilote2Vol, destinationVol, heureDepartVol, heureEmbarquementVol, hoteAccueil1Vol, hoteAccueil2Vol, provenanceVol, heureArriveeVol, typeVol, idAvion, modelAvion, nombreBagage, poidsBagage, numPorte, nomTerminal, longitudeTerminal, latitudeTerminal)

Cette relation est 1 NF car tous les attributs sont supposés atomiques et que notre relation possède une clé

Cette relation n'est cependant pas 2NF car une partie de la clé détermine des attributs non clé.

On découpe alors la relation en : 
- R1 : (#idVol, #idPassager, nombreBagage, poidsBagage)
- R2 : (#idVol, nomCompagnieVol, pilote1Vol, pilote2Vol, destinationVol, heureDepartVol, heureEmbarquementVol, hoteAccueil1Vol, hoteAccueil2Vol, provenanceVol, heureArriveeVol, typeVol, idAvion, modelAvion, nomTerminal, numPorte, longitudeTerminal, latitudeTerminal)
- R3 : (#idPassager, numeroTelPassager)

Ces relations ne sont pas non plus 3NF car des attributs non-clés déterminent des attributs non-clés.

On découpé alors les relations en :
- R1 : (#idVol, #idPassager, nombreBagage, poidsBagage)
- R2 : (#idVol, nomCompagnieVol, pilote1Vol, pilote2Vol, destinationVol, heureDepartVol, heureEmbarquementVol, hoteAccueil1Vol, hoteAccueil2Vol, provenanceVol, heureArriveeVol, typeVol, idAvion => R4.idAvion, nomTerminal => R5.nomTerminal, numPorte)
- R3 : (#idPassager, numeroTelPassager)
- R4 : (#idAvion, modelAvion)
- R5 : (#nomTerminal, longitudeTerminal, latitudeTerminal)
- R6 : (#idVol, #idPassager)
- R7 : (#idmodel, nom, nombrePlaces, vitesseMax, type, pousseemax, vitMaxRot, compagnieFabrique)

On retrouve alors les relations présentes dans notre MLD, excepté : la relation "Porte (#terminal ⇒ Terminal.nom, #num : int)"
