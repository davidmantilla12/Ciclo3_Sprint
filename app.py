import os
import sqlite3
from sqlite3 import Error

from flask import Flask, flash, redirect, render_template, request
from flask_wtf import form

from pilotos import piloto
from vuelos import vuelo
from comentarios import comentario

app = Flask(__name__)
app.secret_key=os.urandom(24)
sesion_iniciada =False
nombre =""

@app.route("/", methods=["GET","POST"])
def inicio_usuario():
    # Si ya se inició sesión  -> Pantalla de inicio para usuario específico
    # sino -> página de bienvenida para usuarios
    form=vuelo()
    if nombre =="Admin":
        return render_template("dashboard_admin.html",sesion_iniciada=sesion_iniciada,nombre =nombre)
    else:
        return render_template("inicio.html", sesion_iniciada=sesion_iniciada,nombre =nombre,form=form)

@app.route("/Registro", methods=["GET", "POST"])
def registro():
    # Seleccionar método de registro e ingresar a la base de datos
    global registro_exitoso
    return render_template('/registro.html')


@app.route("/Iniciar_Sesion", methods=["GET", "POST"])
def iniciarSesion():
    # Seleccionar método de inicio de sesion y volver a la página de inicio
    global sesion_iniciada
    global nombre
    if request.method =="GET":
        return render_template("inicio_sesion.html")
    else:
        sesion_iniciada=True
        nombre = request.form["nombre"]
        return redirect("/")

@app.route("/cerrar_sesion", methods = ["POST"])
def cerrarSesion():
    global sesion_iniciada
    global nombre

    sesion_iniciada=False
    nombre=""
    return redirect("/")

@app.route("/Mi_Perfil/<id_usuario>", methods=["GET", "POST"])
def miPerfil(id_usuario):
    # Ver / modificar información personal y de vuelos tomados en caso de cambios guardar en base de datos
    if (id_usuario in lista_usuarios):
        return f"Página Mi Perfil del usuario {id_usuario}"
    else: 
        return f"Error, el usuario {id_usuario} no existe"


@app.route("/Buscar_vuelos", methods=["POST"])
def buscarVuelos():
    global sesion_iniciada
    global nombre
    form = vuelo()
    # Nueva página para listar los vuelos según las características indicadas en la página de inicio
    ida= request.args.get("ida")
    origen=form.origen.data
    destino=form.destino.data
    fecha_ida=form.fecha.data
    fecha_vuelta=form.fecha_vuelta.data
    ninos=request.args.get("niños")
    adultos=request.args.get("adultos") 

    try:
        with sqlite3.connect("viajesun.db") as con:
            
            con.row_factory=sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM vuelos WHERE origen=? AND destino=? AND fecha=?", [origen,destino,fecha_ida]) 
            row=cur.fetchall()
            return render_template("buscar_vuelos.html",ida=ida,origen=origen,destino=destino,fecha_ida=fecha_ida,fecha_vuelta=fecha_vuelta,ninos=ninos,adultos=adultos,sesion_iniciada=sesion_iniciada,nombre=nombre,row=row)        

    except Error:
        print(Error)
        flash(Error)
    return render_template("buscar_vuelos.html",ida=ida,origen=origen,destino=destino,fecha_ida=fecha_ida,fecha_vuelta=fecha_vuelta,ninos=ninos,adultos=adultos,sesion_iniciada=sesion_iniciada,nombre=nombre)


@app.route("/Reservar_vuelo", methods=["GET", "POST"])
def reserva():
    global sesion_iniciada
    global nombre
    # Página para reserva de vuelo, seleccionar métodos de págo y confirmación de datos de los pasajeros
    ida= request.args.get("vuelo_ida")
    vuelta=request.args.get("vuelo_vuelta")
    return render_template("reserva.html",sesion_iniciada=sesion_iniciada,nombre=nombre,ida=ida,vuelta=vuelta)

@app.route("/Mis_vuelos", methods=["GET"])
def misVuelos():
    # Página para listar los vuelos tomados y reservados
    return "Página Mis vuelos"

