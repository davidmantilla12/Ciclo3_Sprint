from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


app = Flask(__name__)

lista_usuarios = ["Danna","Dario","Jose","Alejandra"]
lista_vuelos = {
    "1": "vuelo 1", 
    "2": "vuelo 2", 
    "3": "vuelo 3",
    "4": "vuelo 4",
    "5": "vuelo 5"   
}

sesion_iniciada =False
nombre =""

@app.route("/", methods=["GET","POST"])
def inicio_usuario():
    # Si ya se inició sesión  -> Pantalla de inicio para usuario específico
    # sino -> página de bienvenida para usuarios

    if nombre =="Admin":
        return render_template("dashboard_admin.html")
    else:
        return render_template("inicio.html", sesion_iniciada=sesion_iniciada,nombre =nombre)



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


@app.route("/Buscar_vuelos", methods=["GET"])
def buscarVuelos():
    global sesion_iniciada
    global nombre
    # Nueva página para listar los vuelos según las características indicadas en la página de inicio
    ida= request.args.get("ida")
    origen=request.args.get("origen")
    destino=request.args.get("destino")
    fecha_ida=request.args.get("fecha_ida")
    fecha_vuelta=request.args.get("fecha_vuelta")
    ninos=request.args.get("niños")
    adultos=request.args.get("adultos")
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




if (__name__=="__main__"):
    app.run(debug=True)
