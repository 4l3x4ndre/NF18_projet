import psycopg2
import sys
import subprocess

HOST = "localhost"
USER = "me"
PASSWORD = "secret"
DATABASE = "mydb"
   

def init(cur):
    cur.execute(open("drop.sql", "r").read())
    cur.execute(open("create.sql", "r").read())
    cur.execute(open("insert.sql", "r").read())

def modif_passager():
    idpassager = int(input("Entrez l'id du passager à modifier : "))
    numerotel = input("Entrez le nouveau numéro de téléphone : ")

    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    sql = "UPDATE Passager SET numerotel = %s WHERE idpassager = %s;"
    cur.execute(sql, (numerotel, idpassager))
    conn.commit()
    conn.close()



def main(): 
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    init(cur)
        
    requests = open("request.sql", "r").read().split(";")
    requests = [request for request in requests if request.strip() != ""]
    for request in requests:
        cur.execute(request)
        print("La requête suivante a été exécutée :")
        print(request)
        print("Résultat de la requête :")
        for record in cur:
            print(record)
        print("--------------------------------------")

    conn.close()

if __name__ == "__main__":
    main()