@app.route("/agregar_vuelo", methods=['GET','POST'])
def agregar_vuelo():
    global nombre
    global sesion_iniciada
    form=vuelo()
    if request.method=='POST':
        origen=form.origen.data
        destino=form.destino.data
        hora_salida=str(form.hora_salida.data)
        hora_llegada=str(form.hora_llegada.data) 
        fecha=str(form.fecha.data)
        piloto=form.piloto.data
        asientos=form.asientos.data
        valor=str(form.valor.data)
        try:
            with sqlite3.connect('viajesun.db') as con:
                cur=con.cursor()                
                cur.execute("INSERT INTO vuelos (origen, destino, hora_salida, hora_llegada, fecha, piloto, asientos, valor) VALUES (?,?,?,?,?,?,?,?);", [origen,destino,hora_salida,hora_llegada,fecha,piloto,asientos,valor])
                con.commit()
                print("Vuelo añadido")
        except Error:
            print(Error)
        
    return render_template('agregar_vuelo.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form)

@app.route("/editar_vuelo", methods=['GET','POST'])
def editar_vuelo():
    global nombre
    global sesion_iniciada
    form=vuelo()
    row={
        "id_Vuelo":"",
        "origen":"",
        "destino":"",
        "hora_salida":"",
        "hora_llegada":"",
        "fecha":"",
        "piloto":"",
        "asientos":"",
        "valor":"",
    }
    if request.method=='POST':
        if form.origen.data=="":
            
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM vuelos WHERE id_Vuelo = ?', [form.id_vuelo.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)


        else:
            id_Vuelo=(form.id_vuelo.data)
            origen=form.origen.data
            destino=form.destino.data
            hora_salida=str(form.hora_salida.data)
            hora_llegada=str(form.hora_llegada.data) 
            fecha=str(form.fecha.data)
            piloto=form.piloto.data
            asientos=form.asientos.data
            valor=str(form.valor.data)
            print(id_Vuelo,origen,destino,hora_llegada,hora_salida,fecha,piloto,asientos,valor)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("UPDATE vuelos SET origen=?, destino=?, hora_salida=?, hora_llegada=?, fecha=?, piloto=?, asientos=?, valor=? WHERE id_Vuelo=?", [origen,destino,hora_salida,hora_llegada,fecha,piloto,asientos,valor,id_Vuelo])
                    con.commit()
                    print("Vuelo editado")
            except Error:
                print(Error)
        
    return render_template('editar_vuelo.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)

@app.route("/eliminar_vuelo", methods=['GET','POST'])
def eliminar_vuelo():
    global nombre
    global sesion_iniciada
    form=vuelo()
    row={
        "id_Vuelo":"",
        "origen":"",
        "destino":"",
        "hora_salida":"",
        "hora_llegada":"",
        "fecha":"",
        "piloto":"",
        "asientos":"",
        "valor":"",
    }
    if request.method=='POST':
        if form.origen.data=="":
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM vuelos WHERE id_Vuelo = ?', [form.id_vuelo.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)

        else:
            id_Vuelo=(form.id_vuelo.data)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("DELETE FROM vuelos WHERE id_Vuelo=?", [id_Vuelo])
                    con.commit()
                    print("Vuelo ELIMINADO")
            except Error:
                print(Error)
        
    return render_template('eliminar_vuelo.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)

@app.route("/agregar_piloto", methods=['GET','POST'])
def agregar_piloto():
    global nombre
    global sesion_iniciada
    form=piloto()
    if request.method=='POST':
        nombre_piloto=form.nombre.data
        cedula=form.cedula.data
        trama_vuelos=form.vuelos.data
        try:
            with sqlite3.connect('viajesun.db') as con:
                cur=con.cursor()                
                cur.execute("INSERT INTO pilotos (nombre, cedula, vuelos_asignados) VALUES (?,?,?)", [nombre_piloto,cedula,trama_vuelos])
                con.commit()
                print("Piloto añadido")
        except Error:
            print(Error)    
    return render_template('agregar_piloto.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form)

@app.route("/editar_piloto", methods=['GET','POST'])
def editar_piloto():
    global nombre
    global sesion_iniciada

    form=piloto()

    row={
        "id_Piloto":"",
        "nombre":"",
        "cedula":"",
        "vuelos_asignados":""    
    }
    if request.method=='POST':
        if form.nombre.data=="":
            
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM pilotos WHERE id_Piloto = ?', [form.id_piloto.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)


        else:
            id_Piloto=(form.id_piloto.data)
            nombre_piloto=form.nombre.data
            cedula=form.cedula.data
            trama_vuelos=str(form.vuelos.data)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("UPDATE pilotos SET nombre=?, cedula=?, vuelos_asignados=? WHERE id_Piloto=?", [nombre_piloto,cedula,trama_vuelos,id_Piloto])
                    con.commit()
                    print("Piloto editado")
            except Error:
                print(Error)
        
    return render_template('editar_piloto.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)

@app.route("/eliminar_piloto", methods=['GET','POST'])
def eliminar_piloto():
    global nombre
    global sesion_iniciada
    form=piloto()
    row={
        "id_Piloto":"",
        "nombre":"",
        "cedula":"",
        "vuelos_asignados":""    
    }
    if request.method=='POST':
        if form.nombre.data=="":
            
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM pilotos WHERE id_Piloto = ?', [form.id_piloto.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)
        else:
            id_Piloto=(form.id_piloto.data)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("DELETE FROM pilotos WHERE id_Piloto=?", [id_Piloto])
                    con.commit()
                    print("Piloto eliminado")
            except Error:
                print(Error)
        
    return render_template('eliminar_piloto.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)


@app.route("/agregar_comentario", methods=['POST','GET'])
def agregar_comentario():
    global nombre
    global sesion_iniciada
    form = comentario()
    usuario=form.usuario.data
    puntuacion=form.puntuacion.data
    comentario2=form.comentario.data
    id_vuelo=form.id_vuelo.data
    try:
        with sqlite3.connect('viajesun.db') as con:
            cur=con.cursor()                
            cur.execute("INSERT INTO comentarios (usuario,puntuacion,comentario,id_vuelo) VALUES (?,?,?,?);", [usuario,puntuacion,comentario2,id_vuelo])
            con.commit()
            print("Comentario agregado")
    except Error:
        print(Error)    
    return render_template('agregar_comentario.html',sesion_iniciada=sesion_iniciada, nombre=nombre, form=form)

@app.route("/editar_comentario", methods=['GET','POST'])
def editar_comentario():
    global nombre
    global sesion_iniciada
    form=comentario()
    row={
        "id_vuelo":"",
        "usuario":"",
        "puntuacion":"",
        "comentario":"",
    }
    if request.method=='POST':
        if form.usuario.data=="":
            
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM comentarios WHERE id_comentario = ?', [form.id_comentario.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)

        else:
            id_comentario=(form.id_comentario.data)
            usuario=form.usuario.data
            puntuacion=form.puntuacion.data
            comentario2=str(form.comentario.data)
            id_vuelo=(form.id_vuelo.data) 
            print(id_comentario,usuario,puntuacion,comentario2,id_vuelo)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("UPDATE comentarios SET usuario=?, puntuacion=?, comentario=?, id_vuelo=? WHERE id_comentario=?", [usuario,puntuacion,comentario2,id_vuelo,id_comentario])
                    con.commit()
                    print("comentario editado")
            except Error:
                print(Error)
        
    return render_template('editar_comentario.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)

@app.route("/eliminar_comentario", methods=['GET','POST'])
def eliminar_comentario():
    global nombre
    global sesion_iniciada
    form=comentario()
    row={
        "id_Vuelo":"",
        "usuario":"",
        "puntuacion":"",
        "comentario":"",
    }
    if request.method=='POST':
        if form.origen.data=="":
            try:
                with sqlite3.connect('viajesun.db') as con:
                    con.row_factory=sqlite3.Row
                    cur = con.cursor()
                    cur.execute('SELECT * FROM vuelos WHERE id_Vuelo = ?', [form.id_comentario.data])
                    row = cur.fetchone() 
            except Error:
                print(Error)

        else:
            id_comentario=(form.id_comentario.data)
            try:
                with sqlite3.connect('viajesun.db') as con:
                    cur=con.cursor()                
                    cur.execute("DELETE FROM vuelos WHERE id_Vuelo=?", [id_comentario])
                    con.commit()
                    print("Vuelo ELIMINADO")
            except Error:
                print(Error)
        
    return render_template('eliminar_comentario.html',sesion_iniciada=sesion_iniciada,nombre=nombre,form=form,row=row)


if (__name__=="__main__"):
    app.run(debug=True)
