import random as rand
import sqlite3 as sq
import json as js
import sys
from newdb import newdb

def registration(jsData):

    try:
        conn = sq.connect('main.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM Players")
        data = cur.fetchall()
        if data != []:
            id = data[-1][0]+1 #next id
        else:
            id = 0



        try:
            name = jsData['name']
        except:
            return js.dumps({'type': 'NameExists'}).encode("utf-8")


        if len(name) == 0:
            return js.dumps({'type': 'NoName'}).encode("utf-8")

        if (len(name)>=15) or (len(name)<=3):
            d = {"type": 'InvalidNameLength', "min": 4, "max": 14}
            d["actual"] = len(name)
            return js.dumps(d).encode("utf-8")


        try:
            password = jsData['password']
        except:
            return js.dumps({'type': 'NoPassword'}).encode("utf-8")


        if len(password) == 0:
            return js.dumps({'type': 'NoPassword'}).encode("utf-8")

        if (len(password)>=20) or (len(password)<=3):
            d = {"type": 'InvalidPasswordLength', "min": 4, "max": 19}
            d["actual"] = len(password)
            return js.dumps(d).encode("utf-8")




        token = "".join([chr(rand.randint(65, 90)) for x in range(12)])
        cur.execute("SELECT * FROM Players")
        data = cur.fetchall()

        try:
            email = jsData['email']
        except:
            return js.dumps({'type': 'EmailExists'}).encode("utf-8")



        for player in data:
            if player[1] == name:
                return js.dumps({'type': 'NameExists'}).encode("utf-8")
            if player[4] == email:
                return js.dumps({'type': 'EmailExists'}).encode("utf-8")


        try:
            r = jsData['color']['r']
            g = jsData['color']['g']
            b = jsData['color']['b']
        except:
            return js.dumps({'type': 'ColorExists'}).encode("utf-8")


        resources = 100
        levelT = 1
        levelG = 1
        levelP = 1

        cur.execute("INSERT INTO Players VALUES ({}, '{}', '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, {});".format(id, name, password, token, email, r, g, b, resources, levelT, levelG, levelP))
        conn.commit()

        d = {"type": "Success"}
        d['authInfo'] = {}
        d['authInfo']['id'] = id
        d['authInfo']['token'] = token

        return js.dumps(d).encode("utf-8")





    except Exception as exc:
        print(exc)
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))




def authorization(jsData):

    try:

        conn = sq.connect('main.db')
        cur = conn.cursor()

        cur.execute("SELECT id, name, password, token FROM Players")
        data = cur.fetchall()

        for i in range(len(data)):
            if data[i][1] == jsData['name'] and data[i][2] == jsData['password']:
                token = "".join([chr(rand.randint(65, 90)) for x in range(12)])
                cur.execute("UPDATE Players SET token = '{}' WHERE id = {};".format(token, i))
                conn.commit()
                d = {"type": "Success", "authInfo": {}}
                d["authInfo"]['id'] = i
                d["authInfo"]['token'] = token
                return js.dumps(d).encode("utf-8")

        return js.dumps({"type": "PairNotFound"}).encode("utf-8")
    except:
        return js.dumps({"type": "PairNotFound"}).encode("utf-8")





if __name__=="__main__":
    from pprint import pprint as pp

    newdb()

    #print(registration({"name": "vladislav", "email": "vlados400125@gmail.com", "password": "1234567", "color": {"r": 255, "g": 255, "b": 255}}))

    #print(authorization({"type": "Authorization", "name": "vladislav", "password": "1234567"}))

    conn = sq.connect('main.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM Players")
    pp(cur.fetchall())
