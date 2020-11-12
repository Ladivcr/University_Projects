#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""
##################ARCHIVO DE FUNCIONES#################################

import mysql.connector
from mysql.connector import errorcode
import json

def conexionMorelia():
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

        return("\t¡Conexión a BDMorelia exitosa!")
        #cnx.close()
    except:
        return("La conexión a BDMorelia fallo...")

def conexionPatzcuaro():
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

        return("\t¡Conexión a BDPátzcuaro exitosa!")
    except:
        return("La conexión a BDPátzcuaro fallo...")


def TP():
    """
    Procesador de transacciones (TP)
    - Recibe y procesa las solicitudes de datos de la aplicación (remota y local)
    - Es un componente de software
    - Se debe encontrar en cada computadora o equipo que pida datos
    - También se conoce como procesador de aplicaciones o administrador
    de transacciones
    """
    pass
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
