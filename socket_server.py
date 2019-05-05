# -*- coding: utf-8 -*-

import socket
import json as js
import registration as reg
import sqlite3 as sq
from newdb import newdb
import sys
import build
from time import time
from math import trunc
from state import stateEvent
from sectorBuild import sectorBuild

import param_parser

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

params = param_parser.parse_params(sys.argv[1:])

if "-i" in params.keys():
    ip = params["-i"]
else:
    ip = 'localhost' #'78.47.182.60'

if "-p" in params.keys() and params["-p"].isdigit():
    port = int(params["-p"])
else:
    port = 9090

if "-c" in params.keys():
    newdb()

resourcesTime  = time()

print(ip, port)
sock.bind((ip, port))
sock.listen(999)
sock.settimeout(0.5) #таймаут апгрейда
while True:
    try:
        while True:
            conn, addr = sock.accept()
            conn.settimeout(1)
            print('connected:', addr)

            data_res = ''
            while True:
                data1 = conn.recv(1024)
                if not data1.endswith('#'.encode('utf-8')):
                    data_res += data1.decode('utf-8')
                else:
                    data_res += data1.decode('utf-8')[0:-1:1]
                    break

            jsData = dict(js.loads(data_res))
            print(jsData)
            if jsData['type']=='RegistrationEvent':
                conn.send(reg.registration(jsData))
                conn.close()
                continue
                print("Finish")
            elif jsData['type']=='BuildEvent':
                conn.send(build.build(jsData))
                conn.close()
                print("Finish")
                continue
            elif jsData['type']=='AuthorizationEvent':
                conn.send(reg.authorization(jsData))
                conn.close()
                print("Finish")
                continue
            elif jsData['type']=='DestroyEvent':
                conn.send(build.destroy(jsData))
                conn.close()
                print("Finish")
                continue
            elif jsData['type'] == 'StateRequestEvent':
                conn.send(stateEvent(jsData))
                conn.close()
                print("Finish")
                continue
            elif jsData['type'] == 'SectorBuildEvent':
                conn.send(sectorBuild(jsData))
                conn.close()
                print("Finish")
                continue
            #conn.send(data_res)
            conn.close()
            print("NotThisType!")
            print()
    except Exception as exc:
        #Выполнится если произойдёт ошибка в сокете
        #или в течении 300-от секунд никто не подключится
        #РАЗУМЕЕТСЯ 300 СЕКУНД ЭТО ВРЕМЕННО!!!!
        #БУДУ ИСПОЛЬЗОВАТЬ это для ОБНОВЛЕНИЯ ИГРОВОГО СОСТОЯНИЯ каждые 300 секунд ЕСЛИ СЕРВЕР НИЧЕМ НЕ ЗАНЯТ

        print(exc)
        #print(type(exc)=="<'Socket.timeout'>")
        #print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno))

        passedTime = trunc(time() - resourcesTime)
        if passedTime < 8:
            pass
        else:
            conn = sq.connect('main.db')
            cur = conn.cursor()

            cur.execute("SELECT id, resources FROM Players;")
            play = cur.fetchall()

            for p in play:
                idPlayer = p[0]
                resPlayer = p[1]
                sectors = cur.execute("SELECT id FROM Sectors WHERE idPlayer={};".format(idPlayer)).fetchall()
                b = 0
                for sec in sectors:
                    sectorId = sec[0]

                    energy = 10
                    data = cur.execute("SELECT type FROM Buildings WHERE idSector={};".format(sectorId)).fetchall()
                    for i in data:
                        if i[0]=='Generator':
                            energy += 30
                        elif i[0]=='Mine':
                            energy -= 5
                        elif i[0]=='Turret':
                            energy -= 6
                        elif i[0]=='Hangar':
                            energy -= 10
                        else:
                            energy -= 4
                    if energy >= 0:
                        b += len(cur.execute("SELECT id FROM Buildings WHERE idSector={} AND type='Mine';".format(sectorId)).fetchall())
                b += len(sectors)
                max = 200 + len(sectors)*50

                print(b)
                line = max - b*trunc(passedTime/8)
                #print(max, ' ', line)
                if resPlayer<=line:
                    cur.execute("UPDATE Players SET resources = {} WHERE id = {};".format(resPlayer+b*trunc(passedTime/8), idPlayer))
                    conn.commit()
                else:
                    cur.execute("UPDATE Players SET resources = {} WHERE id = {};".format(max, idPlayer))
                    conn.commit()

            print(cur.execute("SELECT resources FROM Players").fetchall())

            resourcesTime = time()
            print("UPDATE ZA ", passedTime, " sec")


        #print("Upgrade")
        #print("-")
    continue
