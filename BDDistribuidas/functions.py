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
    print("\t ########## AÑADIR CLIENTE ##########")
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
        status = TP(datos = client, data_type = "Cliente")
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
    print("\t ########## AÑADIR DIRECCIÓN ##########")
    print("\tIntroduce los siguientes datos para añadir la dirección\n")
    try:
        calle = str(input("Calle: ")); calle = calle.capitalize()
        numero = int(input("Número de casa: "))
        colonia = str(input("Colonia: ")); colonia = colonia.capitalize()
        estado = str(input("Estado: ")); estado = estado.capitalize()
        cp = str(input("Código Postal: "))
        rfc = str(input("RFC del Cliente: "))
    except:
        print("Algo hiciste mal, introduce los datos de nuevo")
    # Para TP
    direccion = [calle, numero, colonia, estado, cp, rfc]
    # Comprobamos que no haya un registro con estos DATOS
    try:
        # ANTES DE INSERTAR DEBEREMOS LLAMAR LA FUNCIÓN TP PARA
        # CORROBORAR QUE SEA UN REGISTRO GLOBAL
        status = TP(datos = direccion, data_type="Domicilio")
        #print(f"estado!! {status}")
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
        val = (calle, numero, colonia, estado, cp, rfc, )

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
    print("\t ########## BÚSQUEDA DE CLIENTE ##########")
    marca = "off"
    try:
        opt = int(input("\n1) Por Nombre\n2) Por RFC\n3) Por Domicilio\n\nIntroduce un número: "))

        if opt == 1:

            name = str(input("Introduce el nombre del cliente: ")).split(" ")
            if len(name) > 1:
                if len(name) == 2:
                    nombre = name[0].capitalize(); apeP = name[1].capitalize(); apeM = ""
                    sentence = 'SELECT * FROM Clientes WHERE Nombre LIKE %s"%" AND (ApellidoP LIKE %s"%" OR ApellidoM LIKE %s"%");'
                    val = (nombre, apeP, apeM, )
                elif len(name) == 3:
                    nombre = name[0].capitalize(); apeP = name[1].capitalize(); apeM = name[2].capitalize()
                    sentence = 'SELECT * FROM Clientes WHERE Nombre LIKE %s"%" AND ApellidoP LIKE %s"%" AND ApellidoM LIKE %s"%";'
                    val = (nombre, apeP, apeM, )
            else:
                name = name[0].capitalize()
                sentence = 'SELECT * FROM Clientes WHERE Nombre LIKE %s"%";'
                val = (name, )
        elif opt == 2:

            rfc = str(input("Introduce el RFC del cliente: "))
            sentence = 'SELECT * FROM Clientes WHERE RFC LIKE %s"%";'
            val = (rfc, )

            #print(sentence, val)
        elif opt == 3:
            marca = "on"
            # calle, numero, colonia, estado, CP
            print("\n\t## INSTRUCCIONES ##")
            print("\nIntroduce los datos en el siguiente orden y separados por espacio:")
            print("\tcalle, numero, colonia, estado, CP")
            print("\nIMPORTANTE: Introduce todos los datos")
            print("Si no conoces el dato, introduce '-' (guíon)")
            try:
                while True:
                    address = str(input("\nIntroduce la dirección: ")).split(" ")
                    #print(address)
                    if len(address) == 5:
                        calle = address[0].capitalize(); numero = address[1]
                        colonia = address[2].capitalize(); estado = address[3].capitalize()
                        cp = address[4]
                        #sentence = 'SELECT RFC FROM Direcciones WHERE Calle LIKE %s"%" OR (Numero LIKE %s"%" OR Colonia LIKE %s"%" OR Estado LIKE %s"%" OR CP LIKE %s"%");'
                        sentence = 'SELECT RFC FROM Direcciones WHERE Calle = %s OR (Numero = %s OR Colonia = %s OR Estado = %s OR CP = %s);'
                        val = (calle, numero, colonia, estado, cp, )
                        break
                    else:
                        print("Deben de ser 5 datos (los guines se cuentan)")
            except:
                print("Revisa que el segundo dato sea un número")

        #print(val)
        tmp_bufer = []
        #print("Tia")
        try:
            #print(sentence, val)
            for BD in BDS:
                cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
                cursor = cnx.cursor()
                #sentence = 'SELECT * FROM Clientes WHERE Nombre LIKE %s"%" ;'
                #val = (name,)
                cursor.execute(sentence, val)
                values = cursor.fetchall()
                #print(type(values),values)
                if len(values) != 0:
                    tmp_bufer.append(values)
                else:
                    pass

            if len(tmp_bufer) != 0 and marca == "off":
                cnx.close()
                return(tmp_bufer)
            elif len(tmp_bufer) != 0 and marca == "on":
                result = DP(searchByAdd = tmp_bufer)
                return(result)
            else:
                #print("No existe un cliente con esos datos")
                return(False)
        except:
            print("Algo a fallado en la búsqueda")
            return (False)

    except:
        print("Se requiere un número")



