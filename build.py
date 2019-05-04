import sqlite3 as sq
import json as js
import sys
from functions import *

def build(jsData):

    try:

        idPlayer = jsData["authInfo"]["id"]
        token = jsData["authInfo"]["token"]
        buildType = jsData["buildingType"]
        xb = jsData['x']
        yb = jsData['y']

        conn = sq.connect('main.db')
        cur = conn.cursor()
        try:
            if token != cur.execute("SELECT token FROM Players WHERE id={};".format(idPlayer)).fetchall()[0][0]:
                return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")
        except:
            return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")


        cur.execute("SELECT resources FROM Players WHERE id={};".format(idPlayer))
        resources = cur.fetchall()[0][0]


        if buildType=='Beacon':
            return js.dumps({"Vlad": "Ne tot zapros"}).encode("utf-8")
        elif buildType=='Mine':
            sx = 5
            sy = 5
            cash = 25
            en = 0.5
        elif buildType=='Generator':
            sx = 5
            sy = 5
            cash = 25
            en = "!"
        elif buildType=='Hangar':
            sx = 7
            sy = 7
            cash = 50
            en = 1
        elif buildType=='ResearchCenter':
            sx = 6
            sy = 5
            cash = 50
            en = 0.4
        elif buildType=='Turret':
            sx = 2
            sy = 2
            cash = 15
            en = 0.6


        idSector = -1
        cur.execute("SELECT id, x, y, isBlocked FROM Sectors WHERE idPlayer={};".format(idPlayer))
        dataSectors = cur.fetchall()
        for sector in dataSectors:
            xs = sector[1]
            ys = sector[2]
            if rectangle_contains(xs, ys, 41, 41, xb - 1, yb - 1, sx + 2, sy + 2):
                if not rectangles_intersect(xs + 19, ys + 19, 3, 3, xb - 1, yb - 1, sx + 2, sy + 2):
                    idSector = sector[0]
                    isBlocked = sector[3]
                    break

        if idSector == -1:
            return js.dumps({"type": "NotInTerritory"}).encode("utf-8")



        cur.execute("SELECT x, y, type FROM Buildings WHERE idSector={};".format(idSector))
        dataBuildings = cur.fetchall()
        for build in dataBuildings:
            type = build[2]
            dx = build[0]
            dy = build[1]
            if type=='Mine':
                dsx = 5
                dsy = 5
            elif type=='Generator':
                dsx = 5
                dsy = 5
            elif type=='Hangar':
                dsx = 7
                dsy = 7
            elif type=='ResearchCenter':
                dsx = 6
                dsy = 5
            elif type=='Turret':
                dsx = 2
                dsy = 2

            if not rectangles_intersect(dx, dy, dsx, dsy, xb - 1, yb - 1, sx + 2, sy + 2):
                continue
            else:
                return js.dumps({"type": "NotInTerritory"}).encode("utf-8")





        if cash<=resources:
            if isBlocked == 0:
                cur.execute("SELECT id FROM Buildings")
                idBuildings = cur.fetchall()
                if idBuildings != []:
                    idNewBuild = idBuildings[-1][0]+1
                else:
                    idNewBuild = 0
                cur.execute("INSERT INTO Buildings VALUES ({}, {}, {}, '{}', {}, '');".format(idNewBuild, xb, yb, buildType, idSector))
                cur.execute("UPDATE Players SET resources = {} WHERE id = {};".format(resources-cash, idPlayer))
                conn.commit()
                ret = {"type": "Built"}
                ret['cost'] = cash
                ret['info'] = {}
                ret['info']['playerIndex'] = idPlayer
                ret['info']['building'] = {}
                ret['info']['building']['type'] = buildType
                ret['info']['building']['x'] = xb
                ret['info']['building']['y'] = yb
                ret['info']['building']['id'] = idNewBuild
                ret['info']['building']['playerId'] = idPlayer
                ret['info']['building']['sectorId'] = idSector
                if buildType=='Hangar':
                    ret['info']['building']["units"] = {}
                    ret['info']['building']["units"]["units"] = []
                return js.dumps(ret).encode('utf-8')
            return js.dumps({"type": "SectorBlocked"}).encode("utf-8")
        ret = {"type": "NotEnoughResources"}
        ret['required'] = cash
        return js.dumps(ret).encode("utf-8")
    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

    return js.dumps({"type": "NotInTerritory"}).encode("utf-8")

def destroy(jsData):
    try:

        idPlayer = jsData['authInfo']['id']
        idB = jsData['id']
        token = jsData['authInfo']['token']

        conn = sq.connect('main.db')
        cur = conn.cursor()

        try:
            if token != cur.execute("SELECT token FROM Players WHERE id={};".format(idPlayer)).fetchall()[0][0]:
                return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")
        except:
            return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")

        type = cur.execute("SELECT type FROM Buildings WHERE id={};".format(idB)).fetchall()[0][0]
        data = cur.fetchall("SELECT x, y FROM Buildings WHERE id={};".format(idB)).fetchall()
        x = data[0][0]
        y = data[0][1]
        cur.execute("SELECT idSector FROM Buildings WHERE id={};".format(idB))
        idSector = cur.fetchall()[0][0]
        print(idSector, "  - idSector")
        cur.execute("SELECT idPlayer FROM Sectors WHERE id={};".format(idSector))
        idPlayerB = cur.fetchall()[0][0]
        if idPlayer==idPlayerB:
            cur.execute("DELETE FROM Buildings WHERE id={};".format(idB))
            conn.commit()
            d = {"type": "Destroyed"}
            d["info"] = {}
            d["info"]["playerIndex"] = idPlayer
            d["info"]["building"] = {}
            d["info"]["building"]["type"] = type
            d["info"]["building"]["x"] = x
            d["info"]["building"]["y"] = y
            d["info"]["building"]["id"] = idB
            d["info"]["building"]["playerId"] = idPlayer
            d["info"]["building"]["sectorId"] = idSector


            return js.dumps(d).encode("utf-8")
    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")
