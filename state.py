import time
import sqlite3 as sq
import json as js
import sys

def stateEvent(jsData):
    try:
        id = jsData["authInfo"]["id"]
        token = jsData["authInfo"]["token"]

        conn = sq.connect('main.db')
        cur = conn.cursor()

        d = {"type": "StateRequestSuccess"}
        d["gameState"] = {}
        d["gameState"]["playerId"] = id
        d["gameState"]["attackEvents"] = []
        d["gameState"]["resources"] = cur.execute("SELECT resources FROM Players WHERE id={};".format(id)).fetchall()[0][0]
        d["gameState"]["time"] = time.time()

        d["gameState"]["players"] = []
        players = cur.execute("SELECT id, name, r, g, b FROM Players;").fetchall()
        for player in players:
            d["gameState"]["players"].append({})
            d["gameState"]["players"][-1]["playerId"] = player[0]
            d["gameState"]["players"][-1]["name"] = player[1]
            d["gameState"]["players"][-1]["color"] = {}
            d["gameState"]["players"][-1]["color"]["r"] = player[2]
            d["gameState"]["players"][-1]["color"]["g"] = player[3]
            d["gameState"]["players"][-1]["color"]["b"] = player[4]
            d["gameState"]["players"][-1]["sectors"] = []
            sectors = cur.execute("SELECT id, x, y FROM Sectors WHERE idPlayer={};".format(player[0])).fetchall()
            for sector in sectors:
                d["gameState"]["players"][-1]["sectors"].append({})
                d["gameState"]["players"][-1]["sectors"][-1]["x"] = sector[1]
                d["gameState"]["players"][-1]["sectors"][-1]["y"] = sector[2]
                d["gameState"]["players"][-1]["sectors"][-1]["sectorId"] = sector[0]
                d["gameState"]["players"][-1]["sectors"][-1]["buildings"] = []
                buildings = cur.execute("SELECT id, x, y, type, Data FROM Buildings WHERE idSector={};".format(sector[0])).fetchall()
                for build in buildings:
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"].append({})
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["type"] = build[3]
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["x"] = build[1]
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["y"] = build[2]
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["id"] = build[0]
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["playerId"] = player[0]
                    d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["sectorId"] = sector[0]
                    if build[3]=='Hangar':
                        d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["units"] = {}
                        d["gameState"]["players"][-1]["sectors"][-1]["buildings"][-1]["units"]["units"] = []

        #return d
        return js.dumps(d).encode("utf-8")
    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))
    return js.dumps({"type": "WrongAuthInfo"}).encode("utf-8")



if __name__=="__main__":
    import pprint as pp
    pp.pprint(stateEvent({"authInfo": {"id": 0, "token": "blabla"}}))
