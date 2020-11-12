#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""
##################ARCHIVO MENU#################################

import mysql.connector
from mysql.connector import errorcode
import json
import functions

"""
Algunas líneas que nos van a servir
cursos.execute("SHOW DATABASES")
mybds = cursor.fetchall() #obtener las bds de mi mysql

cursor.execute(f"USE {bd}") #usar una base de datos
cursor.execute("SHOW TABLES") #mostrar tablas
tables = cursor.fetchall()
"""
try:
    print("Elige un número")
    opt = int(input("\n1) Morelia\n2) Pátzcuaro\n"))
except:
    print("Debes introducir un número para identificarte...")

# Morelia
if opt == 1:
    # Carga de las credenciales
    with open("credentialsDBMorelia.json") as file:
        credentials = json.load(file)

    # Seleccionamos las credenciales

    user = credentials["credentials"][0]["user"]
    password = credentials["credentials"][0]["password"]
    host = credentials["credentials"][0]["host"]
    nameDB = credentials["credentials"][0]["database"]

    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user,
                password=password,
                host=host,
                database=nameDB)

        print("\t¡Conexión a BDMorelia exitosa!")
        cnx.close()
    except:
        print("La conexión a BDMorelia fallo...")



# Pátzcuaro
elif opt == 2:
    # Carga de las credenciales
    with open("credentialsDBPatzcuaro.json") as file:
        credentials = json.load(file)

    # Seleccionamos las credenciales

    user = credentials["credentials"][0]["user"]
    password = credentials["credentials"][0]["password"]
    host = credentials["credentials"][0]["host"]
    nameDB = credentials["credentials"][0]["database"]

    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user,
                password=password,
                host=host,
                database=nameDB)

        print("\t¡Conexión a BDPátzcuaro exitosa!")
        cnx.close()
    except:
        print("La conexión a BDPátzcuaro fallo...")
