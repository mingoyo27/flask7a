from flask import Flask
from markupsafe import escape

from flask import render_template
from flask import request

import pusher

import mysql.connector
import datetime
import pytz

con = mysql.connector.connect(
  host="185.232.14.52",
  database="u760464709_tst_sep",
  user="u760464709_tst_sep_usr",
  password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    con.close()
  
    return render_template("app.html")

@app.route("/alumnos")
def alumnos():
    con.close()
  
    return render_template("alumnos.html")

@app.route("/alumnos/guardar", methods=["POST"])
def alumnosGuardar():
    con.close()
  
    matricula      = request.form["txtMatriculaFA"]
    nombreapellido = request.form["txtNombreApellidoFA"]

    return f"Matrícula: {matricula} Nombre y Apellido: {nombreapellido}"

@app.route("/registrar", methods=["GET"])
def registrar():
    # Parámetros de la solicitud GET
    args = request.args
    correo_electronico = args.get("correo_electronico")
    nombre = args.get("nombre")
    asunto = args.get("asunto")

    try:
        # Conexión a la base de datos
        con = obtener_conexion()
        cursor = con.cursor()

        # Consulta SQL para insertar el registro, sin incluir `Id_Contacto`
        sql = "INSERT INTO tst0_contacto (Correo_Electronico, Nombre, Asunto) VALUES (%s, %s, %s)"
        val = (correo_electronico, nombre, asunto)
        cursor.execute(sql, val)
        con.commit()

        # Enviar notificación con Pusher
        pusher_client.trigger("registrosTiempoReal", "registroTiempoReal", {
            "correo_electronico": correo_electronico,
            "nombre": nombre,
            "asunto": asunto
        })

        return jsonify({"status": "Registro exitoso"}), 200

    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

    finally:
        if con.is_connected():
            con.close()

    return registros
