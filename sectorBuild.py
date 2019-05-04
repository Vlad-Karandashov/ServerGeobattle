import sqlite3 as sq
import json as js
import sys



def sectorBuild(jsData):
    try:

        conn = sq.connect('main.db')
        cur = conn.cursor()

        idPlayer = jsData["authInfo"]["id"]
        token = jsData["authInfo"]["token"]

        try:
            if token != cur.execute("SELECT token FROM Players WHERE id={};".format(idPlayer)).fetchall()[0][0]:
                return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")
        except:
            return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")

        xbs = jsData["x"]
        ybs = jsData["y"]

        cur.execute("SELECT resources FROM Players WHERE id={};".format(idPlayer))
        resources = cur.fetchall()[0][0]

        mySectors = cur.execute("SELECT x, y FROM Sectors WHERE idPlayer={};".format(idPlayer)).fetchall()
        #sectors = cur.execute("SELECT x, y FROM Sectors;").fetchall()


        if resources >= 50:
            marker = False
            for mySector in mySectors:
                if ((mySector[0]+41==xbs) or (mySector[0]-41==xbs)) and ((mySector[1]+41==ybs) or (mySector[1]-41==ybs)):
                    marker = True

            if marker:

                try:
                    idNewSector = 1 + cur.execute("SELECT id FROM Sectors;").fetchall()[-1][0]
                except:
                    idNewSector = 0

                cur.execute("INSERT INTO Sectors VALUES ({}, {}, {}, {}, {});".format(idNewSector, xbs, ybs, idPlayer, 0))
                conn.commit()

                ret = {}
                ret["type"] = "SectorBuilt"
                ret["info"] = {}
                ret["info"]["playerIndex"] = idPlayer
                ret["info"]["x"] = xbs
                ret["info"]["y"] = ybs
                ret["info"]["id"] = idPlayer

                return js.dumps(ret).encode('utf-8')

            else:
                return js.dumps({"type": "WrongPosition"}).encode("utf-8")

        else:
            return js.dumps({"type": "NotEnoughResources"}).encode("utf-8")


    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    return js.dumps({"type": "WrongPosition"}).encode("utf-8")
