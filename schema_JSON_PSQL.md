| Information                   | Valeur                               |
| --                            | --                                   |
| Version du document           | 2.0.0                                |
| Dernière modification         | 2024-06-10                           |
| Auteurs | AMRANI Alexandre, DELBECQUE Lucas, DELMAERE Mathis, LAMY Léo |

---

**<mark style='background:#ffadad'>Tous les champs sont NOT NULL par défaut.</mark>** 


### Attribut JSON passager (Type : JSON)

Données attendues : Une liste d'objets représentant les passagers du vol. Chaque objet doit contenir :
- id_personne (Type : Entier) : Identifiant unique de la personne.
- nom (Type : Chaîne de caractères) : Nom de famille du passager.
- prenom (Type : Chaîne de caractères) : Prénom du passager.
- dateNaiss (Type : Date) : Date de naissance du passager au format AAAA-MM-JJ.
- rue (Type : Chaîne de caractères) : numéro et rue de l'adresse du passager.
- codepostal (Type : Chaîne de caractères) : Code postal de l'adresse du passager.
	- Le type est chaîne de caractères car en Javascript (donc JSON) le préfixe 0 défini le type octal
	- Il est donc attendu une chaîne représentant le code postal en entier, c'est-à-dire comprenant tous les zéros. Ce champ représente un entier positif.
- ville (Type : Chaîne de caractères) : Ville de résidence du passager.
- pays (Type : Chaîne de caractères) : Pays de résidence du passager.
- numeroTel (Type : Chaîne de caractères) : Numéro de téléphone du passager.
	- Le format est 10 chiffres ou 9 chiffres précédés d'un indicatif téléphonique ("+33")
- bagages (Type : JSON) : Objet représentant les bagages de ce passager. Chaque objet doit contenir :
	- passager_id (Type : Entier) : Identifiant unique du passager (référencent `id_personne` du champ JSON passager).
	- nombreBagage (Type : Entier) : Nombre de bagages enregistrés par le passager.
	- poidsBagage (Type : Flottant) : Poids total des bagages du passager en kilogrammes.

Contraintes :
- bagages.poidsBagage >= 0
- bagages.nombreBagage >=0
- bagages.nombreBagage > 0 $\Longleftrightarrow$  bagages.poidsBagage > 0

### Attribut JSON avion (Type : JSON)

Données attendues : Un objet représentant les informations sur l'avion. L'objet doit contenir :
- avion_id (Type : Chaîne de caractères) : Identifiant unique de l'avion.
- model (Type : JSON) : Objet contenant toutes les informations du modèles, à savoir
	- nom (Type : Chaîne de caractères) : Nom du modèle de l'avion.
	- compagnieFabrication (Type : Chaîne de caractères) : Compagnie ayant fabriqué l'avion.
	- nombrePlaces (Type : Entier) : Nombre de places disponibles dans l'avion.
		- Doit être supérieur ou égale à zéro.
	- vitesseMax (Type : Flottant) : Vitesse maximale de l'avion en km/h.
		- Doit être supérieur à zéro.
	- type (Type : Chaîne de caractères) : Type de moteur de l'avion 
		- choix obligatoire parmi : TurboRéacteur; TurboPropulseur.
	- pousseeMax (Type : Flottant, optionnel) : Poussée maximale des moteurs de l'avion (en kN).
		- Doit être supérieur à zéro.

Contraintes :
- Si le type est TurboRéacteur, alors la vitesseMax est renseignée et non pousseeMax
- Si le type est TurboPropulseur, alors la pousseeMax est renseignée et non vitesseMax

### Attribut JSON pilote1 et pilote2 (Type : JSON)

Données attendues : Un objet représentant les informations sur le premier pilote et le deuxième pilote. L'objet doit contenir :
- id_personne (Type : Entier) : Identifiant unique du pilote.
- numeroTel (Type : Chaîne de caractères) : Numéro de téléphone du pilote.
	- Le format est 10 chiffres ou 9 chiffres précédés d'un indicatif téléphonique ("+33")
- nom (Type : Chaîne de caractères) : Nom de famille du pilote.
- prenom (Type : Chaîne de caractères) : Prénom du pilote.
- dateNaiss (Type : Date) : Date de naissance du pilote au format AAAA-MM-JJ.
- rue (Type : Chaîne de caractères) : numéro et rue de l'adresse du pilote.
- codepostal (Type : Chaîne de caractères) : Code postal de l'adresse du pilote.
	- Le type est chaîne de caractères car en Javascript (donc JSON) le préfixe 0 défini le type octal
- ville (Type : Chaîne de caractères) : Ville de résidence du pilote.
- pays (Type : Chaîne de caractères) : Pays de résidence du pilote.

Contraintes : 
- Les champs pilote1 et pilote2 doivent être différents : ils indiquent les deux pilotes, différents, du vol.
