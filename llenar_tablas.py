#!/usr/bin/python3

#####################################################################################
##  author: GUS VALERO      ##      titulo: RESET DE TABLAS CON DATOS DE EJEMPLO   ##   
#####################################################################################

import sqlite3

PATH_DB = 'menussh.db'

def sql_send_query(query):
    try:
        conexion = sqlite3.connect(PATH_DB)
    except Error:
        return Error
    finally:
        cursorObj = conexion.cursor()
        cursorObj.execute(query)
        conexion.commit()
        rows = cursorObj.fetchall()
        conexion.close()
        return rows

# TABLA CLIENTE

query = "DELETE FROM cliente"
resultado = sql_send_query(query)

for fila in range(20):
    query = "INSERT INTO cliente(cli_descripcion) VALUES ('cliente-"+str(fila)+"')"
    sql_send_query(query)

# TABLA SERVIDOR

query = "DELETE FROM servidor"
resultado = sql_send_query(query)

query = "SELECT * FROM cliente"
clientes = sql_send_query(query)

for cliente in clientes:
    for fila in range(10):
        query = "INSERT INTO servidor(srv_cliente, srv_id, srv_descripcion, srv_url, srv_port) VALUES ('"+str(cliente[0])+"' , '"+str(fila)+"', 'server-"+str(fila)+"', '192.168.200.1', '22')"
        resultado = sql_send_query(query)

# TABLA USER AND PASS

query = "DELETE FROM userandpass"
resultado = sql_send_query(query)

for cliente in clientes:
    query = "SELECT * FROM servidor WHERE srv_cliente= '"+str(cliente[0])+"'"
    servidores = sql_send_query(query)
    for servidor in servidores:
        for fila in range(5):
            query = "INSERT INTO userandpass(up_cliente, up_servidor, up_cli_srv_id, up_usuario, up_password) VALUES ('"+str(cliente[0])+"', '"+str(servidor[1])+"', '"+str(fila)+"', 'usuario-"+str(fila)+"', 'pass')"
            resultado = sql_send_query(query)
            
print("Gus said: Se termino de cargar tablas")