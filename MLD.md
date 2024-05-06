| Information                   | Valeur                               |
| --                            | --                                   |
| Version du document           | 1.0.0                                |
| Dernière modification         | 2024-04-24                           |
| Auteurs | AMRANI Alexandre, DELBECQUE Lucas, DELMAERE Mathis, LAMY Léo |

# Justification de l’héritage

- **Model** : héritage par mère, car relations sur la mère et pas sur les filles, et héritage quasi-complet
- **Personne** : héritage par référence car héritage non exclusif 
- **Personnel** : héritage par fille car aucune relation avec la mère
- **Vol** : héritage par mère car pas de relations sur les filles, sauf une mais n’est pas une relation \* à \* . Donc on aura soit 5 attributs nuls soit 2.
- **Compagnie** : héritage par les filles car aucune relation sur la mère.

# Relations

Personne(#id_personne : int, nom : str, prenom : str, dateNaiss : date, rue : str, codepostal : int, ville : str, pays : str) avec (date < current date et codepostal > 0)

Passager (#id => Personne.id_personne, numeroTel : int) avec { 10 <= length(numeroTel) <= 12, NULLABLE }

Pilote(#id => Personne.id_personne, numeroTel : int) avec { 10 <= length(numeroTel) <= 12 }

Technique(#id => Personne.id_personne, terminal => Terminal.nom,  numeroTel : int) avec { 10 <= length(numeroTel) <= 12 }

Stewart(#id => Personne.id_personne, numeroTel : int)  avec {10 <= length(numeroTel) <= 12 }

HoteAccueil(#id => Personne.id_personne, numeroTel : int)  avec { 10 <= length(numeroTel) <= 12 }

Terminal(#nom : String, longitude : float, latitude : float) avec { (longitude, latitude) unique AND -90<latitude<90 AND -180<longitude<180 }

Porte (#terminal ⇒ Terminal.nom, #num : int) avec (num > 0)

CompagnieFabrique (#nom : String)

CompagnieVol (#nom : String)

Model (#nom : String, nombrePlaces : int, vitesseMax : float, type:enum{Turbopropulseur, Turboreacteur} vitMaxRot : float, pousseeMax : float, compagnieFabrication ⇒ CompagnieFabrique) avec { nombrePlace >= 0 AND ( (type = Turbopropulseur AND vitMaxRot NOT NULL AND vitMaxRot > 0 ) OR (type =Turboreacteur AND pousseeMax NOT NULL AND pousseeMax > 0) ) }

Avion (#id : str, model => Model.nom)

Vol (#id : str, avion => Avion.id, compagnie => CompagnieVol.nom, pilote1 => Pilote.id_personne, pilote2 => Pilote.id_personne, porte_num => Porte.num, porte_term => Porte.term, destination : str, heureDepart : datetime, heureEmnarquement : datetime, hote1 => HoteAccueil.id_personne, hote2 => HoteAccueil.id_personne, provenance : str, heureArrivee : datetime, type : {VolArrivee / VolDepart }) avec {id composé de chiffres et lettres, (destination AND  heureDepart AND heureEmbarquement AND hote1 AND hote2 nulls si type = volArrivee) AND(heureArrivee AND provenance nulls si type = volDepart) AND (destination AND  heureDepart AND heureEmbarquement AND hote1 AND hote2 not nulls si type = volDepart) AND (heureArrivee AND provenance not nulls si type=VolArrivee), heureEmbarquement < heureDepart, pilote1 ≠ pilote2, hote1 ≠ hote2 si type = volDepart}

Bagage(#vol => Vol.id, #passager => Passager.id_personne, nombreBagage : int, poidsBagage : float)

StewartTravail (#stewart ⇒ Stewart.id_personne, #vol ⇒ Vol.id)

PeutAccueillir (#porte_num ⇒ Porte.num, #porte_term ⇒ Porte.terminal, #model ⇒ Model.nom)


# Contraintes

- Intersection(CompagnieFabrique, CompagnieVol) = {}
- Les intersections dans les tables Stewart, Pilote, Technique, HoteAccueil prisent deux à deux sont toutes égales à l’ensemble vide.
- Il y a au moins deux Stewart par vol.
- Une porte accueille au moins un modèle et un modèle peut au moins être accueilli par une porte.
	- Projection(PeutAccueillir, porte_num, porte_term) = Projection(Porte, num, terminal)
	- Projection(PeutAccueillir, model) = Projection(Model, nom)
- Il y a au moins un technicien par terminal.
	- Projection(Technique, terminal) = Projection(Terminal, nom)
- Le nombre de passagers est inférieur ou égal au nombre de places du modèle de l'avion associé au vol
- Le vol et la porte associée doivent avoir le même modèle d'avion
- Un avion a au moins un vol.
	- Projection(Avion, id) = Projection(Vol, avion)


SQL : // On pourrait utiliser un trigger permettant de respecter la contrainte : "Les intersections dans les tables Stewart, Pilote, Technique, HoteAccueil prisent deux à deux sont toutes égales à l’ensemble vide."




