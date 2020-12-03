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
#print(datosconnect)
# Seleccionamos las credenciales para la bd central que alberga las
# sucursales
user = datosconnect["user"]
password = datosconnect["password"]
host = datosconnect["host"]
db = datosconnect["database"]

def create_table(BD, conectores):
    name_table = str(input("Introduce el nombre de la tabla, sin espacios: "))
    if " " in name_table: name_table = "_".join(name_table); name_table.capitalize

    num_valores = int(input("Introduce el número de columnas en la tabla: "))
    columnas = []
    for i in range(num_valores):
        name_columna = str(input(f"Nombre (sin espacios) de la columna {i+1}: "))
        columnas.append(name_columna)
    values = {columnas[i]: [] for i in range(len(columnas))}

    print(values)
    for key, value in values.items():
            option = int(input(f"¿Qué datos recibira la columna *{key}*?\n1) Texto\n2) Números\n3) Fechas\n4) Booleanos (valores si/no)\n> "))

            if option == 1:
                tmp = int(input("¿El dato puede quedar en blanco?\n1) Sí\n2) No\n> "))
                if tmp == 1:
                    leng = str(input("Introduce el número de caracteres: ")); value.append(f"VARCHAR({leng})")
                elif tmp == 2:
                    leng = str(input("Introduce el número de caracteres: ")); value.append(f"VARCHAR({leng}) NOT NULL")
                else:
                    print("El dato puede quedar en blanco por defecto...")
                    leng = str(input("Introduce el número de caracteres: ")); value.append(f"VARCHAR({leng})")

            elif option == 2:
                tmp = int(input("¿Tus números serán: 1) Enteros ó 2) Decimales\n> "))
                if tmp == 1:
                    tmp2 = int(input("¿El dato puede quedar en blanco?\n1) Sí\n2) No\n> "))
                    if tmp2 == 1:
                        value.append("INT")
                    elif tmp2 == 2:
                        value.append("INT NOT NULL")
                    else:
                        print("El dato puede quedar en blanco por defecto...")
                        value.append("INT")
                elif tmp == 2:
                    tmp2 = int(input("¿El dato puede quedar en blanco?\n1) Sí\n2) No\n> "))
                    if tmp2 == 1:
                        value.append("FLOAT")
                    elif tmp2 == 2:
                        value.append("FLOAT NOT NULL")
                    else:
                        print("El dato puede quedar en blanco por defecto...")
                        value.append("FLOAT")
                else: print("Opción no existente\nSe asignara por defecto <<FLOAT>>"); value.append("FLOAT")

            elif option == 3:
                tmp2 = int(input("¿El dato puede quedar en blanco?\n1) Sí\n2) No\n> "))
                if tmp2 == 1:
                    value.append("DATE")
                elif tmp2 == 2:
                    value.append("DATE NOT NULL")
                else:
                    print("El dato se puede quedar en blanco por defecto...")
                    value.append("DATE")

            elif option == 4:
                tmp2 = int(input("¿El dato puede quedar en blanco?\n1) Sí\n2) No\n> "))
                if tmp2 == 1:
                    value.append("BOOLEAN")
                elif tmp2 == 2:
                    value.append("BOOLEAN NOT NULL")
                else:
                    print("El dato se puede quedar en blanco por defecto...")
                    value.append("BOOLEAN")

    opt = int(input("la tabla se conectara a: 1) Clientes 2) Direcciones 3) Otra\n> "))

    #CREATE TABLE employees
    #(id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    #lastname VARCHAR(20), firstname VARCHAR(20), phone VARCHAR(20),  dateofbirth DATE)


    # Formar la sentencia sql
    #tmp_cont = len(values)
    aux = show_tables(BD, conectores)
    sentence = f"CREATE TABLE {name_table} (Id{aux} INT(11) AUTO_INCREMENT PRIMARY KEY, "
    for key, value in values.items():
        #if tmp_cont == 0:
            #sentence += f"{key} {value}"
        #else:
            #sentence += f"{key} {value}, "

        sentence += f"{key} {value[0]}, "


    if opt == 1:
        #Clientes
        tmp_c = "RFC VARCHAR(13) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL, FOREIGN KEY (RFC) REFERENCES Clientes(RFC));"
        sentence += tmp_c
    elif opt == 2:
        #Direcciones
        tmp_d = "Id INT(11) NOT NULL, FOREIGN KEY (Id) REFERENCES Direcciones(Id));"
        sentence += tmp_d
    elif opt == 3:
        tmp_name = str(input("Introduce el nombre de la tabla CORRECTAMENTE: "))
        tmp_name = tmp_name.capitalize()
        ################
        user = conectores[0]; password = conectores[1]; host = conectores[2]
        try:
            cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
            cursor = cnx.cursor()
            cursor.execute(f"DESCRIBE {tmp_name}")
            tmp_val = cursor.fetchone()
            tmp_id = tmp_val[0]+" "+tmp_val[1]
            cnx.close()
        except:
            print("A fallado la conexión\nCreación de la tabla interrumpida...")
            return(False)

        ################
        tmp_o = f"{tmp_id} NOT NULL, FOREIGN KEY ({tmp_val[0]}) REFERENCES {tmp_name}({tmp_val[0]}));"
        sentence += tmp_o
    else:
        print("Opción no existe, se conectara automaticamente a *Clientes...")
        tmp_c = "RFC VARCHAR(13) CHARACTER SET utf8 COLLATE utf8_spanish_ci NOT NULL, FOREIGN KEY (RFC) REFERENCES Clientes(RFC));"
        sentence += tmp_c

    #print(values, len(values))
    print(sentence)
    user = conectores[0]; password = conectores[1]; host = conectores[2]
    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
        cursor = cnx.cursor()
        cursor.execute(sentence)
        cnx.close()
        print("Tabla creada exitosamente...")
        return(True)
    except:
        print("A fallado la conexión\nCreación de la tabla interrumpida...")
        return(False)

    return(None)

