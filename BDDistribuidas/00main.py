#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""
import sys
import json
import functions
import mysql.connector
from mysql.connector import errorcode

###############CONEXIÓN A LA SUCURSAL#############
# Carga de las credenciales de manera global para todas las funciones
with open("credentials.json") as file:
    credentials = json.load(file)

datosconnect = credentials["credentials"]
# Seleccionamos las credenciales para conectarnos a la bd central y de
# ahí obtener las credenciales para las sucursales
User = datosconnect["user"]
Password = datosconnect["password"]
Host = datosconnect["host"]
DB = datosconnect["database"]

#print(User, Password, Host, DB)

def current_ubicacion():
    try:
        #ELECCION DE UBICACIÓN POR PARTE DEL USUARIO
        print("\nElige tu ubicación introduciendo un número\n")
        opt = int(input("\n1) Morelia\n2) Pátzcuaro\n\n> "))
        if opt == 1:
            opt = "Morelia"
            #tmp_status = False
        elif opt == 2:
            opt = "Patzcuaro"
            #tmp_status = False
            #break
    except:
        print("Debes introducir un número para identificarte...")

    try:
        cnx = mysql.connector.connect(user=User, password=Password, host=Host, database=DB)

        cursor = cnx.cursor()
        sentence = 'SELECT * FROM Sucursales WHERE db = %s;'
        val = (opt, )
        cursor.execute(sentence, val)
        values = cursor.fetchall()
        usuario = values[0][2]; contrasena = values[0][3]
        hosting = values[0][4]; sucursal = values[0][5]
        #print(usuario, contrasena, host, sucursal)
        cnx.close()
        return([usuario, contrasena, hosting, sucursal])

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return (False)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return (False)
        else:
            return (False)


BDS = functions.all_dbs()
#print(BDS)
#BDS = ["Morelia", "Patzcuaro"]
tmp_status = True
while(tmp_status):
    values = current_ubicacion()
    if values:
        #print(values)
        user = values[0]; passwd = values[1]
        hoster = values[2]; ubicacion = values[3]
        #print(user, passwd, hoster, ubicacion)
        tmp_status = False
        break
    elif not(values):
        print("Algo a fallado a la hora de elegir ubicación y no podemos continuar sin ubicación")
        sys.exit(1)


while True:
    try:
        sucursal = ubicacion
        datos_coneccion = [user, passwd, hoster]  # Mis credenciales
        status = functions.conexion(sucursal, datos_coneccion)
        if(status):
            #print(datos_coneccion)
            break
        elif not(status):
            print("Algo a fallado en la conexión a la sucursal, reinicia el script y vuelve a intentar")
    except:
        print("Error en la función de conexion, no debería pasar. Reportalo al admin.")


tmp_status_menu = True
while(tmp_status_menu):
    print(f"\n\tUbicación Actual: {sucursal}\n")
    # CONEXION A Morelia DADA LA UBICACION ELEGIDA
    BD = sucursal
    opcion = functions.acciones()
    # 1) Registras nuevo cliente
    if opcion == 1:
        status = functions.add_client(BD, datos_coneccion)
        if(status):
            print("\t\nRegistro de cliente efectuado correctamente")
        elif not(status):
            print("\t\nNo ha sido posible efectuar el registro del cliente")
        else:
            print("\t\nAlgo a salido mal a la hora de efectuar el registro del cliente")
    #2) Registrar nueva dirección
    elif opcion == 2:
        status = functions.add_address(BD, datos_coneccion)
        if(status):
            print("\t\nRegistro de dirección efectuado correctamente")
        elif not(status):
            print("\t\nNo ha sido posible efectuar el registro de la dirección")
        else:
            print("\t\nAlgo a salido mal a la hora de efectuar el registro de dirección")

    #3) Actualizar cliente
    elif opcion == 3:
        functions.update_client(BD, datos_coneccion)

    #4) Actualizar dirección
    elif opcion == 4:
        #update_address(BDS, datos_coneccion)

    #5) Buscar cliente
    elif opcion == 5:
        result = functions.search_client(BDS, datos_coneccion)
        if not(result):
            print("No existe un cliente con esos datos")
        else:
            #print(len(result),result)
            print("Lista de coincidencias")
            for values in result:
                if len(values) >= 2:
                    for i in values:
                        print(f"Datos del cliente: {i}")
                else:
                    print(f"Datos del cliente: {values}")

    # 6) Listar clientes
    elif opcion == 6:
        result = functions.list_clients(BDS, datos_coneccion)
        if not(result):
            print("No existe un cliente con esos datos")
        else:
            #print(len(result),result)
            print(f"\tLista de clientes - Total: {len(result)} \n")
            #print(result)
            for values in result:
                name, fenac, RFC = values.values()
                print(name, fenac, RFC)

    #7) Cambiar ubicación
    elif opcion == 7:
        sucursal = current_ubicacion()
        sucursal = sucursal[-1]
        print(sucursal)
    #8) crear tabla
    elif opcion == 8:
        status = functions.create_table(BD, datos_coneccion)

<<<<<<< HEAD

    #9) Mostrar Tablas
=======
    #9) Salir
>>>>>>> 30e3205993c0618823e5a6a4f16afd5051fe3e6c
    elif opcion == 9:
        status = functions.show_tables(BD, datos_coneccion)
        
    #10) Salir
    elif opcion == 10:
        print("Hasta luego...")
        break

    else:
        print("Esa opción no existe")
