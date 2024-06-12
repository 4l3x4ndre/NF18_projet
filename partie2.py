import datetime
import psycopg2
import json

# Configuration de la connexion à la base de données
HOST = "localhost"
USER = "me"
PASSWORD = "secret"
DATABASE = "mydb"

def init(cur):
    cur.execute(open("main_JSON_PSQL.sql", "r").read())

def voir_id_vols(conn, cursor):
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
    
    voir_id_vols(conn, cursor)

    id_vol = input("Quel vol souhaitez-vous voir ? (id) : ")
    sql = "SELECT * FROM VolNR WHERE id = %s"
    cursor.execute(sql, (id_vol,))
    ligne = cursor.fetchone()
    while ligne:
        print(ligne)
        ligne = cursor.fetchone()
def ajouter_passager(conn, cursor):
    print("\nLes vols existants sont : ")
    voir_id_vols(conn, cursor)
    print()
    vol_id = input("Entrez l'ID du vol : ")

    #req1="SELECT SUM((p->'bagages'->>'poidsBagage')::numeric) AS poids_total_bagages FROM schema_json_psql.VolNR v, JSON_ARRAY_ELEMENTS(v.passager) p WHERE v.destination = 'Istanbul' OR v.provenance = 'Istanbul';"

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
            else:
                # Le vol n'existe pas, le créer avec le premier passager
                cursor.execute("INSERT INTO VolNR (vol_id, passager) VALUES (%s, %s);",
                              (id, json.dumps([nouveau_passager])))

            print("Passager ajouté avec succès.")
            conn.commit()


def supprimer_passager(conn, cursor):
    print("\nLes vols existants sont : ")
    voir_id_vols(conn, cursor)
    print()
    vol_id = input("Entrez l'ID du vol pour voir les passagers : ")
    sql = "SELECT passager FROM VolNR WHERE id = %s"
    cursor.execute(sql, (vol_id,))
    result = cursor.fetchone()

    if not result or not result[0]:
        print(f"Aucun passager trouvé pour le vol {vol_id}.")
        return

    passagers = result[0]
    print("Passagers du vol :")
    for idx, passager in enumerate(passagers, 1):
        print(f"{idx}. {passager['nom']} {passager['prenom']}")

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
    #conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    #cursor = conn.cursor()
    req1="SELECT SUM((p->'bagages'->>'poidsBagage')::numeric) AS poids_total_bagages FROM schema_json_psql.VolNR v, JSON_ARRAY_ELEMENTS(v.passager) p WHERE v.destination = 'Istanbul' OR v.provenance = 'Istanbul';"
    cursor.execute(req1)
    result = cursor.fetchone()
    
    if result and result[0] is not None:
        poids_total_bagages = result[0]
        print(f"Poids total : {poids_total_bagages}")
    else:
        print("No baggage weight found for the specified conditions.")

    """
    req2="SELECT AVG((avion->>'model')::json->>'nombrePlaces')::numeric AS nombre_moyen_stewards FROM schema_json_psql.VolNR WHERE (avion->>'model')::json->>'nom' = 'A307';"
    cursor.execute(req2)
    print(cursor.fetchall())
    """

    req3="SELECT compagnieVol, SUM(json_array_length(passager::json)) AS total_passagers FROM schema_json_psql.VolNR WHERE type = 'VolDepart' GROUP BY compagnieVol ORDER BY total_passagers DESC LIMIT 10;"   
    cursor.execute(req3)
    print(f"Les compagnies sont : {cursor.fetchall()}")

def view_requests0(conn,cursor):
    queries = [
         "SELECT SUM((passager->>'bagages')::json->>'poidsBagage')::numeric AS poids_total_bagages FROM schema_json_psql.VolNR WHERE destination = 'Istanbul' OR provenance = 'Istanbul';",
        "SELECT AVG((avion->>'model')::json->>'nombrePlaces')::numeric AS nombre_moyen_stewards FROM schema_json_psql.VolNR WHERE (avion->>'model')::json->>'nom' = 'A307';.id = STEWARTTRAVAIL.vol RIGHT OUTER JOIN Avion ON Avion.id = vol.avion JOIN Model ON Model.nom = Avion.model WHERE Model.nom = 'A307' GROUP BY Avion.id;",
        "SELECT compagnieVol, SUM(json_array_length(passagerjson)) AS total_passagers FROM schema_json_psql.VolNR WHERE type = 'VolDepart' GROUP BY compagnieVol ORDER BY total_passagers DESC LIMIT 10;"
    ]
    for query in queries:
        cursor.execute(query)
        results = cursor.fetchall()
        print("Résultats de la requête :")
        for result in results:
            print(result)

def main():
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    init(cur)
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
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
