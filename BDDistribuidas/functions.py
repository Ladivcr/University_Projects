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

#nameDB = credentials["credentials"][0]["database"]
# Carga de las credenciales de manera global para todas las funciones
with open("credentials.json") as file:
    credentials = json.load(file)

datosconnect = credentials["credentials"][0]
# Seleccionamos las credenciales
user = datosconnect["user"]
password = datosconnect["password"]
host = datosconnect["host"]

def conexion(BD):
    # Hacemos la conexión
    try:
        cnx = mysql.connector.connect(user=user, password=password,
        host=host, database=BD)
        print(f"Conexión a {BD} exitosa...\n")
        return(True)
    except:
        return(False)



# OPERACIONES A REALIZAR EN LA BASE DE DATOS

#1) Registras nuevo cliente
def add_client(BD):
    print("\tIntroduce los siguientes datos para añadir el cliente\n")
    name = str(input("Nombre: ")); name = name.capitalize()
    apellidoP = str(input("Apellido Paterno: ")); apellidoP = apellidoP.capitalize()
    tmp_AP = apellidoP
    apellidoM = str(input("Apellido Materno: ")); apellidoM = apellidoM.capitalize()
    tmp_AM = apellidoM
    año = str(input("Introduce el AÑO de nacimiento (formato YYYY): "))
    mes = str(input("Introduce el MES de nacimiento (formato MM): "))
    dia = str(input("Introduce el DIA de nacimiento (formato DD): "))
    fechaN = f"{año}-{mes}-{dia}"
    # PARA FORMAR EL RFC nos basamos en: http://cec.cele.unam.mx/include/howToRFC.php
    # Así mismo, programamos algunas excepciones, no todas debido a que eran algo complejas
    # NO HEMOS INCLUIDO LA HOMOCLAVE debido a que el algoritmo es privado y si
    # lo haciamos pseudoaleatorio, corriamos el riesgo de duplicación
    # SOME RULE FOR MAKE RFC
    if apellidoM[0] == "Ñ":
         tmp_AM = apellidoM.replace("Ñ", "X", 1)
    if apellidoP[0] == "Ñ":
         tmp_AP = apellidoP.replace("Ñ", "X", 1)

    vocal = [i for i in name if i == "a" or i == "e" or i == "i" or i == "o" or i == "u"]

    if tmp_AM[0] == "X" and tmp_AP[0] == "X":
        RFC = tmp_AP[0].upper()+vocal[0].upper()+tmp_AM[0].upper()+name[0].upper()+año+mes+dia
    elif tmp_AM[0] == "X" and tmp_AP[0] != "X":
        RFC = apellidoP[0].upper()+vocal[0].upper()+tmp_AM[0].upper()+name[0].upper()+año+mes+dia
    elif tmp_AM[0] != "X" and tmp_AP[0] == "X":
        RFC = tmp_AP[0].upper()+vocal[0].upper()+apellidoM[0].upper()+name[0].upper()+año+mes+dia
    else:
        RFC = apellidoP[0].upper()+vocal[0].upper()+apellidoM[0].upper()+name[0].upper()+año+mes+dia


    # para TP
    client = [RFC]
    # Comprobamos que no haya un registro con estos DATOS
    try:
        # ANTES DE INSERTAR DEBEMOS LLAMAR LA FUNCIÓN TP PARA
        # CORROBORAR QUE SEA UN REGISTRO GLOBAL Y ÚNICO EN EL SISTEMA
        status = TP(cliente = client)
        if status == True:
            print("\n\tEl registro ya existe en una de las BD")
            return(False)
        elif status == False:
            pass
    except:
        print("Algo a fallado en TP")

    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host)#, database=BD)
        cursor = cnx.cursor()
        cursor.execute(f"USE {BD}")
        sentence = "INSERT INTO Clientes(Nombre, ApellidoP, ApellidoM, FeNacimiento, RFC) VALUES (%s, %s, %s, %s, %s)"
        val = (name, apellidoP, apellidoM, fechaN, RFC, )
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
    try:
        calle = str(input("Calle: ")); calle = calle.capitalize()
        numero = int(input("Número de casa: "))
        colonia = str(input("Colonia: ")); colonia = colonia.capitalize()
        estado = str(input("Estado: ")); estado = estado.capitalize()
        CP = str(input("Código Postal: "))
        rfc = str(input("RFC del Cliente: "))
    except:
        print("Algo hiciste mal, introduce los datos de nuevo")
    # Para TP
    direccion = [calle, numero, colonia, estado, CP, rfc]
    # Comprobamos que no haya un registro con estos DATOS
    try:
        # ANTES DE INSERTAR DEBEREMOS LLAMAR LA FUNCIÓN TP PARA
        # CORROBORAR QUE SEA UN REGISTRO GLOBAL
        status = TP(domicilio = direccion)
        print(f"estado!! {status}")
        if status == True:
            print("\n\tEl registro ya existe en una de las BD")
            return(False)
        elif status == False:
            pass
    except:
        print("Algo fallo en TP")

    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host)#, database=BD)
        cursor = cnx.cursor()
        cursor.execute(f"USE {BD}")
        sentence = "INSERT INTO Direcciones(Calle, Numero, Colonia, Estado, CP, RFC) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (calle, numero, colonia, estado, CP, rfc)

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
def search_client(BDS):
    tmp_bufer = []
    try:
        opt = int(input("\n1) Por Nombre\n2) Por RFC\n3) Por Domicilio\n\nIntroduce un número: "))
        if opt == 1:
            try:
                name = str(input("Introduce el nombre del cliente: "))
                for BD in BDS:
                    cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
                    cursor = cnx.cursor()
                    sentence = "SELECT * FROM Clientes WHERE Nombre = %s;"
                    val = (name,)
                    cursor.execute(sentence, val)
                    values = cursor.fetchall()
                    tmp_bufer.append(values)

                if len(tmp_bufer) != 0:
                    cnx.close()
                    return(tmp_bufer)
                else:
                    #print("No existe un cliente con esos datos")
                    return(False)
            except:
                print("Algo a fallado en la búsqueda")
                return (False)

        elif opt == 2:
            try:
                cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)

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
                cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)

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


    except:
        print("Se requiere un número")



