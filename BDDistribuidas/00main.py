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
status = True
while status:
    try:
        print("Elige un número")
        opt = int(input("\n1) Morelia\n2) Pátzcuaro\n3) Salir\n"))
    except:
        print("Debes introducir un número para identificarte...")

    # Morelia
    if opt == 1:
        print(functions.conexionMorelia())
    # Pátzcuaro
    elif opt == 2:
        print(functions.conexionPatzcuaro())
    # Salir
    elif opt == 3:
        print("Hasta luego...")
        status = False
    else:
        print("Esa opción no existe")