def show_tables(BD, conectores):
    user = conectores[0]; password = conectores[1]; host = conectores[2]
    try:
        cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
        cursor = cnx.cursor()
        cursor.execute("SHOW TABLES;")
        result = cursor.fetchall()
        print(result)
        cnx.close()
        return(len(result))
    except:
        print("A fallado la conexión\nNo se pueden mostrar las tablas")
        return(False)

def all_dbs():
    try:
        cnx = mysql.connector.connect(user=user, password=password,
        host=host, database=db)

        cursor = cnx.cursor()
        sentence = 'SELECT * FROM Sucursales'
        cursor.execute(sentence)
        values = cursor.fetchall()
        bd1 = values[0][5]; bd2 = values[1][5]
        #print(usuario, contrasena, host, sucursal)
        cnx.close()
        return([bd1, bd2])

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return (False)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return (False)
        else:
            return (False)

def conexion(BD, conectores):
    # Hacemos la conexión
    try:
        user = conectores[0]; password = conectores[1]; host = conectores[2]
        cnx = mysql.connector.connect(user=user, password=password,
        host=host, database=BD)
        print(f"Conexión a {BD} exitosa...\n")
        return(True)
    except:
        return(False)

#################################### ESTANDAR DE OPCIONES ###################
##################ARCHIVO MENU#################################
def acciones():
    print("\t¿Qué deseas hacer?")
    print("1) Registras nuevo cliente\n2) Registrar nueva dirección")
    print("3) Actualizar cliente\n4) Actualizar dirección")
    print("5) Buscar cliente\n6) Listar clientes")
    print("7) Cambiar ubicación\n8) Crear una tabla\n9) Mostrar tablas existentes")
    print("10) Salir")
    try:
        option = int(input("\nIntroduce un número: "))
        if option < 1 or option > 10:
            print("La opción no existe\n")
        else:
            return(option)
    except:
        print("Te he pedido un número")


# OPERACIONES A REALIZAR EN LA BASE DE DATOS

#1) Registras nuevo cliente
def add_client(BD, conectores):
    #print(conectores)
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
        user = conectores[0]; password = conectores[1]; host = conectores[2]
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
def add_address(BD, conectores):
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
        user = conectores[0]; password = conectores[1]; host = conectores[2]
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
def search_client(BDS, conectores):
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
                user = conectores[0]; password = conectores[1]; host = conectores[2]
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
def list_clients(BDS, conectores):
    try:
        #clientes = ['Nombre |  FeNacimiento  | RFC']
        clientes = []
        user = conectores[0]; password = conectores[1]; host = conectores[2]
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

def list_direcciones(BDS, conectores):
    try:
        #clientes = ['Nombre |  FeNacimiento  | RFC']
        direcciones = []
        user = conectores[0]; password = conectores[1]; host = conectores[2]
        for BD in BDS:
            cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
            cursor = cnx.cursor()
            query = ("SELECT * FROM Direcciones")
            cursor.execute(query)
            for row in cursor:
                #print(row)
                name = f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}"
                cliente = {"Id":row[0], "Calle": row[1], "Numero": row[2], "Colonia": row[3], "Estado": row[4], "CP": row[5], "RFC": row[6]}
                direcciones.append(cliente)

        return(direcciones)
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

