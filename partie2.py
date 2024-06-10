import psycopg2
import datetime
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

def ajouter_passager(conn,cursor):
    vol_id = input("Entrez l'ID du vol : ")
    nom = input("Nom: ")
    prenom = input("Prénom: ")
    dateNaiss = input("Date de naissance (YYYY-MM-DD): ")
    rue = input("Rue: ")
    codepostal = input("Code postal: ")
    ville = input("Ville: ")
    pays = input("Pays: ")
    numeroTel = input("Numéro de téléphone: ")
    nombreBagage = int(input("Nombre de bagages: "))
    poidsBagage = float(input("Poids total des bagages: "))

    passager_id = int(input("Entrez l'ID du passager : "))
    nombreBagage= int(input("Entrez le nombre de bagage du passager : "))
    poidsBagage = float(input("Entrez le poids des bagages : "))
    sql="SELECT passager FROM BAGAGE WHERE passager=%s AND vol=%s"
    cursor.execute(sql,(passager_id,vol_id))
    passager = cursor.fetchone()
    if passager is None:
        sql ="SELECT nombrePlaces FROM Model JOIN Avion ON Model.nom = Avion.model JOIN Vol ON Vol.avion = Avion.id WHERE Vol.id =%s"
        cursor.execute(sql, (vol_id,))
        nb_place = cursor.fetchone()[0]
        sql = "SELECT COUNT(passager) FROM Bagage JOIN Vol ON Bagage.vol = Vol.id WHERE Vol.id =%s"
        cursor.execute(sql, (vol_id,))
        nb_passager = cursor.fetchone()[0]
        if (nb_place>nb_passager):
            cursor.execute("INSERT INTO Bagage (vol, passager,nombreBagage,poidsBagage) VALUES (%s, %s,%s,%s)",
                       (vol_id, passager_id, nombreBagage, poidsBagage))
            print("Passager ajouté avec succès.")
            conn.commit()
        else:
            print("Avion plein")
    else:
        print("Le passager est déjà dans le vol")
    cursor.close()
    conn.close()


def supprimer_passager(conn,cursor):
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cursor = conn.cursor()
    vol_id = input("Entrez l'ID du vol : ")
    passager_id = int(input("Entrez l'ID du passager : "))
    sql="SELECT * FROM Bagage WHERE (vol,passager)=(%s,%s)"
    cursor.execute(sql,(vol_id,passager_id))
    passager = cursor.fetchone()
    if (passager is None):
        print("Le passager n'est pas inscrit sur le vol")
    else:
        cursor.execute("DELETE FROM Bagage WHERE vol = %s AND passager = %s", (vol_id,passager_id))
        conn.commit()
        print("Passager supprimé avec succès.")
    cursor.close()
    conn.close()


def modifier_passager(conn,cursor):
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cursor = conn.cursor()
    passager_id = int(input("Entrez l'ID du passager à modifier : "))
    sql = "SELECT numeroTel FROM Passager WHERE id_personne =%s"
    cursor.execute(sql,(passager_id,))
    passager = cursor.fetchone()[0]
    if passager is not None :
        new_prenom = input("Donnez le nouveau prénom (ou l'ancien) de la personne : ")
        new_nom = input("Donnez le nouveau nom (ou l'ancien) de la personne : ")
        annee = int(input("Entrez l'année : "))
        mois = int(input("Entrez le mois : "))
        jour = int(input("Entrez le jour : "))
        new_date = datetime.date(annee, mois, jour)
        new_rue= input("Donnez la nouvelle rue (ou l'ancienne) de la personne : ")
        new_cp = input("Donnez le nouveau code postal (ou l'ancien) de la personne : ")
        new_ville = input("Donnez la nouvelle ville (ou l'ancienne) de la personne : ")
        new_pays = input("Donnez le nouveau pays (ou l'ancien) de la personne : ")
        cursor.execute("UPDATE Personne SET nom = %s,  prenom = %s, dateNaiss = %s,  rue = %s, ville = %s,  pays = %s , codepostal = %s  WHERE id_personne = %s", (new_nom, new_prenom, new_date,new_rue, new_ville, new_pays, new_cp, passager_id))
        conn.commit()
        print("Passager modifié avec succès.")
    else :
        print("Ce passager n'est pas présent dans notre base de données")
    cursor.close()
    conn.close()


def view_requests(conn,cursor):
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cursor = conn.cursor()
    # Vous devrez ajuster ces requêtes selon les vraies requêtes que vous souhaitez exécuter
    queries = [
        "SELECT SUM(poidsBagage) AS poids_total FROM Bagage B JOIN Vol V ON B.vol = V.id WHERE V.provenance = 'Istanbul' OR V.destination = 'Istanbul';",
        "SELECT Avion.id, COUNT(DISTINCT STEWARTTRAVAIL.stewart) AS nb_stew FROM STEWARTTRAVAIL JOIN Vol on vol.id = STEWARTTRAVAIL.vol RIGHT OUTER JOIN Avion ON Avion.id = vol.avion JOIN Model ON Model.nom = Avion.model WHERE Model.nom = 'A307' GROUP BY Avion.id;",
        "SELECT vol.compagnie, COUNT(DISTINCT bagage.passager) AS nb_pass FROM Vol LEFT OUTER JOIN BAGAGE ON Vol.id = BAGAGE.vol WHERE Vol.type = 'VolDepart' GROUP BY vol.compagnie ORDER BY nb_pass DESC LIMIT 3;"
    ]
    for query in queries:
        cursor.execute(query)
        results = cursor.fetchall()
        print("Résultats de la requête :")
        for result in results:
            print(result)
    cursor.close()
    conn.close()


def main():
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    init(cur)
    while True:
        print("\nMenu Principal")
        print("1. Voir les tables")
        print("2. Ajouter un passager à un vol")
        print("3. Supprimer un passager d’un vol")
        print("4. Modifier un passager")
        print("5. Voir les résultats des requêtes")
        print("6. Quitter")
        choice = input("Entrez votre choix : ")

        if choice == "1":
            voir_vol(conn,cur)
        elif choice == "2":
            ajouter_passager(conn,cur)
        elif choice == "3":
            supprimer_passager(conn,cur)
        elif choice == "4":
            modifier_passager(conn,cur)
        elif choice == "5":
            view_requests(conn,cur)
        elif choice == "6":
            print("Au revoir !")
            break
        else:

            print("Choix invalide, veuillez réessayer.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()