import sqlite3 as sq
import json as js
import sys

def build(jsData):

    try:

        idPlayer = jsData["authInfo"]["id"]
        token = jsData["authInfo"]["token"]
        buildType = jsData["buildingType"]
        xb = jsData['x']
        yb = jsData['y']

        conn = sq.connect('main.db')
        cur = conn.cursor()


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
            if (xb>=xs+1) and (yb>=ys+1) and (xb<=xs+40-sx) and (yb<=ys+40-sy):
                if ((xb>=xs) and (xb<=xs+18-sx) and (yb>=ys) and (yb<=ys+41-sy)) or ((xb>=xs) and (xb<=xs+41-sx) and (yb>=ys+23) and (yb<=ys+41-sy)) or ((xb>=xs+23) and (xb<=xs+41-sx) and (yb>=ys) and (yb<=ys+41-sy)) or ((xb>=xs) and (xb<=xs+41-sx) and (yb>=ys) and (yb<=ys+18-sy)):
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

            if ((xb>=xs) and (xb<=xs+41) and (yb>=dy+dsy+1) and (yb<=ys+41)) or ((xb>=dx+dsx+1) and (xb<=xs+41) and (yb>=ys) and (yb<=ys+41)) or ((xb>=xs) and (xb<=xs+41) and (yb>=ys) and (yb<=dy-1)) or ((xb>=xs) and (xb<=dx-1) and (yb>=ys) and (yb<=ys+41)):
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
                cur.execute("INSERT INTO Buildings VALUES ({}, {}, {}, '{}', {}, '{}');".format(idNewBuild, xb, yb, buildType, idSector))
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

        conn = sq.connect('main.db')
        cur = conn.cursor()

        type = cur.execute("SELECT type FROM Buildings WHERE id={};".format(idB)).fetchall()[0][0]

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
            d["info"]["building"] = type

            return js.dumps(d).encode("utf-8")
    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")