def update_client(BD,conectores):
    result = list_clients([BD], conectores)
    print(f"\tLista de clientes - Total: {len(result)} \n")
    #print(result)
    for v in result:
        name, fenac, RFC = v.values()
        print(name, fenac, RFC)
    user = conectores[0]; password = conectores[1]; host = conectores[2]
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
    cursor = cnx.cursor()
    uptable = "UPDATE Clientes SET "
    upvalues = " = %s WHERE RFC = %s"
    columns = ["Nombre","ApellidoP","ApellidoM","RFC"]
    IdExist = False
    while not(IdExist):
        print("\nIngresa el RFC del cliente que quieres actualizar")
        idClient = input("> ")
        line = cursor.execute("SELECT * FROM Clientes WHERE RFC = %s;",[idClient])
        for a in cursor:
            print(columns[0], a[1], columns[1], a[2], columns[2], a[3], columns[3], a[4])
            IdExist = True
        if(not(IdExist)):
            print("El Id que ingresaste no existe")
    for c in columns:
        yes = 3
        if(c == "idCliente"):
            while (yes != 1 or yes != 2):
                print("\nQuieres cambiar", c, ": 1 sí, o 2 para terminar")
                yes = int(input("> "))
                if(yes == 1):
                    print("\nA que valor lo quieres cambiar")
                    value = input("> ")
                    values = [c,value,idClient]
                    update = (uptable+str(c)+upvalues)
                    cursor.execute(update,values)
                    cnx.commit()
                    break
                elif(yes == 2):
                    break
            break

        while (yes != 1 or yes != 2):
            print("\nQuieres cambiar", c, ": 1 sí, o 2 para continuar a la siguiente columna")
            yes = int(input("> "))
            if(yes == 1):
                print("\nA que valor lo quieres cambiar")
                value = input("> ")
                values = [value,idClient]
                update = (uptable+str(c)+upvalues)
                cursor.execute(update,values)
                cnx.commit()
                break
            elif(yes == 2):
                break
    result = list_clients([BD], conectores)
    print(f"\tLista de clientes - Total: {len(result)} \n")
    #print(result)
    for v in result:
        name, fenac, RFC = v.values()
        print(name, fenac, RFC)

def update_address(BD, conectores):
    result = list_direcciones([BD], conectores)
    print(f"\tLista de direcciones - Total: {len(result)} \n")
    #print(result)
    for v in result:
        id, calle, numero, colonia, estado, cp, rfc = v.values()
        print(id, calle, numero, colonia, estado, cp, rfc)
    user = conectores[0]; password = conectores[1]; host = conectores[2]
    cnx = mysql.connector.connect(user=user, password=password, host=host, database=BD)
    cursor = cnx.cursor()
    uptable = "UPDATE Direcciones SET "
    upvalues = " = %s WHERE Id = %s"
    columns = ["Id","Calle","Numero","Colonia","Estado","CP"]
    IdExist = False
    while not(IdExist):
        print("\nIngresa el ID de la dirección que quieres actualizar")
        idClient = input("> ")
        line = cursor.execute("SELECT * FROM Direcciones WHERE Id = %s;",[idClient])
        for a in cursor:
            print(columns[0], a[1], columns[1], a[2], columns[2], a[3], columns[3], a[4],columns[4], a[5], columns[5], a[6])
            IdExist = True
        if(not(IdExist)):
            print("El Id que ingresaste no existe")
    for c in columns:
        yes = 3
        if(c == "idCliente"):
            while (yes != 1 or yes != 2):
                print("\nQuieres cambiar", c, ": 1 sí, o 2 para terminar")
                yes = int(input("> "))
                if(yes == 1):
                    print("\nA que valor lo quieres cambiar")
                    value = input("> ")
                    values = [c,value,idClient]
                    update = (uptable+str(c)+upvalues)
                    cursor.execute(update,values)
                    cnx.commit()
                    break
                elif(yes == 2):
                    break
            break

        while (yes != 1 or yes != 2):
            print("\nQuieres cambiar", c, ": 1 sí, o 2 para continuar a la siguiente columna")
            yes = int(input("> "))
            if(yes == 1):
                print("\nA que valor lo quieres cambiar")
                value = input("> ")
                values = [value,idClient]
                update = (uptable+str(c)+upvalues)
                cursor.execute(update,values)
                cnx.commit()
                break
            elif(yes == 2):
                break
    result = list_direcciones([BD], conectores)
    print(f"\tLista de direcciones - Total: {len(result)} \n")
    #print(result)
    for v in result:
        id, calle, numero, colonia, estado, cp, rfc = v.values()
        print(id, calle, numero, colonia, estado, cp, rfc)

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
