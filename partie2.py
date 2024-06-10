import datetime
import psycopg2
import json

# Configuration de la connexion à la base de données
HOST = "localhost"
USER = "leolamy"
PASSWORD = "Toutoukarl02-"
DATABASE = "postgres"

def init(cur):
    cur.execute(open("main_JSON_PSQL.sql", "r").read())

def voir_vol(conn,cursor):

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
    id_vol = input("Quel vol souhaitez-vous voir ? (id) : ")
    sql = "SELECT * FROM VolNR WHERE id = %s"
    cursor.execute(sql, (id_vol,))
    ligne = cursor.fetchone()
    while ligne:
        print(ligne)
        ligne = cursor.fetchone()
def ajouter_passager(conn, cursor):
    vol_id = input("Entrez l'ID du vol : ")
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
                      (vol_id, json.dumps([nouveau_passager])))

    print("Passager ajouté avec succès.")
    conn.commit()

def supprimer_passager(conn,cursor):
    voir_vol(conn,cursor)
    vol_id = input("Entrez l'ID du vol : ")
    sql="SELECT passager ->> 'id_personne' AS id_passager, passager ->> 'nom' AS nom, passager ->> 'prenom' AS prenom FROM VolNR WHERE VolNR.id = %s"
    cursor.execute(sql(vol_id,))
    passager=cursor.fetchall()
    for ligne in passager:
        print(ligne)
    passager_id = int(input("Entrez l'ID du passager à supprimer : "))
    sql="SELECT passager ->> 'id_personne' AS id_passager FROM VolNR WHERE VolNR.passager.id_personne = %s"
    cursor.execute(sql, (passager_id,))
    passager = cursor.fetchone()
    if (passager is None):
        print("Le passager n'est pas inscrit sur le vol")
    else:
        sql = "UPDATE VolNR SET passager=(SELECT jsonb_agg(passager) FROM jsonb_array_elements(passager) AS passager)WHERE passager->>'id_personne'<>%s"
        cursor.execute(sql, (passager_id,))
        conn.commit()
        print("Passager supprimé avec succès.")
    cursor.close()
    conn.close()

#def view_requests(conn,cursor):

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