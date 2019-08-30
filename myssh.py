#!/usr/bin/python3

#####################################################################################
##  author: GUS VALERO      ##      titulo: ABM Y EJECUCION DE CONEXIONES SSH      ##   
#####################################################################################

import sqlite3
import curses

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

def imprimir_header(fullscreen):
    height, width = fullscreen.getmaxyx()
    text0 = "  _____                   _                     ______ ____ __"
    text1 = " / ___/__  ___  _____ __ (_)__  ___  ___ ___   / __/ // / // /"
    text2 = "/ /__/ _ \/ _ \/ -_) \ // / _ \/ _ \/ -_|_-<  _\ \/ _  / _  / " 
    text3 = "\___/\___/_//_/\__/_\_\/_/\___/_//_/\__/___/ /___/_//_/_//_/  "
    fullscreen.addstr( 0 , width//2 -len(text0)//2, text0)
    fullscreen.addstr( 1 , width//2 -len(text1)//2, text1)
    fullscreen.addstr( 2 , width//2 -len(text2)//2, text2)
    fullscreen.addstr( 3 , width//2 -len(text3)//2, text3)

def imprimir_footer(fullscreen, texto_one="", texto_two="", texto_three="", texto_four="", texto_five="", texto_six=""):
    height, width = fullscreen.getmaxyx()
    firma1 = " Gus Valero"
    firma2 = " Powered by"
    fullscreen.addstr( height-1 , width -len(firma1) -2, firma1)
    fullscreen.addstr( height-2 , width -len(firma2) -2, firma2)
    fullscreen.addstr( height-1 , width -len(texto_one) -4 -len(firma1), texto_one)
    fullscreen.addstr( height-2 , width -len(texto_two) -4 -len(firma2), texto_two)
    fullscreen.addstr( height-1 , width -len(texto_three) -len(texto_one) -6 -len(firma1), texto_three)
    fullscreen.addstr( height-2 , width -len(texto_four) -len(texto_two) -6 -len(firma2), texto_four)
    fullscreen.addstr( height-1 , width -len(texto_five) -len(texto_three) -len(texto_one) -8 -len(firma1), texto_five)
    fullscreen.addstr( height-2 , width -len(texto_six) -len(texto_four) -len(texto_two) -8 -len(firma2), texto_six)

def ingresar_de_dato(fullscreen, texto):
    height, width = fullscreen.getmaxyx()
    subscreen = curses.newwin(height-7, width, 5, 0)
    subscreen.clear()
    subscreen.refresh()
    subscreen.border()
    height, width = subscreen.getmaxyx()
    subscreen.addstr( (height//2)-1, width//2 -len(texto)//2, texto)
    subscreen.addstr( (height//2)+1, width//2 -len(texto)//2, "= ")
    curses.curs_set(1)
    curses.echo()
    subscreen.refresh()
    getDato = subscreen.getstr(height//2+1, width//2-(len(texto)//2)+2).decode("utf-8")
    subscreen.clear()
    curses.noecho()
    curses.curs_set(0)
    subscreen.refresh()
    return getDato

def imprimir_confirmar(fullscreen, option_selected, pregunta, limpiar=False):
    height, width = fullscreen.getmaxyx()
    subscreen = curses.newwin(height-7, width, 5, 0)
    subscreen.clear()
    if limpiar:
        subscreen.refresh()
        return True
    subscreen.border()
    height, width = subscreen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    subscreen.addstr((height//2)-2, width//2-(len(pregunta)//2), pregunta)
    if option_selected:
        subscreen.attron(curses.color_pair(1))
        subscreen.addstr(height//2, width//2-1, "SI")
        subscreen.attroff(curses.color_pair(1))
        subscreen.addstr(height//2+1, width//2-1, "NO")
    else:
        subscreen.attron(curses.color_pair(1))
        subscreen.addstr(height//2+1, width//2-1, "NO")
        subscreen.attroff(curses.color_pair(1))
        subscreen.addstr(height//2, width//2-1, "SI")
    subscreen.refresh()

def confirmacion(fullscreen, limpiar=False):
    resultado = False
    imprimir_confirmar(fullscreen, resultado, "Esta por eliminar el registro, ¿esta seguro?")
    if limpiar:
        imprimir_confirmar(fullscreen,resultado, " ",True)
        return False
    while True:
        key3 = fullscreen.getch()
        if key3 == curses.KEY_DOWN and resultado==True:
            resultado=False
        elif  key3 == curses.KEY_UP and resultado==False:
            resultado=True
        elif key3 == curses.KEY_ENTER or key3 in [10, 13]:
            break
        elif key3 == 27 or key3 == 360:
            #salir
            return False
        imprimir_confirmar(fullscreen, resultado, "Esta por eliminar el registro, ¿esta seguro?")
    return resultado

def imprimir_menu_usuario(fullscreen, lista_usuarios, usuario_selected):
    height, width = fullscreen.getmaxyx()
    menu_usuario_screen = curses.newwin(height-7, width, 5, 0)
    menu_usuario_screen.clear()   
    menu_usuario_screen.border()
    height, width = menu_usuario_screen.getmaxyx()
    tope_minimo = 0
    tope_maximo = ((height-3)//2)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    menu_usuario_screen.addstr(1, 1, "Seleccionar usuario - password:")
    if tope_minimo > 0:
        menu_usuario_screen.addstr(2, width//2, "▲")
    if tope_maximo < len(lista_usuarios):
        menu_usuario_screen.addstr(height-2, width//2, "▼")
    alto = 3
    for user in enumerate(lista_usuarios):
        if user[0] < tope_maximo and user[0] >= tope_minimo:
            escribir = str(user[1][3])+"  -  "+str(user[1][4])
            if user[0] == (usuario_selected):
                menu_usuario_screen.attron(curses.color_pair(1))
                menu_usuario_screen.addstr(alto, width//2-(len(escribir)//2), escribir)
                menu_usuario_screen.attroff(curses.color_pair(1))
            else:
                menu_usuario_screen.addstr(alto, width//2-(len(escribir)//2), escribir)           
            alto += 2
    menu_usuario_screen.refresh()
    return True       

def imprimir_menu_server(fullscreen, lista_server ,server_selected, tope_minimo, tope_maximo, limpiar):
    height, width = fullscreen.getmaxyx()
    menu_server_screen = curses.newwin(height-7, width//2, 5, width//2)
    menu_server_screen.clear()
    height, width = menu_server_screen.getmaxyx()
    if limpiar:
        menu_server_screen.refresh()
        return False       
    menu_server_screen.border()
    menu_server_screen.addstr(1, 1, "Seleccionar servidor:")
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    if tope_minimo > 0:
        menu_server_screen.addstr(2, width//2, "▲")
    if tope_maximo < len(lista_server):
        menu_server_screen.addstr(height-2, width//2, "▼")
    alto = 3 

    for server in enumerate(lista_server):
        if server[0] < tope_maximo and server[0] >= tope_minimo:
            if server[0] == (server_selected):
                menu_server_screen.attron(curses.color_pair(1))
                menu_server_screen.addstr(alto, width//2-(len(server[1][2])//2), server[1][2])
                menu_server_screen.attroff(curses.color_pair(1))
            else:
                menu_server_screen.addstr(alto, width//2-(len(server[1][2])//2), server[1][2])           
            alto += 2
    menu_server_screen.refresh()
    return True

def menu_usuario(fullscreen, cliente, servidor):
    query = "SELECT * FROM userandpass WHERE up_cliente ='"+str(cliente)+"' AND up_servidor = '"+str(servidor)+"'"
    lista_usuarios = sql_send_query(query)
    usuario_selected = 0
    ejecutar_linea = False
    imprimir_menu_usuario(fullscreen, lista_usuarios, usuario_selected)
    while True:
        key3 = fullscreen.getch()
        if key3 == 27  or key3 == 360:
            break
        elif key3 == curses.KEY_UP and usuario_selected > 0:
                usuario_selected -= 1
        elif key3 == curses.KEY_DOWN and usuario_selected < (len(lista_usuarios)-1):
            usuario_selected += 1
        elif key3 == 330:
            #borrar
            if confirmacion(fullscreen):
                query = "DELETE FROM userandpass WHERE up_cliente ="+str(cliente)+" AND up_servidor = "+str(servidor)+" AND up_cli_srv_id ="+str(lista_usuarios[usuario_selected][2])
                resultado = sql_send_query(query)
                query = "SELECT * FROM userandpass WHERE up_cliente ="+str(cliente)+" AND up_servidor = "+str(servidor)
                lista_usuarios = sql_send_query(query)
        elif key3 == 262:
            # agregar
            texto = "Ingresar el nuevo USUARIO y apretar enter"
            nuevo_usuario = ingresar_de_dato(fullscreen, texto)   
            texto = "Ingresar el password asociado y apretar enter"
            nueva_password = ingresar_de_dato(fullscreen, texto) 
            query = "INSERT INTO userandpass(up_cliente, up_servidor, up_cli_srv_id, up_usuario, up_password) VALUES ('"+str(cliente)+"', '"+str(servidor)+"', '"+str(len(lista_usuarios)+1)+"', '"+nuevo_usuario+"', '"+nueva_password+"')"
            resultado = sql_send_query(query)
            query = "SELECT * FROM userandpass WHERE up_cliente ='"+str(cliente)+"' AND up_servidor = '"+str(servidor)+"'"
            lista_usuarios = sql_send_query(query)
        elif key3 == curses.KEY_ENTER or key3 in [10, 13]:
            query = "SELECT * FROM userandpass WHERE up_cliente ='"+str(cliente)+"' AND up_servidor = '"+str(servidor)+"' AND up_cli_srv_id ='"+str(lista_usuarios[usuario_selected][2])+"'"
            datos_usuario_password = sql_send_query(query)
            query = "SELECT * FROM servidor WHERE srv_cliente = '"+str(cliente)+"' AND srv_id = '"+str(servidor)+"'"
            datos_servidor = sql_send_query(query)
            ejecutar_linea = ["ssh "+datos_usuario_password[0][3]+"@"+datos_servidor[0][3]+" -p"+datos_servidor[0][4] , datos_usuario_password[0][4] ]
            return ejecutar_linea

        imprimir_menu_usuario(fullscreen, lista_usuarios, usuario_selected)
    confirmacion(fullscreen, True) #limpiar la pantalla
    return ejecutar_linea
    
def menu_server(fullscreen, lista_clientes, cliente_selected0, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar):
    cliente_selected = lista_clientes[cliente_selected0]
    height, width = fullscreen.getmaxyx()
    menu_server_screen = curses.newwin(height-7, width//2, 5, width//2)
    menu_server_screen.clear()

    query = "SELECT * FROM servidor WHERE srv_cliente = "+str(cliente_selected[0])
    lista_servidores = sql_send_query(query)
    server_selected = 0
    tope_maximo_servers = ((height-12)//2)
    tope_minimo_servers = 0
    imprimir_menu_server(fullscreen, lista_servidores ,server_selected, tope_minimo_servers, tope_maximo_servers, False)
    server_selected_row = ''

    while True:
        key2 = fullscreen.getch()
        if key2 == 27  or key2 == 360:
            imprimir_menu_server(fullscreen, lista_servidores ,server_selected, tope_minimo_servers, tope_maximo_servers, True) 
            break
        elif key2 == curses.KEY_UP and server_selected > 0:
            server_selected -= 1
        elif key2 == curses.KEY_DOWN and server_selected < (len(lista_servidores)-1):
            server_selected += 1
        elif key2 == 330:
            #borrar
            if confirmacion(fullscreen):
                query = "DELETE FROM userandpass WHERE up_cliente = "+str(cliente_selected[0])+" AND up_servidor = "+str(lista_servidores[server_selected][1])
                resultado = sql_send_query(query)
                query = "DELETE FROM servidor WHERE srv_id = "+str(lista_servidores[server_selected][1])+" AND srv_cliente = "+str(cliente_selected[0])
                resultado = sql_send_query(query)
                query = "SELECT * FROM servidor WHERE srv_cliente = "+str(cliente_selected[0])
                lista_servidores = sql_send_query(query) 
            imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar, False)
        elif key2 == 262:
            # agregar
            texto = "Ingresar el NOMBRE del nuevo servidor y apretar enter"
            nombre_nuevo_servidor = ingresar_de_dato(fullscreen, texto)
            texto = "Ingresar la IP del nuevo servidor y apretar enter"
            ip_nuevo_servidor = ingresar_de_dato(fullscreen, texto)
            texto = "Ingresar el PUERTO del nuevo servidor y apretar enter"
            port_nuevo_servidor = ingresar_de_dato(fullscreen, texto)
            query = "INSERT INTO servidor(srv_cliente, srv_id, srv_descripcion, srv_url, srv_port) VALUES ('"+str(cliente_selected[0])+"', '"+str(len(lista_servidores)+1)+"', '"+nombre_nuevo_servidor+"', '"+ip_nuevo_servidor+"', '"+port_nuevo_servidor+"')"
            resultado = sql_send_query(query)
            query = "SELECT * FROM servidor WHERE srv_cliente = "+str(cliente_selected[0])
            lista_servidores = sql_send_query(query)           
            imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar, False)
        elif key2 == curses.KEY_ENTER or key2 in [10, 13]:
            server_selected_row = menu_usuario(fullscreen, cliente_selected[0], lista_servidores[server_selected][1])
            imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar, False)
            if server_selected_row:
                return server_selected_row

        if server_selected >= tope_maximo_servers:
            tope_maximo_servers += 1
            tope_minimo_servers +=1
        if server_selected < tope_minimo_servers:
            tope_maximo_servers -= 1      
            tope_minimo_servers -= 1
        imprimir_menu_server(fullscreen, lista_servidores ,server_selected, tope_minimo_servers, tope_maximo_servers, False)
    return server_selected_row

def imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected,  tope_minimo, tope_maximo, limpiar):
    height, width = fullscreen.getmaxyx()
    menu_cliente_screen = curses.newwin(height-7, width//2, 5, 0)
    menu_cliente_screen.clear()
    if limpiar:
        menu_cliente_screen.refresh()
        return False
    menu_cliente_screen.border()
    menu_cliente_screen.addstr(1, 1, "Seleccionar cliente:")
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
    height, width = menu_cliente_screen.getmaxyx()
    if tope_minimo > 0:
        menu_cliente_screen.addstr(2, width//2, "▲")
    if tope_maximo < len(lista_clientes)-1:
        menu_cliente_screen.addstr(height-2, width//2, "▼")
    alto = 3 
    for cliente in enumerate(lista_clientes):
        if cliente[0] < tope_maximo and cliente[0] >= tope_minimo:
            if cliente[0] == (cliente_selected):
                menu_cliente_screen.attron(curses.color_pair(1))
                menu_cliente_screen.addstr(alto, width//2-(len(cliente[1][1])//2), cliente[1][1])
                menu_cliente_screen.attroff(curses.color_pair(1))
            else:
                menu_cliente_screen.addstr(alto, width//2-(len(cliente[1][1])//2), cliente[1][1])
            alto += 2
    menu_cliente_screen.refresh()
    return True

def main(fullscreen):
    fullscreen.clear()
    curses.curs_set(0)
    height, width = fullscreen.getmaxyx()

    query = "SELECT * FROM cliente"
    lista_clientes = sql_send_query(query)
    cliente_selected = 0
    tope_maxima_de_lineas_de_clientes_a_mostrar = ((height-12)//2)
    tope_minimo_de_lineas_de_clientes_a_mostrar = 0
    conex = ''

    while True:
        imprimir_header(fullscreen)
        imprimir_footer(fullscreen,"bajar -  ▼  ","subir -  ▲  "," eliminar - SUPR   "," agregar - INICIO ","elegir - INTRO ","      salir - FIN    ")
        fullscreen.refresh()
        imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar, False)
        key = fullscreen.getch()
        if key == 27 or key == 360:
            #salir
            break
        elif key == curses.KEY_UP and cliente_selected > 0:
            cliente_selected -= 1
        elif key == curses.KEY_DOWN and cliente_selected < (len(lista_clientes)-1):
            cliente_selected += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            imprimir_footer(fullscreen,"bajar -  ▼  ","subir -  ▲  "," eliminar - SUPR   "," agregar - INICIO ","elegir - INTRO ","      volver - FIN    ")
            fullscreen.refresh()
            conex = menu_server(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar)
            if conex:
                return conex
        elif key == 330:
            # eliminar
            if confirmacion(fullscreen):
                query = "DELETE FROM userandpass WHERE up_cliente = "+str(lista_clientes[cliente_selected][0])
                resultado = sql_send_query(query)
                query = "DELETE FROM servidor WHERE srv_cliente = "+str(lista_clientes[cliente_selected][0])
                resultado = sql_send_query(query)
                query = "DELETE FROM cliente WHERE cli_id = "+str(lista_clientes[cliente_selected][0])
                resultado = sql_send_query(query)
                query = "SELECT * FROM cliente"
                lista_clientes = sql_send_query(query)
            confirmacion(fullscreen, True)
        elif key == 262:
            # agregar
            texto = "Ingresar el nombre del nuevo cliente y apretar enter"
            nuevo_cliente = ingresar_de_dato(fullscreen, texto)
            query = "INSERT INTO cliente(cli_descripcion) VALUES ('"+nuevo_cliente+"')"
            resultado = sql_send_query(query)
            query = "SELECT * FROM cliente"
            lista_clientes = sql_send_query(query)

        if cliente_selected >= tope_maxima_de_lineas_de_clientes_a_mostrar:
            tope_maxima_de_lineas_de_clientes_a_mostrar += 1
            tope_minimo_de_lineas_de_clientes_a_mostrar +=1
        if cliente_selected < tope_minimo_de_lineas_de_clientes_a_mostrar:
            tope_maxima_de_lineas_de_clientes_a_mostrar -= 1
            tope_minimo_de_lineas_de_clientes_a_mostrar -= 1
        imprimir_menu_cliente(fullscreen, lista_clientes, cliente_selected, tope_minimo_de_lineas_de_clientes_a_mostrar, tope_maxima_de_lineas_de_clientes_a_mostrar, False)     
    return conex




salida = curses.wrapper(main)
if(salida):
    print("Las password es:  "+salida[1])
    import os
    os.system(salida[0])