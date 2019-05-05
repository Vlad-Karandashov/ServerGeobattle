import sqlite3 as sq
import json as js
import sys
from functions import *


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
        sectors = cur.execute("SELECT x, y FROM Sectors;").fetchall()


        if resources >= 50:
            if len(mySectors) == 0:
                canBuild = True
            else:
                isNeighbour = False
                exists = False
                for mySector in mySectors:
                    horizontalNeighbour = abs(mySector[0] - xbs) == 41 and mySector[1] == ybs
                    verticalNeighbour = abs(mySector[1] - ybs) == 41 and mySector[0] == xbs
                    if horizontalNeighbour or verticalNeighbour:
                        isNeighbour = True
                    if mySector[0] == xbs and mySector[1] == ybs:
                        exists = True

                canBuild = isNeighbour and not exists

            if not canBuild:
                return js.dumps({"type": "WrongPosition"}).encode("utf-8")


            for sector in sectors:
                if rectangles_intersect(sector[0], sector[1], 41, 41, xbs, ybs, 41, 41):
                    return js.dumps({"type": "IntersectsWithEnemy"}).encode("utf-8")





            try:
                idNewSector = 1 + cur.execute("SELECT id FROM Sectors;").fetchall()[-1][0]
            except Exception as exc:
                idNewSector = 0

            cur.execute("INSERT INTO Sectors VALUES ({}, {}, {}, {}, {});".format(idNewSector, xbs, ybs, idPlayer, 0))
            cur.execute("UPDATE Players SET resources = {} WHERE id = {};".format(resources-50, idPlayer))
            conn.commit()

            ret = {}
            ret["type"] = "SectorBuilt"
            ret["info"] = {}
            ret["info"]["playerIndex"] = idPlayer
            ret["info"]["x"] = xbs
            ret["info"]["y"] = ybs
            ret["info"]["id"] = idNewSector

            return js.dumps(ret).encode('utf-8')

        else:
            return js.dumps({"type": "NotEnoughResources"}).encode("utf-8")

    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    return js.dumps({"type": "WrongPosition"}).encode("utf-8")
