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


def conexionMorelia(BD):
    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user,
                password=password,
                host=host)

        cursor = cnx.cursor()
        cursor.execute(f"USE {BD}")
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
        cursor.execute(f"USE {BD}")
        print("Conexión a Pátzcuaro exitosa...\n")
        return(True)
    except:
        return(False)


# OPERACIONES A REALIZAR EN LA BASE DE DATOS

#1) Registras nuevo cliente
def add_client(BD):
    from datetime import datetime
    from random import choice
    date = str(datetime.now())

    #aux = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    #He eliminado la aleatoriedad en la homoclave para tener un
    #mejor control, así mimso el mes y el día
    #homoclave = choice(aux)+choice(aux)+choice(aux)
    año = date[2:4] #mes = date[5:7]; dia = date[8:10]
    aux = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9,
    "K":10, "L":11, "M":12, "N":13, "O":14, "P":16, "Q":17, "R":18, "S":19,
    "T":20, "U":21, "V":22, "W":23, "X":24, "Y":25, "Z":26}
    print("\tIntroduce los siguientes datos para añadir el cliente\n")
    name = str(input("Nombre: "))
    #name = name.upper()
    apellidoP = str(input("Apellido Paterno: "))
    #apellidoP = apellidoP.upper()
    apellidoM = str(input("Apellido Materno: "))
    #apellidoM = apellidoM.upper()
    homoclave = apellidoP[2:3].upper()+apellidoM[1:3].upper()+str(aux[name[-1].upper()])+str(aux[apellidoP[-1].upper()])
    RFC = apellidoP[0].upper()+apellidoP[1].upper()+apellidoM[0].upper()+name[0].upper()+año+homoclave
    Id =  name[0:2].upper()+apellidoP[0:2].upper()+apellidoM[0:2].upper()

    # para TP
    client = [name, RFC]
    # Comprobamos que no haya un registro con estos DATOS
    try:
        status = TP(cliente = client)
        #print("estado!!",status)
        if status == True:
            print("\n\tEl registro ya existe en una de las BD")
            return(False)
        elif status == False:
            pass
    except:
        pass

    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host)#, database=BD)
        cursor = cnx.cursor()
        cursor.execute(f"USE {BD}")
        sentence = "INSERT INTO Clientes(Id, Nombre, ApellidoP, ApellidoM, RFC) VALUES (%s, %s, %s, %s, %s)"
        val = (Id, name, apellidoP, apellidoM, RFC)
        # ANTES DE INSERTAR DEBEREMOS LLAMAR LA FUNCIÓN TP PARA
        # CORROBORAR QUE SEA UN REGISTRO GLOBAL
        cursor.execute(sentence, val)
        cursor.close()
        cnx.commit()
        cnx.close()
        return(True)
    except:
        return (False)


#2) Registrar nueva dirección
def add_address(BD):
    print("\tIntroduce los siguientes datos para añadir la dirección\n")
    calle = str(input("Calle: "))
    calle = calle.upper()

    numero = str(input("Número: "))

    colonia = str(input("Colonia: "))
    colonia = colonia.upper()

    estado = str(input("Estado (abreviado): "))
    estado = estado.upper()

    CP = str(input("Código Postal: "))
    idCliente = str(input("Id Cliente: "))

    Id =  estado[0:2]+colonia[0:2]+CP[0]+numero[0]
    # Para TP
    direccione = [calle, colonia, estado, CP]
    # Comprobamos que no haya un registro con estos DATOS
    try:
        print("Estoy aquí")
        status = TP(domicilio = direccione)
        print("estado!!")
        if status == True:
            print("\n\tEl registro ya existe en una de las BD")
            return(False)
        elif status == False:
            pass
    except:
        print("Algo fallo")

    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host)#, database=BD)
        cursor = cnx.cursor()
        cursor.execute(f"USE {BD}")
        sentence = "INSERT INTO Direcciones(Id, Calle, Numero, Colonia, Estado, CP, idCliente) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (Id, calle, numero, colonia, estado, CP, idCliente)
        # ANTES DE INSERTAR DEBEREMOS LLAMAR LA FUNCIÓN TP PARA
        # CORROBORAR QUE SEA UN REGISTRO GLOBAL
        cursor.execute(sentence, val)
        cursor.close()
        cnx.commit()
        cnx.close()
        return(True)
    except:
        return (False)
