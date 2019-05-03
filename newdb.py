import sqlite3 as sq
import sys
import os
#from registration import registration as reg

def newdb():

    os.remove("main.db")

    try:
        conn = sq.connect('main.db')
        cur = conn.cursor()
        cur.execute(
                        """CREATE TABLE Players (
                        id int NOT NULL PRIMARY KEY,
                        name varchar(255) NOT NULL,
                        password varchar(255),
                        token varchar(255),
                        email varchar(255),
                        r int,
                        g int,
                        b int,
                        resources int,
                        levelT int,
                        levelG int,
                        levelP int
                        )
                        """)


        cur.execute(
                        """CREATE TABLE Sectors (
                        id int NOT NULL PRIMARY KEY,
                        x int,
                        y int,
                        idPlayer int,
                        isBlocked int
                        )
                        """)  #isBlocked is 0 or 1. 1==BLOCKED

        cur.execute(
                        """CREATE TABLE Buildings (
                        id int NOT NULL PRIMARY KEY,
                        x int,
                        y int,
                        type varchar(255),
                        idSector int,
                        Data varchar(255)
                        )
                        """)


        #cur.execute("INSERT INTO Players VALUES (0, 'Test', 'qwerty', 'token', 'vlados400125@gmail.com', 255, 255, 255, 100, 1, 1, 1)")
        #cur.execute("INSERT INTO Sectors VALUES (0, 0, 0, 0, 0);")
        #cur.execute("INSERT INTO Sectors VALUES (1, 41, 0, 0, 0);")
        #cur.execute("INSERT INTO Sectors VALUES (2, 0, 41, 0, 0);")
        #cur.execute("INSERT INTO Buildings VALUES (0, 41, 0, 'Mine', 1, '{}');")
        conn.commit()
        print("yes")
    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))





if __name__=="__main__":
    newdb()
    #print(reg({'name': 'Vlad3001', 'password': "123456789", 'email': "vlados400127@gmail.com", 'color': {"r": 255, "g": 255, "b": 255}}))
