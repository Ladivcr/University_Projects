import json
import mysql.connector
from mysql.connector import errorcode

with open('credentialsDBMorelia.json') as json_file:
    config1 = json.load(json_file)

with open('credentialsDBPatzcuaro.json') as json_file:
    config2 = json.load(json_file)


def list():
    try:
        cnx1 = mysql.connector.connect(**config1)
        cursor1 = cnx1.cursor()
        cnx2 = mysql.connector.connect(**config2)
        cursor2 = cnx2.cursor()
        query = ("SELECT * FROM clientes")
        cursor1.execute(query)
        clientes = ['ID |  Nombre  | RFC']
        clientes.append("---------Sucursal Morelia---------")
        for row in cursor1:
            cliente = "ID = " + str(row[0]) + ", nombre = " + str(row[1])+" "+str(row[2])+" "+str(row[3]) + ", RFC = " + str(row[4])
            clientes.append(cliente)
        cnx1.close()
        cursor2.execute(query)
        clientes.append("---------Sucursal Patzcuaro---------")
        for row in cursor2:
            cliente = "ID = " + str(row[0]) + ", nombre = " + str(row[1])+" "+str(row[2])+" "+str(row[3]) + ", RFC = " + str(row[4])
            clientes.append(cliente)
        cnx2.close()
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
        cnx1.close()
        cnx2.close()
