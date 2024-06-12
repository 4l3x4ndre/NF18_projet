import datetime
import psycopg2
import json

# Configuration de la connexion à la base de données
USER = "nf18p013"
HOST = "tuxa.sme.utc"
PASSWORD = "hIcD85qXLDBu"
DATABASE = "dbnf18p013"


def init(cur):
    cur.execute(open("main_JSON_PSQL.sql", "r").read())

def voir_id_vols(conn, cursor):
    """
    Affiche la liste (vol id , compagnie vol) de la table VolNR
    """
    table_name = "VolNR"
    sql = "SELECT id, compagnieVol FROM " + table_name + " ; "
    cursor.execute("SELECT id, compagnieVol FROM " + table_name + " LIMIT 0; ")
    column = []
    for DESC in cursor.description:
        column.append(DESC[0])
    print(column)
    cursor.execute(sql)
    ligne = cursor.fetchone()
    while ligne :
        print(ligne)
        ligne = cursor.fetchone()


def voir_vol(conn,cursor):
    """
    Permet de voir le contenu d'un vol sélectionné par son id.
    """
    # Affichage de la liste des vols pour en choisir un.
    voir_id_vols(conn, cursor)

    id_vol = input("Quel vol souhaitez-vous voir ? (id) : ")
    sql = "SELECT * FROM VolNR WHERE id = %s"
    cursor.execute(sql, (id_vol,))
    ligne = cursor.fetchone()
    while ligne:
        print(ligne)
        ligne = cursor.fetchone()


def ajouter_passager(conn, cursor):
    """
    Permet d'ajouter un passager dans un vol.
    Les entrées concernant les utilisateurs sont supposées valides.

    Vérification du nombre de personnes déjà présentes dans le vol et comparaison
    avec le nombre de places de l'avion. Ajout refusé si nombre de places max atteint.
    """

    # Affichage de la liste des vols pour en choisir un.
    print("\nLes vols existants sont : ")
    voir_id_vols(conn, cursor)
    print()
    vol_id = input("Entrez l'ID du vol : ")

    # --------------------------------Récupère le nombre de places max --------------------------
    cursor.execute("SELECT avion->'model'->>'nombrePlaces' from schema_json_psql.VolNR v where v.id = %s", (vol_id,))
    result = cursor.fetchone()
    if not result:
        print("Pas de vol avec cet id!")

    else:

        nbPlacesMax = int(result[0])

        # ------------------------------ Compter le nombre de passager ----------------------
        cursor.execute("SELECT SUM(json_array_length(passager::json))::numeric as nb_passagers_actuel FROM schema_json_psql.VolNR WHERE id = %s", (vol_id,)) 
        result = cursor.fetchone()
        nb_passagers_actuel = int(result[0])
        print(f"Il y a actuellement {nb_passagers_actuel} passagers actuel dans le vol.", end=" ")
        print(f"Le nombre de places maximal est {nbPlacesMax}.")

        if nbPlacesMax <= nb_passagers_actuel:
            print("Vous ne pouvez donc pas rajouter de passager.")
        else:

            print("Vous pouvez donc rajouter un passager.")

            # Sélection des informations et conversion dans le type demandé.
            nom = input("Nom: ")
            prenom = input("Prénom: ")
            dateNaiss = input("Date de naissance (YYYY-MM-DD): ")
            rue = input("Rue: ")
            codepostal = input("Code postal: ")
            ville = input("Ville: ")
            pays = input("Pays: ")
            numeroTel = input("Numéro de téléphone: ")
            nombreBagage = int(input("Ajouter le nombre total de bagages : "))
            poidsBagage = float(input("Ajouter le poids total des bagages : "))

            # Création de l'objet JSON
            nouveau_passager = {
                "nom": nom,
                "prenom": prenom,
                "dateNaiss": dateNaiss,
                "rue": rue,
                "codepostal": codepostal,
                "ville": ville,
                "pays": pays,
                "numeroTel": numeroTel,
                "bagages": {
                    "nombreBagage" : nombreBagage,
                    "poidsBagage" : poidsBagage,
                }
            }

            # Vérifier si le vol existe déjà
            cursor.execute("SELECT VolNR.passager FROM VolNR WHERE id = %s;", (vol_id,))
            result = cursor.fetchone()

            if result:
                # Le vol existe, ajouter le passager à la liste
                passagers_existants = result[0]
                passagers_existants.append(nouveau_passager)
                cursor.execute("UPDATE VolNR SET passager = %s WHERE id = %s;",
                              (json.dumps(passagers_existants), vol_id))

                print("Passager ajouté avec succès.")
                conn.commit()