# 6) Listar clientes
# 7) Listar clientes totales

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
        RFC = cliente[0]
        #print(RFC)
        tmp_bufer = []
        for bd in BD:

            cnx = mysql.connector.connect(user=user,
            password=password, host=host, database=bd)
            cursor = cnx.cursor()
            sentence = "SELECT Nombre, RFC FROM Clientes WHERE RFC = %s"
            val = (RFC, )
            cursor.execute(sentence, val)
            values = cursor.fetchall()

            if len(values) != 0:
                tmp_bufer.append(values)
            else:
                pass

        # En caso de no encontrar registros en ninguna de las BD,
        # se regresa un Estado falso ante la existencia
        # del registro y se permite realizarlo
        if len(tmp_bufer) != 0:
            cnx.close()
            return(True)

        else:
            cnx.close()
            return(False)

    # AUN NO JALA NO SÉ PORQUE, DEPURANDO
    elif domicilio != None:

        #Busqueda de domicilio
        #domicilio = [calle, numero, colonia, estado, CP, rfc]
        calle = domicilio[0]; numero = domicilio[1]; colonia = domicilio[2]
        estado = domicilio[3]; cp = domicilio[4]; rfc = domicilio[5]
        tmp_bufer = []
        for bd in BD:
            cnx = mysql.connector.connect(user=user,
            password=password, host=host, database=bd)
            cursor = cnx.cursor()

            #sentence = "SELECT Id, Calle FROM Direcciones WHERE Calle = %s and Numero = %s and Colonia = %s and Estado = %s and CP = %s and RFC = %s"
            #val = (calle, numero, colonia, estado, cp, rfc, )
            # Dado que no queremos tener clientes con multiples cuentas
            # Lo que vamos a verificar es la existencia de su RFC en
            # las direcciones
            sentence = "SELECT Id, Calle FROM Direcciones WHERE RFC = %s"
            val = (rfc, )
            cursor.execute(sentence, val)
            values = cursor.fetchall()

            if len(values) != 0:
                tmp_bufer.append(values)
            else:
                pass

        # En caso de no encontrar registros en ninguna de las BD,
        # se regresa un Estado falso ante la existencia
        # del registro y se permite realizarlo
        if len(tmp_bufer) != 0:
            cnx.close()
            return(True)

        else:
            cnx.close()
            return(False)
    else:
        print("Error en los datos esperados")
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
