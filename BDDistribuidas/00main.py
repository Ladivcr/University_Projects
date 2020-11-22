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
    print("8) Volver al inicio")
    try:
        option = int(input("\nIntroduce un número: "))
        if 1 > option or option > 8:
            print("La opción no existe\n")
        else:
            return(option)
    except:
        print("Te he pedido un número")


BDS = ["Morelia", "Patzcuaro"]
while(True):
    try:
        #ELECCION DE UBICACIÓN POR PARTE DEL USUARIO
        print("\nElige tu ubicación introduciendo un número\n")
        opt = int(input("\n1) Morelia\n2) Pátzcuaro\n3) Salir\n"))
    except:
        print("Debes introducir un número para identificarte...")

    # CONEXION A Morelia DADA LA UBICACION ELEGIDA
    if opt == 1:
        BD = "Morelia"
        status = functions.conexion(BD)  # Comprobamos que se pueda hacer la conexión
        if status == True:
            BD = "Morelia"
            opcion = acciones()
            # 1) Registras nuevo cliente
            if opcion == 1:
                status = functions.add_client(BD)
                if status == True:
                    print("\t Registro efectuado correctamente")
                elif status == False:
                    print("\t No ha sido posible efectuar el registro")
                else:
                    print("\t Algo a salido mal a la hora de efectuar el registro del cliente")
            #2) Registrar nueva dirección
            elif opcion == 2:
                status = functions.add_address(BD)
                if status == True:
                    print("\t Registro de dirección efectuado correctamente")
                elif status == False:
                    print("\t No ha sido posible efectuar el registro de la dirección")
                else:
                    print("\t Algo a salido mal a la hora de efectuar el registro de dirección")

            #3) Actualizar cliente
            elif opcion == 3:
                pass
                #status = update_client()

            #4) Actualizar dirección
            elif opcion == 4:
                pass
                #status = update_address()

            #5) Buscar cliente
            elif opcion == 5:
                result = functions.search_client(BDS)
                if result == False:
                    print("No existe un cliente con esos datos")
                else:
                    if len(result)>5:
                        for values in result:
                            print(f"Datos del cliente: {values}")
                    else:
                        print(f"Datos del cliente: {result}")

            #6) Listar clientes
            elif opcion == 6:
                pass
                #result = list_clients()

            #7) Listar clientes totales
        elif opcion == 7:
                pass
                #result = list_total_clients()
        elif opcion == 8:
            break

        elif status == False:
            print("Algo fallo en la conexión a Morelia, contacta al admin.")



    # CONEXION A Pátzcuaro DADA LA UBICACION ELEGIDA
    elif opt == 2:
        BD = "Patzcuaro"
        status = functions.conexion(BD) # Comprobar que se efectuo la conexión
        if status == True:
            opcion = acciones()
            # 1) Registras nuevo cliente
            if opcion == 1:
                status = functions.add_client(BD)
                if status == True:
                    print("\t Registro efectuado correctamente")
                elif status == False:
                    print("\t No ha sido posible efectuar el registro")
                else:
                    print("\t Algo a salido mal a la hora de efectuar el registro del cliente")
            #2) Registrar nueva dirección
            elif opcion == 2:
                status = functions.add_address(BD)
                if status == True:
                    print("\t Registro de dirección efectuado correctamente")
                elif status == False:
                    print("\t No ha sido posible efectuar el registro de la dirección")
                else:
                    print("\t Algo a salido mal a la hora de efectuar el registro de dirección")

            #3) Actualizar cliente
            elif opcion == 3:
                pass
                #status = update_client()

            #4) Actualizar dirección
            elif opcion == 4:
                pass
                #status = update_address()

            #5) Buscar cliente
            elif opcion == 5:
                result = functions.search_client(BDS)
                if result == False:
                    print("No existe un cliente con esos datos")
                else:
                    if len(result)>5:
                        for values in result:
                            print(f"Datos del cliente: {values}")
                    else:
                        print(f"Datos del cliente: {result}")

            #6) Listar clientes
            elif opcion == 6:
                pass
                #result = list_clients()

            #7) Listar clientes totales
        elif opcion == 7:
                pass
                #result = list_total_clients()

        elif status == False:
            print("Algo fallo en la conexión a Pátzcuaro, contacta al admin.")


    # Salir
    elif opt == 3:
        print("Hasta luego...")
        break
    else:
        print("Esa opción no existe")
