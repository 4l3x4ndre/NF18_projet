import psycopg2
import sys
import subprocess
from interface.menu import menu
from interface.display import affiche_note

HOST = "localhost"
USER = "me"
PASSWORD = "secret"
DATABASE = "mydb"



    

def init(cur):
    cur.execute(open("drop.sql", "r").read())
    cur.execute(open("create.sql", "r").read())
    cur.execute(open("insert.sql", "r").read())

def main(): 
    conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD))
    cur = conn.cursor()
    init(cur)

    conn.close()

if __name__ == "__main__":
    main()