def supprimer_passager(conn, cursor):
    """
    Suppresion d'un passager sur la base de son nom,prénom, numéro de téléphone.

    Le nom et prénom de tous les passagers sont listés ainsi que le numéro de téléphone.
    L'utilisateur en supprime un en sélectionnant sa position dans la liste (en partant de 1).
    """
    # Affichage de la liste des vols pour en choisir un.
    print("\nLes vols existants sont : ")
    voir_id_vols(conn, cursor)
    print()

    # Récupération du vol
    vol_id = input("Entrez l'ID du vol pour voir les passagers : ")
    sql = "SELECT passager FROM VolNR WHERE id = %s"
    cursor.execute(sql, (vol_id,))
    result = cursor.fetchone()

    if not result or not result[0]:
        print(f"Aucun passager trouvé pour le vol {vol_id}.")
        return

    # Affichage de tous les passagers de ce vol
    passagers = result[0]
    print("Passagers du vol :")
    for idx, passager in enumerate(passagers, 1):
        print(f"{idx}. {passager['nom']} {passager['prenom']} {passager['numeroTel']}")

    # Suppression basé sur l'index.
    passager_idx = int(input(f"Entrez l'index du passager à supprimer dans la liste (entre [1, {len(passagers)}]) :")) - 1
    if 0 <= passager_idx < len(passagers):
        passager_a_supprimer = passagers[passager_idx]

        # Supprime le passager de la liste
        passagers.pop(passager_idx)

        # Met à jour la base de données
        sql = "UPDATE VolNR SET passager = %s WHERE id = %s"
        cursor.execute(sql, (json.dumps(passagers), vol_id))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"Passager {passager_a_supprimer['nom']} {passager_a_supprimer['prenom']} supprimé avec succès.")
        else:
            print("Aucun passager n'a été supprimé. Vérifiez les informations.")
    else:
        print("Numéro de passager invalide.")

def view_requests(conn,cursor):
    """
    Effectue les requêtes demandés et affiche le résultat.
    """
    # --------------- Requête 1 --------------
    req1="SELECT SUM((p->'bagages'->>'poidsBagage')::numeric) AS poids_total_bagages FROM schema_json_psql.VolNR v, JSON_ARRAY_ELEMENTS(v.passager) p WHERE v.destination = 'Istanbul' OR v.provenance = 'Istanbul';"
    cursor.execute(req1)
    result = cursor.fetchone()
    
    if result and result[0] is not None:
        poids_total_bagages = result[0]
        print(f"Poids total : {poids_total_bagages}")
    else:
        print("No baggage weight found for the specified conditions.")


    # --------------- Requête 3 --------------
    req3="SELECT compagnieVol, SUM(json_array_length(passager::json)) AS total_passagers FROM schema_json_psql.VolNR WHERE type = 'VolDepart' GROUP BY compagnieVol ORDER BY total_passagers DESC LIMIT 10;"   
    cursor.execute(req3)
    print(f"Les compagnies sont : {cursor.fetchall()}")

def main():
    # Connection
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    init(cur)

    # Menu principal
    while True:
        print("\nMenu Principal")
        print("1. Voir les tables")
        print("2. Ajouter un passager à un vol")
        print("3. Supprimer un passager d’un vol")
        print("4. Voir les résultats des requêtes")
        print("5. Quitter")
        choice = input("Entrez votre choix : ")

        if choice == "1":
            voir_vol(conn,cur)
        elif choice == "2":
            ajouter_passager(conn,cur)
        elif choice == "3":
            supprimer_passager(conn,cur)
        elif choice == "4":
            view_requests(conn,cur)
        elif choice == "5":
            print("Au revoir !")
            break
        else:

            print("Choix invalide, veuillez réessayer.")

    # Fermeture de la connection
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
