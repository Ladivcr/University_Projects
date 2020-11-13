#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas & Gustavo Alfredo Zarate Acosta
About: Tablas distribuidas
"""
import functions
##################ARCHIVO MENU#################################
def acciones():
    print("\t¿Qué deseas hacer?")
    print("1) Registras nuevo cliente\n2) Registrar nueva dirección")
    print("3) Actualizar cliente\n4) Actualizar dirección")
    print("5) Buscar cliente\n6) Listar clientes\n7) Listar clientes totales")
    try:
        option = int(input("\nIntroduce un número: "))
        if option < 1 or option > 7:
            print("La opción no existe\n")
        else:
            return(option)
    except:
        print("Te he pedido un número")


programa = True
while programa:
    try:
        #ELECCION DE UBICACIÓN POR PARTE DEL USUARIO
        print("Elige tu ubicación introduciendo un número")
        opt = int(input("\n1) Morelia\n2) Pátzcuaro\n3) Salir\n"))
    except:
        print("Debes introducir un número para identificarte...")

    # CONEXION A Morelia DADA LA UBICACION ELEGIDA
    if opt == 1:
        status = functions.conexionMorelia()
        if status == True:
            opcion = acciones()

            #1) Registras nuevo cliente
            if opcion == 1:
                pass
                status = add_client()

            #2) Registrar nueva dirección
            elif opcion == 2:
                pass
                status = add_address()

            #3) Actualizar cliente
            elif opcion == 3:
                pass
                status = update_client()

            #4) Actualizar dirección
            elif opcion == 4:
                pass
                status = update_address()

            #5) Buscar cliente
            elif opcion == 5:
                pass
                result = search_client()

            #6) Listar clientes
            elif opcion == 6:
                pass
                result = list_clients()

            #7) Listar clientes totales
            elif option == 7:
                pass
                result = list_total_clients()

        elif status == False:
            print("Algo fallo en la conexión a Morelia, contacta al admin.")



    # CONEXION A Pátzcuaro DADA LA UBICACION ELEGIDA
    elif opt == 2:
        status = functions.conexionPatzcuaro()
        if status == True:
            opcion = acciones()
        elif status == False:
            print("Algo fallo en la conexión a Pátzcuaro, contacta al admin.")


    # Salir
    elif opt == 3:
        print("Hasta luego...")
        programa = False
    else:
        print("Esa opción no existe")
