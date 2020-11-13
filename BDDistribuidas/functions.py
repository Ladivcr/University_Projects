#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""

"""
Algunas líneas que nos van a servir
cursos.execute("SHOW DATABASES")
mybds = cursor.fetchall() #obtener las bds de mi mysql

cursor.execute(f"USE {bd}") #usar una base de datos
cursor.execute("SHOW TABLES") #mostrar tablas
tables = cursor.fetchall()
"""
##################ARCHIVO DE FUNCIONES#################################

import mysql.connector
from mysql.connector import errorcode
import json
# Carga de las credenciales
with open("credentialsDBMorelia.json") as file:
    credentials = json.load(file)

# Seleccionamos las credenciales

user = credentials["credentials"][0]["user"]
password = credentials["credentials"][0]["password"]
host = credentials["credentials"][0]["host"]
#nameDB = credentials["credentials"][0]["database"]


def conexionMorelia():
    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user,
                password=password,
                host=host)

        cursor = cnx.cursor()
        cursor.execute("SHOW DATABASES")
        mybds = cursor.fetchall() #obtener las bds de mi mysql
        #print(mybds)
        # Elegimos la base de datos
        for bd in mybds:
            #print(bd[0])
            #print(bd[0] == "Morelia")
            if bd[0] == "Morelia":
                cursor.execute(f"USE {bd[0]}") #usar una base de datos
                print("Conexión a Morelia exitosa...\n")
                return(True)
    except:
        return(False)

def conexionPatzcuaro():
    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user,
                password=password,
                host=host)

        cursor = cnx.cursor()
        cursor.execute("SHOW DATABASES")
        mybds = cursor.fetchall() #obtener las bds de mi mysql
        # Elegimos la base de datos
        for bd in mybds:
            if bd[0] == "Patzcuaro":
                cursor.execute(f"USE {bd[0]}") #usar una base de datos
                print("Conexión a Pátzcuaro exitosa...\m")
                return(True)
    except:
        return(False)


# OPERACIONES A REALIZAR EN LA BASE DE DATOS

#1) Registras nuevo cliente
#2) Registrar nueva dirección
#3) Actualizar cliente
#4) Actualizar dirección
#5) Buscar clientes
#6) Listar clientes
#7) Listar clientes totales
        
def TP():
    """
        Procesador de transacciones (TP)
        - Recibe y procesa las solicitudes de datos de la aplicación (remota y local)
        - Es un componente de software
        - Se debe encontrar en cada computadora o equipo que pida datos
        - También se conoce como procesador de aplicaciones o administrador
        de transacciones
    """
def DP():
    """
    Procesador de datos (DP)
    Guarda y recupera datos localizados en el sitio
    - Es un componente de software que reside en cada computadora
    o equipo
    - Puede que sea un dbms local
    """
    pass

"""
#Componentes de un DDBMS TP y DP
- La comunicación entre los TP y los DP
es posible mediante protocolos, usados por el DDBMS
- Los DP y los TP se pueden agregar al sistema sin
afectar la operación de los otros componentes.
- Un TP y un DP pueden residir en la misma computadora,
permitiendo al usuario final tener acceso transparente a datos
locales y remotos.

#Protocolos entre TP y DP
Los protocolos determinan la forma en que el sistema
de bdd trabaja:
- Se entrelazan con la red para transportar datos y comandos
entre procesadores de datos (DP) y (TP)
- Sincroniza todos los datos recibidos de las DP
(lado de TP) y enruta los datos recuperados a los TP
apropiados (lado de DP)
- Asegura funciones de base de datos comunes en
un sistema distribuido.
"""