# 6) Listar clientes
def list_clients(BDS):
    try:
        #clientes = ['Nombre |  FeNacimiento  | RFC']
        clientes = []
        for BD in BDS:
            cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
            cursor = cnx.cursor()
            query = ("SELECT * FROM Clientes")
            cursor.execute(query)
            for row in cursor:
                #print(row)
                name = f"{row[0]} {row[1]} {row[2]}"
                fecha = str(row[3])
                cliente = {"Nombre": name, "FechaDeNacimiento": fecha, "RFC": row[4]}
                clientes.append(cliente)

        return(clientes)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return []
    else:
        cnx.close()

# TP nos ayudara a evaluar que no haya registros duplicados en la BD
# sino que los registro sean únicos y globales
#    Procesador de transacciones (TP)
# - Recibe y procesa las solicitudes de datos de la aplicación (remota y local)

def TP(datos, data_type):
    """
    datos = arreglo compuesto por los datos para hacer la revisión
    data_type = tipo de revisión que se realizara
    """
    if data_type == "Cliente":
        #Busqueda de cliente
        status = DP(cliente = datos)
        if status != 0:
            return(True)
        elif status == 0:
            return(False)
        else:
            return(False)

    elif data_type == "Domicilio":
        #Busqueda de domicilio
        status = DP(domicilio = datos)
        if status != 0:
            return(True)
        elif status == 0:
            return(False)
        else:
            return(False)


#Procesador de datos (DP)
# Guarda y recupera datos localizados en el sitio
def DP(cliente = None, domicilio = None, searchByAdd = None):
    """
    cliente = Datos del cliente para hacer la revisión de existencia
    domicilio = Datos de la dirección para hacer la revisión de existencia
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
            return(len(tmp_bufer))

        elif len(tmp_bufer) == 0 or len(tmp_bufer) < 0:
            cnx.close()
            return(0)

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
            return(len(tmp_bufer))

        elif len(tmp_bufer) == 0 or len(tmp_bufer) < 0:
            cnx.close()
            return(0)

    elif searchByAdd != None:
        tmp_bufer_aux = []
        #print("This is: ", searchByAdd)
        try:
            for values in searchByAdd:
                if len(values)>=2:
                    try:
                        for i in values:
                            #print(f"Datos del cliente-: {i[0]}")
                            tmp_bufer_aux.append(i[0])
                    except:
                        pass
                else:
                    #print(f"Datos del clientex: {values[0][0]}")
                    tmp_bufer_aux.append(values[0][0])
        except:
            pass

        try:
            tmp_bufer = []
            for bd in BD:
                cnx = mysql.connector.connect(user=user,
                password=password, host=host, database=bd)
                cursor = cnx.cursor()

                for rfc in tmp_bufer_aux:
                    sentence = "SELECT * FROM Clientes WHERE RFC = %s"
                    val = (rfc, )
                    cursor.execute(sentence, val)
                    values = cursor.fetchall()

                    if len(values) != 0:
                        tmp_bufer.append(values)
                    else:
                        pass
            else:
                if len(tmp_bufer) != 0:
                    return(tmp_bufer)
                else:
                    return(False)

        except:
            pass

        print(tmp_bufer)


    else:
        print("Error en los datos esperados")
        return(False)