#3) Actualizar cliente
#4) Actualizar dirección
#5) Buscar clientes
# Búsqueda por: nombre, RFC o domicilio
def search_client(BD):
    try:
        opt = int(input("\n1) Por Nombre\n2) Por RFC\n3) Por Domicilio\n4) Listar todos los clientes\n\nIntroduce un número: "))
        if opt == 1:
            try:
                cnx = mysql.connector.connect(user=user,password=password, host=host, database=BD)

                name = str(input("Introduce el nombre del cliente: "))
                cursor = cnx.cursor()
                sentence = "SELECT * FROM Clientes WHERE Nombre = %s;"
                val = (name,)
                cursor.execute(sentence, val)
                valores_bd = cursor.fetchone()
                if len(valores_bd) != 0:
                    cnx.close()
                    return(valores_bd)
                else:
                    #print("No existe un cliente con esos datos")
                    return(False)
            except:
                print("Algo a fallado en la búsqueda")
                return (False)

        elif opt == 2:
            try:
                cnx = mysql.connector.connect(user=user,password=password, host=host, database=BD)

                rfc = str(input("Introduce el RFC del cliente: "))
                cursor = cnx.cursor()
                sentence = "SELECT * FROM Clientes WHERE RFC = %s;"
                val = (rfc,)
                cursor.execute(sentence, val)
                valores_bd = cursor.fetchone()
                if len(valores_bd) != 0:
                    cnx.close()
                    return(valores_bd)
                else:
                    #print("No existe un cliente con esos datos")
                    return(False)
            except:
                print("Algo a fallado en la búsqueda")
                return (False)

        elif opt == 3:
            try:
                cnx = mysql.connector.connect(user=user,password=password, host=host, database=BD)

                addre = str(input("Introduce el ID de la dirección del del cliente: "))
                cursor = cnx.cursor()
                sentence = "SELECT idCliente FROM Direcciones WHERE Id = %s;"
                val = (addre,)
                cursor.execute(sentence, val)
                valores_bd = cursor.fetchone()
                id_cliente = valores_bd[0]
                sentence = "SELECT * FROM Clientes WHERE Id = %s;"
                val = (id_cliente,)
                cursor.execute(sentence, val)
                valores_bd = cursor.fetchone()
                if len(valores_bd) != 0:
                    cnx.close()
                    return(valores_bd)
                else:
                    #print("No existe un cliente con esos datos")
                    return(False)
            except:
                print("Algo a fallado en la búsqueda")
                return (False)

        elif opt == 4:
            try:
                cnx = mysql.connector.connect(user=user,password=password, host=host, database=BD)

                cursor = cnx.cursor()
                cursor.execute("SELECT * FROM Clientes;")
                valores_bd = cursor.fetchall()
                if len(valores_bd) != 0:
                    cnx.close()
                    return(valores_bd)
                else:
                    #print("No existe un cliente con esos datos")
                    return(False)
            except:
                print("Algo a fallado en la búsqueda")
                return (False)

    except:
        print("Se requiere un número")



#6) Listar clientes
#7) Listar clientes totales

# TP nos ayudara a evaluar que no haya registros duplicados en la BD
# sino que los registro sean únicos y globales
#    Procesador de transacciones (TP)
# - Recibe y procesa las solicitudes de datos de la aplicación (remota y local)
def TP(cliente = None, domicilio = None):
    """
    cliente = arreglo compuesto por nombre y RFC del cliente
    domicilio = arreglo compuesto por calle, colonia, estado y CP
    BD = Base de datos en la que se efectuara la consulta
    """
    BD = ["Morelia", "Patzcuaro"]

    if cliente != None:
        #Busqueda de cliente
        name = cliente[0]; RFC = cliente[1]
        for bd in BD:
            cnx = mysql.connector.connect(user=user,
            password=password, host=host, database=bd)
            cursor = cnx.cursor()
            sentence = "SELECT Id, Nombre FROM Clientes WHERE Nombre = %s or RFC = %s"

            val = (name, RFC)

            cursor.execute(sentence, val)

            valores_bd = cursor.fetchone()

            # En caso de no encontrar registros en ninguna de las BD,
            # se regresa un Estado falso ante la existencia
            # del registro y se permite realizarlo
            if len(valores_bd) != 0:
                cnx.close()
                return(True)

        else:
            cnx.close()
            return(False)

    # AUN NO JALA NO SÉ PORQUE, DEPURANDO
    elif domicilio != None:

        #Busqueda de domicilio
        calle = domicilio[0]; colonia = domicilio[1]
        estado = domicilio[2]; cp = domicilio[3]
        for bd in BD:
            cnx = mysql.connector.connect(user=user,
            password=password, host=host, database=bd)
            cursor = cnx.cursor()
            sentence = "SELECT Id, Calle FROM Direcciones WHERE Calle = %s or Colonia = %s or Estado = %s or CP = %s"

            val = (calle, colonia, estado, cp)

            cursor.execute(sentence, val)

            valores_bd = cursor.fetchone()

            # En caso de no encontrar registros en ninguna de las BD,
            # se regresa un Estado falso ante la existencia
            # del registro y se permite realizarlo
            if len(valores_bd) != 0:
                cnx.close()
                return(True)

        else:
            cnx.close()
            return(False)

    else:
        print("Introduce los datos correctos")
        return(False)

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
