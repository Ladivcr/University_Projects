#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""

import mysql.connector
from mysql.connector import errorcode
import json 

"""
Algunas líneas que nos van a servir
cursos.execute("SHOW DATABASES")
mybds = cursor.fetchall() #obtener las bds de mi mysql

cursor.execute(f"USE {bd}") #usar una base de datos
cursor.execute("SHOW TABLES") #mostrar tablas
tables = cursor.fetchall()
"""

# Carga de las credenciales
with open("credencialesBD.json") as file:
    credentials = json.load(file)

# Seleccionamos las credenciales 
user = credentials["credentials"][0]["user"]
password = credentials["credentials"][0]["password"]
host = credentials["credentials"][0]["host"]
nameDB = credentials["credentials"][0]["database"]

# Hacemos la conexión 
try: 
    cnx = mysql.connector.connect(user=userDB,
            password=password,
            host=host,
            database=nameDB)
except:
    print("La conexión a fallado")
