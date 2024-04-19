| Information                   | Valeur                               |
| --                            | --                                   |
| Version du document           | 1.0.0                                |
| Dernière modification         | 2024-04-19                           |
| Auteurs | AMRANI Alexandre, DELBECQUE Lucas, DELMAERE Mathis, LAMY Léo |

---

# Note de Clarification 

- **UML : Tous les attributs sont NOT NULL par défaut ; héritage exclusif.**

- Le nom d'un terminal est unique et permet de l'identifier
- Un terminal a un couple de position (latitude, longitude) unique et qui permet de l'identifier
- Un terminal a au moins une porte
- Un terminal est entretenu par au moins un membre du personnel technique

- Une porte possède un numéro qui permet de l'identifier dans son terminal : le couple (nom de terminal, numéro de porte) permet d'identifier chaque porte de façon unique
- Certaines portes peuvent ne pas être utilisées par les avionts

- Le nom d'un modèle d'avion est unique et permet de l'identifier
- Un modèle d'avion est frabriquée par une seule compagnie de fabrication
- La vitesse d'un avion se mesure avec une réel positif
- Les vitesses maximales de rotation et de propulsion sont exprimées avec des décimaux
- Un modèle d'avion a au moins une porte à utiliser

- On suppose l'identifiant d'un avion unique et permet de l'identifier
- L'identifiant d'un avion est une chaine de caractères
- Tous les avions ont déjà volé au moins une fois

- Le nom des compagnies de fabrication d'avion est unique et permet de les identifier

- Le nom des compagnies de vol d'avion est unique et permet de les identifier
- Les compagnies de vol n'ont pas forcément un vol

- L'identifiant d'un vol est une chaîne de caractères 
- Un vol utilise un avion
- Un vol est rattaché à une seule compagnie
- Une heure de départ et d'arrivée d'un vol prend aussi en compte la date
- Un vol est conservé dans la base de données, même si sa compagnie de vol disparaît 
- Un vol utilise une et une seule porte
- Un vol n'a pas nécessairement de passagers

- La destination des vols d'arrivée est une chaîne de caractères

- Les informations personnelles (nom, prénom, date de naissance...) des passagers et des employés ne permettent pas de les identifier de façon unique
- Un passager a au moins un vol

- Un passager n'a pas forcément de bagages
- On exprime le poids des bagages avec des décimaux

- Les pilotes, stewarts et hôtes d'accueil peuvent ne pas encore avoir de vol (s'ils viennent d'être embauchés)

- Seuls les membres du personnels techniques sont rattachés à un terminal donné


